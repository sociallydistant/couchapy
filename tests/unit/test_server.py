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
  couch = CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000)
  yield


def test_instanced_class_without_args_has_correct_properties(httpserver: HTTPServer):
  server = Server()



  assert server.session is None
  assert server._predefined_segments == {'node_name': '_local'}


def test_instanced_class_with_args_has_correct_properties(httpserver: HTTPServer):
  from relaxed.session import Session
  session = Session()
  server = Server(session=session)

  assert server.session is session
  assert server._predefined_segments == {'node_name': '_local'}


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
  response = couch.server.get_info()

  assert response == expected_json


def test_get_server_status(httpserver: HTTPServer):
  expected_json = {"status": "ok"}

  httpserver.expect_oneshot_request("/_up",  method="GET").respond_with_json(expected_json)
  response = couch.server.get_server_status()

  assert response == expected_json

  httpserver.expect_oneshot_request("/_up",  method="GET").respond_with_json({}, status=404)
  response = couch.server.get_server_status()
  assert isinstance(response, CouchError) is True
  assert response.status_code == 404


def test_get_active_tasks(httpserver: HTTPServer):
  expected_json = [
    {
        "changes_done": 64438,
        "database": "mailbox",
        "pid": "<0.12986.1>",
        "progress": 84,
        "started_on": 1376116576,
        "total_changes": 76215,
        "type": "database_compaction",
        "updated_on": 1376116619
    }]

  httpserver.expect_oneshot_request("/_active_tasks",  method="GET").respond_with_json(expected_json)
  response = couch.server.get_active_tasks()
  assert response == expected_json

  httpserver.expect_oneshot_request("/_active_tasks",  method="GET").respond_with_json({}, status=401)
  response = couch.server.get_active_tasks()
  assert isinstance(response, CouchError) is True
  assert response.status_code == 401


def test_get_database_names_without_params(httpserver: HTTPServer):
  expected_json = ["_users", "contacts", "docs", "invoices", "locations"]
  httpserver.expect_oneshot_request("/_all_dbs",  method="GET").respond_with_json(expected_json)
  response = couch.server.get_database_names()
  assert response == expected_json


def test_get_database_names_with_params(httpserver: HTTPServer):
  expected_json = ["_users", "contacts", "docs", "invoices", "locations"]
  httpserver.expect_request("/_all_dbs",  method="GET").respond_with_json(expected_json)

  for k in AllowedKeys.SERVER__ALL_DBS__PARAMS:
    response = couch.server.get_database_names(params={k: ''})
    assert isinstance(response, CouchError) is False

  with pytest.raises(InvalidKeysException):
    couch.server.get_database_names(params={'nonexisting_key': ''})


def test_get_databases_without_params(httpserver: HTTPServer):
  expected_json = []
  httpserver.expect_oneshot_request("/_dbs_info",  method="POST").respond_with_json(expected_json)
  response = couch.server.get_databases()
  assert response == expected_json


def test_get_databases_with_params(httpserver: HTTPServer):
  expected_json = ["_users", "contacts", "docs", "invoices", "locations"]
  httpserver.expect_request("/_dbs_info",  method="POST").respond_with_json(expected_json)

  for k in AllowedKeys.SERVER__DBS_INFO__PARAMS:
    response = couch.server.get_databases(data={k: ['test']})
    assert isinstance(response, CouchError) is False

  with pytest.raises(InvalidKeysException):
    couch.server.get_databases(data={'nonexisting_key': ''})


def test_get_databases_with_400_response_from_couch(httpserver: HTTPServer):
  httpserver.expect_request("/_dbs_info",  method="POST").respond_with_json({}, status=400)
  response = couch.server.get_databases(data={'keys': []})
  assert isinstance(response, CouchError) is True
  assert response.status_code == 400


def test_get_cluster_setup_with_params(httpserver: HTTPServer):
  expected_json = {"state": "cluster_enabled"}
  httpserver.expect_request("/_cluster_setup",  method="GET").respond_with_json(expected_json)

  for k in AllowedKeys.SERVER__CLUSTER_SETUP__PARAMS:
    response = couch.server.get_cluster_setup(query={k: ['test']})
    assert isinstance(response, CouchError) is False

  with pytest.raises(InvalidKeysException):
    couch.server.get_cluster_setup(params={'nonexisting_key': ''})

def test_configure_cluster_setup_with_params(httpserver: HTTPServer):
  expected_json = {"state": "cluster_finished"}
  httpserver.expect_request("/_cluster_setup",  method="POST").respond_with_json(expected_json)

  for k in AllowedKeys.SERVER__CLUSTER_SETUP__DATA:
    response = couch.server.configure_cluster_setup(data={k: ['test']})
    assert isinstance(response, CouchError) is False

  with pytest.raises(InvalidKeysException):
    couch.server.configure_cluster_setup(data={'nonexisting_key': ''})
