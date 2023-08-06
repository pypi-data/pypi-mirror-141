import json
import shutil
import os

import pandas as pd
from mindsdb_sql import parse_sql

import mindsdb_datasources
from mindsdb.__about__ import __version__ as mindsdb_version
from mindsdb.interfaces.model.model_interface import ModelInterface
from mindsdb_datasources import (
    FileDS, ClickhouseDS, MariaDS, MySqlDS, PostgresDS, MSSQLDS, MongoDS,
    SnowflakeDS, AthenaDS, CassandraDS, ScyllaDS, TrinoDS
)
from mindsdb.utilities.config import Config
from mindsdb.utilities.log import log
from mindsdb.utilities.json_encoder import CustomJSONEncoder
from mindsdb.utilities.with_kwargs_wrapper import WithKWArgsWrapper
from mindsdb.interfaces.storage.db import session, Datasource, Semaphor, Predictor
from mindsdb.interfaces.storage.fs import FsStore
from mindsdb.interfaces.database.integrations import DatasourceController
from mindsdb.interfaces.database.views import ViewController
from mindsdb.api.mysql.mysql_proxy.utilities.sql import query_df


class QueryDS:
    def __init__(self, query, source, source_type, company_id):
        self.query = query
        self.source = source
        self.source_type = source_type
        self.company_id = company_id

    def query(self, q):
        pass

    @property
    def df(self):
        view_interface = WithKWArgsWrapper(
            ViewController(),
            company_id=self.company_id
        )

        datasource_interface = WithKWArgsWrapper(
            DatasourceController(),
            company_id=self.company_id
        )

        data_store = WithKWArgsWrapper(
            DataStore(),
            company_id=self.company_id
        )

        query = self.query
        if self.source_type == 'view_query':
            if isinstance(query, str):
                query = parse_sql(query, dialect='mysql')
            query_str = str(query)

            table = query.from_table.parts[-1]
            view_metadata = view_interface.get(name=table)

            datasource = datasource_interface.get_db_integration_by_id(view_metadata['datasource_id'])
            datasource_name = datasource['name']

            dataset_name = data_store.get_vacant_name(table)
            data_store.save_datasource(dataset_name, datasource_name, {'query': view_metadata['query']})
            try:
                dataset_object = data_store.get_datasource_obj(dataset_name)
                data_df = dataset_object.df
            finally:
                data_store.delete_datasource(dataset_name)
        elif self.source_type == 'file_query':
            if isinstance(query, str):
                query = parse_sql(query, dialect='mysql')
            table = query.from_table.parts[-1]
            ds = data_store.get_datasource_obj(table, raw=False)
            file_df = ds.df
            data_df = query_df(file_df, query)
        return data_df


class DataStore():
    def __init__(self):
        self.config = Config()
        self.fs_store = FsStore()
        self.dir = self.config['paths']['datasources']
        self.model_interface = ModelInterface()

    def get_analysis(self, name, company_id=None):
        datasource_record = session.query(Datasource).filter_by(company_id=company_id, name=name).first()
        if datasource_record.analysis is None:
            return None
        analysis = json.loads(datasource_record.analysis)
        return analysis

    def start_analysis(self, name, company_id=None):
        datasource_record = session.query(Datasource).filter_by(company_id=company_id, name=name).first()
        if datasource_record.analysis is not None:
            return None
        semaphor_record = session.query(Semaphor).filter_by(company_id=company_id, entity_id=datasource_record.id, entity_type='datasource').first()
        if semaphor_record is None:
            semaphor_record = Semaphor(company_id=company_id, entity_id=datasource_record.id, entity_type='datasource', action='write')
            session.add(semaphor_record)
            session.commit()
        else:
            return
        try:
            analysis = self.model_interface.analyse_dataset(ds=self.get_datasource_obj(name, raw=True, company_id=company_id), company_id=company_id)
            datasource_record = session.query(Datasource).filter_by(company_id=company_id, name=name).first()
            datasource_record.analysis = json.dumps(analysis, cls=CustomJSONEncoder)
            session.commit()
        except Exception as e:
            log.error(e)
        finally:
            semaphor_record = session.query(Semaphor).filter_by(company_id=company_id, entity_id=datasource_record.id, entity_type='datasource').first()
            session.delete(semaphor_record)
            session.commit()

    def get_datasources(self, name=None, company_id=None):
        datasource_arr = []
        if name is not None:
            datasource_record_arr = session.query(Datasource).filter_by(company_id=company_id, name=name)
        else:
            datasource_record_arr = session.query(Datasource).filter_by(company_id=company_id)
        for datasource_record in datasource_record_arr:
            try:
                if datasource_record.data is None:
                    continue
                datasource = json.loads(datasource_record.data)
                datasource['created_at'] = datasource_record.created_at
                datasource['updated_at'] = datasource_record.updated_at
                datasource['name'] = datasource_record.name
                datasource['id'] = datasource_record.id
                datasource_arr.append(datasource)
            except Exception as e:
                log.error(e)
        return datasource_arr

    def get_data(self, name, where=None, limit=None, offset=None, company_id=None):
        offset = 0 if offset is None else offset
        ds = self.get_datasource_obj(name, company_id=company_id)

        if limit is not None:
            # @TODO Add `offset` to the `filter` method of the datasource and get rid of `offset`
            filtered_ds = ds.filter(where=where, limit=limit + offset).iloc[offset:]
        else:
            filtered_ds = ds.filter(where=where)

        filtered_ds = filtered_ds.where(pd.notnull(filtered_ds), None)
        data = filtered_ds.to_dict(orient='records')
        return {
            'data': data,
            'rowcount': len(ds),
            'columns_names': list(data[0].keys())
        }

    def get_datasource(self, name, company_id=None):
        datasource_arr = self.get_datasources(name, company_id=company_id)
        if len(datasource_arr) == 1:
            return datasource_arr[0]
        # @TODO: Remove when db swithc is more stable, this should never happen, but good santiy check while this is kinda buggy
        elif len(datasource_arr) > 1:
            log.error('Two or more datasource with the same name, (', len(datasource_arr), ') | Full list: ', datasource_arr)
            raise Exception('Two or more datasource with the same name')
        return None

    def delete_datasource(self, name, company_id=None):
        datasource_record = Datasource.query.filter_by(company_id=company_id, name=name).first()
        if not Config()["force_datasource_removing"]:
            linked_models = Predictor.query.filter_by(company_id=company_id, datasource_id=datasource_record.id).all()
            if linked_models:
                raise Exception("Can't delete {} datasource because there are next models linked to it: {}".format(name, [model.name for model in linked_models]))
        session.query(Semaphor).filter_by(
            company_id=company_id, entity_id=datasource_record.id, entity_type='datasource'
        ).delete()
        session.delete(datasource_record)
        session.commit()
        self.fs_store.delete(f'datasource_{company_id}_{datasource_record.id}')
        try:
            shutil.rmtree(os.path.join(self.dir, f'{company_id}@@@@@{name}'))
        except Exception:
            pass

    def get_vacant_name(self, base=None, company_id=None):
        ''' returns name of datasource, which starts from 'base' and ds with that name is not exists yet
        '''
        if base is None:
            base = 'datasource'
        datasources = session.query(Datasource.name).filter_by(company_id=company_id).all()
        datasources_names = [x[0] for x in datasources]
        if base not in datasources_names:
            return base
        for i in range(1, 1000):
            candidate = f'{base}_{i}'
            if candidate not in datasources_names:
                return candidate
        raise Exception(f"Can not find appropriate name for datasource '{base}'")

    def create_datasource(self, source_type, source, file_path=None, company_id=None, ds_meta_dir=None):
        datasource_controller = DatasourceController()
        if source_type == 'file_query' or source_type == 'view_query':
            dsClass = QueryDS
            creation_info = {
                'class': dsClass.__name__,
                'args': [],
                'kwargs': {
                    'query': source['query'],
                    'source': source['source'],   # view|file
                    'source_type': source_type,
                    'company_id': company_id
                }
            }

            ds = dsClass(**creation_info['kwargs'])
        elif source_type == 'file':
            source = os.path.join(ds_meta_dir, source)
            shutil.move(file_path, source)
            ds = FileDS(source)

            creation_info = {
                'class': 'FileDS',
                'args': [source],
                'kwargs': {}
            }

        elif datasource_controller.get_db_integration(source_type, company_id) is not None:
            integration = datasource_controller.get_db_integration(source_type, company_id)

            ds_class_map = {
                'clickhouse': ClickhouseDS,
                'mariadb': MariaDS,
                'mysql': MySqlDS,
                'singlestore': MySqlDS,
                'postgres': PostgresDS,
                'cockroachdb': PostgresDS,
                'mssql': MSSQLDS,
                'mongodb': MongoDS,
                'snowflake': SnowflakeDS,
                'athena': AthenaDS,
                'cassandra': CassandraDS,
                'scylladb': ScyllaDS,
                'trinodb': TrinoDS
            }

            try:
                dsClass = ds_class_map[integration['type']]
            except KeyError:
                raise KeyError(f"Unknown DS type: {source_type}, type is {integration['type']}")

            if dsClass is None:
                raise Exception(f"Unsupported datasource: {source_type}, type is {integration['type']}, please install required dependencies!")

            if integration['type'] in ['clickhouse']:
                creation_info = {
                    'class': dsClass.__name__,
                    'args': [],
                    'kwargs': {
                        'query': source['query'],
                        'user': integration['user'],
                        'password': integration['password'],
                        'host': integration['host'],
                        'port': integration['port']
                    }
                }
                ds = dsClass(**creation_info['kwargs'])

            elif integration['type'] in ['mssql', 'postgres', 'cockroachdb', 'mariadb', 'mysql', 'singlestore', 'cassandra', 'scylladb']:
                creation_info = {
                    'class': dsClass.__name__,
                    'args': [],
                    'kwargs': {
                        'query': source['query'],
                        'user': integration['user'],
                        'password': integration['password'],
                        'host': integration['host'],
                        'port': integration['port']
                    }
                }
                kwargs = creation_info['kwargs']

                integration_folder_name = f'integration_files_{company_id}_{integration["id"]}'
                if integration['type'] in ('mysql', 'mariadb'):
                    kwargs['ssl'] = integration.get('ssl')
                    kwargs['ssl_ca'] = integration.get('ssl_ca')
                    kwargs['ssl_cert'] = integration.get('ssl_cert')
                    kwargs['ssl_key'] = integration.get('ssl_key')
                    for key in ['ssl_ca', 'ssl_cert', 'ssl_key']:
                        if isinstance(kwargs[key], str) and len(kwargs[key]) > 0:
                            kwargs[key] = os.path.join(
                                self.integrations_dir,
                                integration_folder_name,
                                kwargs[key]
                            )
                elif integration['type'] in ('cassandra', 'scylla'):
                    kwargs['secure_connect_bundle'] = integration.get('secure_connect_bundle')
                    if (
                        isinstance(kwargs['secure_connect_bundle'], str)
                        and len(kwargs['secure_connect_bundle']) > 0
                    ):
                        kwargs['secure_connect_bundle'] = os.path.join(
                            self.integrations_dir,
                            integration_folder_name,
                            kwargs['secure_connect_bundle']
                        )

                if 'database' in integration:
                    kwargs['database'] = integration['database']

                if 'database' in source:
                    kwargs['database'] = source['database']

                ds = dsClass(**kwargs)

            elif integration['type'] == 'snowflake':
                creation_info = {
                    'class': dsClass.__name__,
                    'args': [],
                    'kwargs': {
                        'query': source['query'],
                        'schema': source.get('schema', integration['schema']),
                        'warehouse': source.get('warehouse', integration['warehouse']),
                        'database': source.get('database', integration['database']),
                        'host': integration['host'],
                        'password': integration['password'],
                        'user': integration['user'],
                        'account': integration['account']
                    }
                }

                ds = dsClass(**creation_info['kwargs'])

            elif integration['type'] == 'mongodb':
                if isinstance(source['find'], str):
                    source['find'] = json.loads(source['find'])
                creation_info = {
                    'class': dsClass.__name__,
                    'args': [],
                    'kwargs': {
                        'database': source['database'],
                        'collection': source['collection'],
                        'query': source['find'],
                        'user': integration['user'],
                        'password': integration['password'],
                        'host': integration['host'],
                        'port': integration['port']
                    }
                }

                ds = dsClass(**creation_info['kwargs'])

            elif integration['type'] == 'athena':
                creation_info = {
                    'class': dsClass.__name__,
                    'args': [],
                    'kwargs': {
                        'query': source['query'],
                        'staging_dir': source['staging_dir'],
                        'database': source['database'],
                        'access_key': source['access_key'],
                        'secret_key': source['secret_key'],
                        'region_name': source['region_name']
                    }
                }

                ds = dsClass(**creation_info['kwargs'])

            elif integration['type'] == 'trinodb':
                creation_info = {
                    'class': dsClass.__name__,
                    'args': [],
                    'kwargs': {
                        'query': source['query'],
                        'user': integration['user'],
                        'password': integration['password'],
                        'host': integration['host'],
                        'port': integration['port'],
                        'schema': integration['schema'],
                        'catalog': integration['catalog']
                    }
                }

                ds = dsClass(**creation_info['kwargs'])
        else:
            # This probably only happens for urls
            ds = FileDS(source)
            creation_info = {
                'class': 'FileDS',
                'args': [source],
                'kwargs': {}
            }
        return ds, creation_info

    def save_datasource(self, name, source_type, source, file_path=None, company_id=None):
        if source_type == 'file' and (file_path is None):
            raise Exception('`file_path` argument required when source_type == "file"')

        datasource_record = session.query(Datasource).filter_by(company_id=company_id, name=name).first()
        while datasource_record is not None:
            raise Exception(f'Datasource with name {name} already exists')

        if source_type == 'views':
            source_type = 'view_query'
        elif source_type == 'files':
            source_type = 'file_query'

        try:
            datasource_record = Datasource(
                company_id=company_id,
                name=name,
                datasources_version=mindsdb_datasources.__version__,
                mindsdb_version=mindsdb_version
            )
            session.add(datasource_record)
            session.commit()

            ds_meta_dir = os.path.join(self.dir, f'{company_id}@@@@@{name}')
            os.mkdir(ds_meta_dir)

            ds, creation_info = self.create_datasource(source_type, source, file_path, company_id, ds_meta_dir)

            if hasattr(ds, 'get_columns') and hasattr(ds, 'get_row_count'):
                try:
                    column_names = ds.get_columns()
                    row_count = ds.get_row_count()
                except Exception:
                    df = ds.df
                    column_names = list(df.keys())
                    row_count = len(df)
            else:
                df = ds.df
                column_names = list(df.keys())
                row_count = len(df)

            if '' in column_names or len(column_names) != len(set(column_names)):
                shutil.rmtree(ds_meta_dir)
                raise Exception('Each column in datasource must have unique non-empty name')

            datasource_record.creation_info = json.dumps(creation_info)
            datasource_record.data = json.dumps({
                'source_type': source_type,
                'source': source,
                'row_count': row_count,
                'columns': [dict(name=x) for x in column_names]
            })

            self.fs_store.put(f'{company_id}@@@@@{name}', f'datasource_{company_id}_{datasource_record.id}', self.dir)
            session.commit()

        except Exception as e:
            log.error(f'Error creating datasource {name}, exception: {e}')
            try:
                self.delete_datasource(name, company_id=company_id)
            except Exception:
                pass
            raise e

        return self.get_datasource_obj(name, raw=True, company_id=company_id)

    def get_datasource_obj(self, name=None, id=None, raw=False, company_id=None):
        try:
            if name is not None:
                datasource_record = session.query(Datasource).filter_by(company_id=company_id, name=name).first()
            else:
                datasource_record = session.query(Datasource).filter_by(company_id=company_id, id=id).first()

            self.fs_store.get(f'{company_id}@@@@@{name}', f'datasource_{company_id}_{datasource_record.id}', self.dir)
            creation_info = json.loads(datasource_record.creation_info)
            if raw:
                return creation_info
            else:
                return eval(creation_info['class'])(*creation_info['args'], **creation_info['kwargs'])
        except Exception as e:
            log.error(f'Error getting datasource {name}, exception: {e}')
            return None
