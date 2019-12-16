import pytest
from pytest_httpserver import HTTPServer

from relaxed import CouchDB

@pytest.fixture
def httpserver_listen_address():
    return ("127.0.0.1", 8000)

def test_get_info(httpserver: HTTPServer):
  expected_json = {
    "couchdb": "Welcome",
    "uuid": "85fb71bf700c17267fef77535820e371",
    "vendor": {
        "name": "The Apache Software Foundation",
        "version": "1.3.1"
    },
    "version": "1.3.1"}

  httpserver.expect_request("/",  method="GET").respond_with_json(expected_json)
  couch = CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000)
  response = couch.server.get_info()

  assert response == expected_json
