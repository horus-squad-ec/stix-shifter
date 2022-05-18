import json
from pydruid.db import connect, exceptions

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    else:
        return False

class APIClient():

    def __init__(self, connection, configuration):
        auth = configuration.get('auth')
        self.user = auth.get('username') if 'username' in auth.keys() else None
        self.password = auth.get('password') if 'password' in auth.keys() else None
        self.host = connection.get('host')
        self.port = connection.get('port')
        self.path = connection.get('path') if 'path' in connection.keys() else '/druid/v2/sql/'
        self.scheme = connection.get('scheme') if 'scheme' in connection.keys() else 'http'
        self.ssl_verify_cert = str2bool(connection.get('ssl_verify_cert')) if 'ssl_verify_cert' in connection.keys() else True
        self.ssl_client_cert = connection.get('ssl_client_cert') if 'ssl_client_cert' in connection.keys() else None

    def ping_data_source(self):
        # Pings the data source
        response = {'code': 200, 'message': 'All Good!'}
        try:
            conn = connect(host=self.host, port=self.port, path=self.path, scheme=self.scheme, user=self.user, password=self.password,
                          ssl_verify_cert=self.ssl_verify_cert, ssl_client_cert=self.ssl_client_cert)
            curs = conn.cursor()
            curs.execute('SELECT 1')
        except Exception as err:
            response['code'] = 502
            response['message'] = err
        else:
            conn.close()
        return response

    def run_search(self, query, start=None, rows=None):
        # Return the search results. Results must be in JSON format before translating into STIX
        response = {'code': 200, 'message': 'All Good!', 'result': []}
        try:
            conn = connect(host=self.host, port=self.port, path=self.path, scheme=self.scheme, user=self.user, password=self.password,
                        ssl_verify_cert=self.ssl_verify_cert, ssl_client_cert=self.ssl_client_cert)
            curs = conn.cursor()
            if rows:
                query = '{0} {1} {2}'.format(query, 'LIMIT', rows)
            if start:
                query = '{0} {1} {2}'.format(query, 'OFFSET', start)
            curs.execute(query)
            results_list = []
            for row in curs:
                results_list.append(row._asdict())
            response['result'] = results_list
        except exceptions.ProgrammingError as err:
            response['code'] = 500
            response['message'] = err
        except Exception as err:
            response['code'] = 502
            response['message'] = err
        else:
            conn.close()
        return response
