import  couchapy
from    couchapy.decorators import AllowedKeys
import  pytest
import  pytest_httpserver as test_server


@pytest.fixture
def httpserver_listen_address():
    return ("127.0.0.1", 8000)


@pytest.fixture(autouse=True)
def setup():
    """ setup any state specific to the execution of the given module."""
    global couch
    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000, db='_local')
    yield


def test_get_doc_info(httpserver: test_server.HTTPServer):
    expected = 'revidhere'

    httpserver.expect_request("/_local/testdoc", method="HEAD").respond_with_json({}, headers={'ETag': 'revidhere'})
    response = couch.db.get_doc_info(uri_segments={'docid': 'testdoc'})

    assert response == expected
