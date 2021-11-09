from stix_shifter_utils.modules.base.stix_transmission.base_ping_connector import BasePingConnector
from stix_shifter_utils.utils import logger
from stix_shifter_utils.utils.error_response import ErrorResponder


class PingConnector(BasePingConnector):
    def __init__(self, api_client):
        self.api_client = api_client
        self.logger = logger.set_logger(__name__)

    def ping_connection(self):
        try:
            response = self.api_client.ping_data_source()
            response_code = response.code
            response_body = response.read().decode('utf-8')

            # Construct a response object
            return_obj = dict()
            if response_code == 200:
                return_obj['success'] = True
            else:
                response_dict = {'code': response_code, 'message': response_body}
                ErrorResponder.fill_error(return_obj, response_dict, ['message'])
            return return_obj
        except Exception as err:
            self.logger.error('error when pinging datasource: %s', err, exc_info=True)
            raise