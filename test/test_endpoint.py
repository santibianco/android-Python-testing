import pytest
import requests

ENDPOINT = "http://localhost:8000/run

class TestEndpoint(object):

    @pytest.mark.parametrize("endpoint", [ENDPOINT])
    def test_endpointIsUp(self, endpoint):
        assert requests.get(endpoint).status_code == 200


    @pytest.mark.parametrize("endpoint", [ENDPOINT])
    def test_retreiveEndpointData(self, endpoint):
        assert requests.get(endpoint).json()['current_url'] == "/run"