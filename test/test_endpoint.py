import pytest
import requests

BASE_URL = "http://localhost:8000"
ENDPOINT = BASE_URL + "/run"
TEST_APP = "speedtest.apk"

class TestEndpoint(object):

    @pytest.mark.parametrize("endpoint", [BASE_URL])
    def test_endpointIsUp(self, endpoint):
        assert requests.get(endpoint).status_code == 200


    @pytest.mark.parametrize("endpoint", [BASE_URL])
    def test_retreiveEndpointData(self, endpoint):
        assert len(requests.get(endpoint).json()['available_apks']) > 0


    @pytest.mark.parametrize("endpoint, app", [(ENDPOINT, TEST_APP)])
    def test_endpointRun(self, endpoint, app):
        response = requests.get(endpoint, params={"name" : app}).json()
        assert response['installation_status'] == "Success"
        assert response['running_status'] == "Success"
        assert "Error" not in response["screenshot_status"]