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
    response = couch.server.get_cluster_setup(params={k: ['test']})
    assert isinstance(response, CouchError) is False

  with pytest.raises(InvalidKeysException):
    couch.server.get_cluster_setup(params={'nonexisting_key': ''})


def test_get_database_updates(httpserver: HTTPServer):
  expected_json = {
    "results": [
      {
        "db_name": "mailbox",
        "type": "created",
        "seq": "1-g1AAAAFReJzLYWBg4MhgTmHgzcvPy09JdcjLz8gvLskBCjMlMiTJ____PyuDOZExFyjAnmJhkWaeaIquGIf2JAUgmWQPMiGRAZcaB5CaePxqEkBq6vGqyWMBkgwNQAqobD4h"},
      {
        "db_name": "mailbox",
        "type": "deleted",
        "seq": "2-g1AAAAFReJzLYWBg4MhgTmHgzcvPy09JdcjLz8gvLskBCjMlMiTJ____PyuDOZEpFyjAnmJhkWaeaIquGIf2JAUgmWQPMiGRAZcaB5CaePxqEkBq6vGqyWMBkgwNQAqobD4hdQsg6vYTUncAou4-IXUPIOpA7ssCAIFHa60"}
      ],
    "last_seq": "2-g1AAAAFReJzLYWBg4MhgTmHgzcvPy09JdcjLz8gvLskBCjMlMiTJ____PyuDOZEpFyjAnmJhkWaeaIquGIf2JAUgmWQPMiGRAZcaB5CaePxqEkBq6vGqyWMBkgwNQAqobD4hdQsg6vYTUncAou4-IXUPIOpA7ssCAIFHa60"
    }

  httpserver.expect_oneshot_request("/_db_updates",  method="POST").respond_with_json(expected_json)
  response = couch.server.get_database_updates()
  assert response == expected_json

  httpserver.expect_oneshot_request("/_db_updates",  method="POST").respond_with_json({}, status=401)
  response = couch.server.get_database_updates()
  assert isinstance(response, CouchError) is True
  assert response.status_code == 401

  httpserver.expect_request("/_db_updates",  method="POST").respond_with_json({})
  for k in AllowedKeys.SERVER__DB_UPDATES__PARAMS:
    response = couch.server.get_database_updates(params={k: ['test']})
    assert isinstance(response, CouchError) is False

  with pytest.raises(InvalidKeysException):
    couch.server.get_database_updates(params={'nonexisting_key': ''})


def test_get_membership(httpserver: HTTPServer):
  expected_json = {
    "all_nodes": [
        "node1@127.0.0.1",
        "node2@127.0.0.1",
        "node3@127.0.0.1"
    ],
    "cluster_nodes": [
        "node1@127.0.0.1",
        "node2@127.0.0.1",
        "node3@127.0.0.1"
    ]
  }

  httpserver.expect_oneshot_request("/_membership",  method="GET").respond_with_json(expected_json)
  response = couch.server.get_membership()
  assert response == expected_json


def test_replicate(httpserver: HTTPServer):
  expected_json = {
    "history": [
        {
            "doc_write_failures": 0,
            "docs_read": 10,
            "docs_written": 10,
            "end_last_seq": 28,
            "end_time": "Sun, 11 Aug 2013 20:38:50 GMT",
            "missing_checked": 10,
            "missing_found": 10,
            "recorded_seq": 28,
            "session_id": "142a35854a08e205c47174d91b1f9628",
            "start_last_seq": 1,
            "start_time": "Sun, 11 Aug 2013 20:38:50 GMT"
        },
        {
            "doc_write_failures": 0,
            "docs_read": 1,
            "docs_written": 1,
            "end_last_seq": 1,
            "end_time": "Sat, 10 Aug 2013 15:41:54 GMT",
            "missing_checked": 1,
            "missing_found": 1,
            "recorded_seq": 1,
            "session_id": "6314f35c51de3ac408af79d6ee0c1a09",
            "start_last_seq": 0,
            "start_time": "Sat, 10 Aug 2013 15:41:54 GMT"
        }
    ],
    "ok": True,
    "replication_id_version": 3,
    "session_id": "142a35854a08e205c47174d91b1f9628",
    "source_last_seq": 28
  }

  httpserver.expect_oneshot_request("/_replicate",  method="POST").respond_with_json(expected_json)
  response = couch.server.replicate()
  assert response == expected_json

  for code in [202]:
    httpserver.expect_oneshot_request("/_replicate",  method="POST").respond_with_json({}, status=code)
    response = couch.server.replicate()
    assert isinstance(response, CouchError) is False

  for code in [400, 401, 404, 500]:
    httpserver.expect_oneshot_request("/_replicate",  method="POST").respond_with_json({}, status=code)
    response = couch.server.replicate()
    assert isinstance(response, CouchError) is True

  httpserver.expect_request("/_replicate",  method="POST").respond_with_json({})
  for k in AllowedKeys.SERVER__REPLICATE__DATA:
    response = couch.server.replicate(data={k: ['test']})
    assert isinstance(response, CouchError) is False

  with pytest.raises(InvalidKeysException):
    couch.server.replicate(data={'nonexisting_key': ''})


def test_get_replication_updates(httpserver: HTTPServer):
  expected_json = {
    "jobs": [
        {
            "database": "_replicator",
            "doc_id": "cdyno-0000001-0000003",
            "history": [
                {
                    "timestamp": "2017-04-29T05:01:37Z",
                    "type": "started"
                },
                {
                    "timestamp": "2017-04-29T05:01:37Z",
                    "type": "added"
                }
            ],
            "id": "8f5b1bd0be6f9166ccfd36fc8be8fc22+continuous",
            "node": "node1@127.0.0.1",
            "pid": "<0.1850.0>",
            "source": "http://myserver.com/foo",
            "start_time": "2017-04-29T05:01:37Z",
            "target": "http://adm:*****@localhost:15984/cdyno-0000003/",
            "user": None
        }
    ],
    "offset": 0,
    "total_rows": 1
  }

  httpserver.expect_oneshot_request("/_scheduler/jobs",  method="GET").respond_with_json(expected_json)
  response = couch.server.get_replication_updates()
  assert response == expected_json

  for code in [401]:
    httpserver.expect_oneshot_request("/_scheduler/jobs",  method="GET").respond_with_json({}, status=code)
    response = couch.server.get_replication_updates()
    assert isinstance(response, CouchError) is True

  httpserver.expect_request("/_scheduler/jobs",  method="GET").respond_with_json({})
  for k in AllowedKeys.SERVER__SCHEDULER_JOBS__PARAMS:
    response = couch.server.get_replication_updates(params={k: ['test']})
    assert isinstance(response, CouchError) is False

  with pytest.raises(InvalidKeysException):
    couch.server.get_replication_updates(params={'nonexisting_key': ''})


def test_get_replication_docs(httpserver: HTTPServer):
  expected_json = {
    "docs": [
        {
            "database": "_replicator",
            "doc_id": "cdyno-0000001-0000002",
            "error_count": 0,
            "id": "e327d79214831ca4c11550b4a453c9ba+continuous",
            "info": None,
            "last_updated": "2017-04-29T05:01:37Z",
            "node": "node2@127.0.0.1",
            "proxy": None,
            "source": "http://myserver.com/foo",
            "start_time": "2017-04-29T05:01:37Z",
            "state": "running",
            "target": "http://adm:*****@localhost:15984/cdyno-0000002/"
        }
    ],
    "offset": 0,
    "total_rows": 1
}

  httpserver.expect_oneshot_request("/_scheduler/docs",  method="GET").respond_with_json(expected_json)
  response = couch.server.get_replication_docs()
  assert response == expected_json

  for code in [401]:
    httpserver.expect_oneshot_request("/_scheduler/docs",  method="GET").respond_with_json({}, status=code)
    response = couch.server.get_replication_docs()
    assert isinstance(response, CouchError) is True

  httpserver.expect_request("/_scheduler/docs",  method="GET").respond_with_json({})
  for k in AllowedKeys.SERVER__SCHEDULER_DOCS__PARAMS:
    response = couch.server.get_replication_docs(params={k: ['test']})
    assert isinstance(response, CouchError) is False

  with pytest.raises(InvalidKeysException):
    couch.server.get_replication_docs(params={'nonexisting_key': ''})


def test_get_replicator_docs(httpserver: HTTPServer):
  expected_json = {
    "docs": [
        {
            "database": "other/_replicator",
            "doc_id": "cdyno-0000001-0000002",
            "error_count": 0,
            "id": "e327d79214831ca4c11550b4a453c9ba+continuous",
            "info": None,
            "last_updated": "2017-04-29T05:01:37Z",
            "node": "node2@127.0.0.1",
            "proxy": None,
            "source": "http://myserver.com/foo",
            "start_time": "2017-04-29T05:01:37Z",
            "state": "running",
            "target": "http://adm:*****@localhost:15984/cdyno-0000002/"
        }
    ],
    "offset": 0,
    "total_rows": 1
  }

  httpserver.expect_oneshot_request("/_scheduler/docs/other/_replicator",  method="GET").respond_with_json(expected_json)
  response = couch.server.get_replicator_docs(uri_segments={'db': 'other'})
  assert response == expected_json

  for code in [401]:
    httpserver.expect_oneshot_request("/_scheduler/docs/other/_replicator",  method="GET").respond_with_json({}, status=code)
    response = couch.server.get_replicator_docs(uri_segments={'db': 'other'})
    assert isinstance(response, CouchError) is True

  httpserver.expect_request("/_scheduler/docs/other/_replicator",  method="GET").respond_with_json({})
  for k in AllowedKeys.SERVER__SCHEDULER_DOCS__PARAMS:
    response = couch.server.get_replicator_docs(uri_segments={'db': 'other'}, params={k: ['test']})
    assert isinstance(response, CouchError) is False

  with pytest.raises(InvalidKeysException):
    couch.server.get_replicator_docs(uri_segments={'db': 'other'}, params={'nonexisting_key': ''})


def test_get_replicator_doc(httpserver: HTTPServer):
  expected_json = {
    "database": "other/_replicator",
    "doc_id": "cdyno-0000001-0000002",
    "error_count": 0,
    "id": "e327d79214831ca4c11550b4a453c9ba+continuous",
    "info": None,
    "last_updated": "2017-04-29T05:01:37Z",
    "node": "node2@127.0.0.1",
    "proxy": None,
    "source": "http://myserver.com/foo",
    "start_time": "2017-04-29T05:01:37Z",
    "state": "running",
    "target": "http://adm:*****@localhost:15984/cdyno-0000002/"
  }

  httpserver.expect_oneshot_request("/_scheduler/docs/other/_replicator/replication-doc-id",  method="GET").respond_with_json(expected_json)
  response = couch.server.get_replicator_doc(uri_segments={'db': 'other', 'docid': 'replication-doc-id'})
  assert response == expected_json

  for code in [401]:
    httpserver.expect_oneshot_request("/_scheduler/docs/other/_replicator/replication-doc-id",  method="GET").respond_with_json({}, status=code)
    response = couch.server.get_replicator_doc(uri_segments={'db': 'other', 'docid': 'replication-doc-id'})
    assert isinstance(response, CouchError) is True
