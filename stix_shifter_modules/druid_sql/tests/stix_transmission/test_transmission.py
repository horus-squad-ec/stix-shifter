from stix_shifter_modules.druid_sql.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils.error_response import ErrorCode
import unittest
from unittest.mock import patch
import sys

@patch('stix_shifter_modules.druid_sql.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestDruidConnection(unittest.TestCase, object):
    configuration = {
        'auth': {}
    }

    connection = {
        'host': 'chase.sl.cloud9.ibm.com'
    }

    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection, self.configuration)
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_modules.druid_sql.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = {'code': 200, 'message': 'All Good!'}
        mock_ping_response.return_value = mocked_return_value
        entry_point = EntryPoint(self.connection, self.configuration)
        ping_result = entry_point.ping_connection()
        assert ping_result['success'] is True

    @patch('stix_shifter_modules.druid_sql.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_failure(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = {'code': 502, 'message': 'Connection error'}
        mock_ping_response.return_value = mocked_return_value
        entry_point = EntryPoint(self.connection, self.configuration)
        ping_response = entry_point.ping_connection()
        assert ping_response['success'] is False
        assert ping_response['code'] == ErrorCode.TRANSMISSION_REMOTE_SYSTEM_IS_UNAVAILABLE.value

    @patch('stix_shifter_modules.druid_sql.stix_transmission.api_client.APIClient.run_search')
    def test_results_reponse(self, mock_query, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = {'code': 200, 'result': {'_0': '2015-09-12T00:46:58.771Z', 'added': 36, 'channel': '#en.wikipedia', 'cityName': '',
        'comment': 'added project', 'countryIsoCode': '', 'countryName': '', 'deleted': 0, 'delta': 36, 'isAnonymous': 'false',
        'isMinor': 'false', 'isNew': 'false', 'isRobot': 'false', 'isUnpatrolled': 'false', 'metroCode': '', 'namespace': 'Talk',
         'page': 'Talk:Oswald Tilghman', 'regionIsoCode': '', 'regionName': '', 'user': 'GELongstreet'}}
        mock_query.return_value = mocked_return_value
        transmission = stix_transmission.StixTransmission('druid_sql', self.connection, self.configuration)
        results_response = transmission.results('query', 0, 1)
        assert results_response['success'] is True
        assert results_response['data'] == mocked_return_value['result']

    @patch('stix_shifter_modules.druid_sql.stix_transmission.api_client.APIClient.run_search')
    def test_results_failure(self, mock_query, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = {'code': 500, 'message': 'Query error'}
        mock_query.return_value = mocked_return_value
        transmission = stix_transmission.StixTransmission('druid_sql', self.connection, self.configuration)
        results_response = transmission.results('query', 0, 1)
        assert results_response['success'] is False
        assert results_response['code'] == ErrorCode.TRANSMISSION_QUERY_PARSING_ERROR.value

    def test_status(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission('druid_sql', self.connection, self.configuration)
        status_response = transmission.status('search_id')
        self.assertTrue(status_response['success'])
        self.assertEqual(status_response['status'], 'COMPLETED')
        self.assertEqual(status_response['progress'], 100)

    def test_delete(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission('druid_sql', self.connection, self.configuration)
        delete_response = transmission.delete('search_id')
        self.assertTrue(delete_response['success'])
