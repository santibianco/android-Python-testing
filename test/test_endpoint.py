import pytest
import requests

class TestEndpoint(object):

    @pytest.mark.parametrize("endpoint", ["http://localhost:8000/run"])
    def test_retreiveEndpointData(self, endpoint):
        response = requests.get(endpoint)
        assert response.status_code == 200
        assert response.json()['current_url'] == "/run"