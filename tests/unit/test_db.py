import pytest
from pytest_httpserver import HTTPServer

from relaxed import AllowedKeys, CouchDB, CouchError, InvalidKeysException
from relaxed.server import Server


@pytest.fixture
def httpserver_listen_address():
    return ("127.0.0.1", 8000)


@pytest.fixture(autouse=True)
def setup():
  """ setup any state specific to the execution of the given module."""
  global couch
  couch = CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000, db='_local')
  yield

def test_get_doc_info(httpserver: HTTPServer):
  expected = 'revidhere'

  httpserver.expect_request("/_local/testdoc",  method="HEAD").respond_with_json({}, headers={'ETag': 'revidhere'})
  response = couch.db.get_doc_info(uri_segments={'docid': 'testdoc'})

  assert response == expected
