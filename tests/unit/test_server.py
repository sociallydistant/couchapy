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
    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000)
    yield


def test_instanced_class_without_args_has_correct_properties(httpserver: test_server.HTTPServer):
    server = couch.server
    assert server.parent is not None
    assert server._predefined_segments == {'node_name': '_local'}


def test_instanced_class_with_args_has_correct_properties(httpserver: test_server.HTTPServer):
    server = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000,
                              server_kwargs={'predefined_segments': {'node_name': 'test'}}).server

    assert 'node_name' in server._predefined_segments and server._predefined_segments['node_name'] == 'test'


def test_get_info(httpserver: test_server.HTTPServer):
    expected_json = {
        "couchdb": "Welcome",
        "uuid": "85fb71bf700c17267fef77535820e371",
        "vendor": {
            "name": "The Apache Software Foundation",
            "version": "1.3.1"
        },
        "version": "1.3.1"
    }

    httpserver.expect_request("/", method="GET").respond_with_json(expected_json)
    response = couch.server.info()

    assert response == expected_json


def test_get_server_status(httpserver: test_server.HTTPServer):
    expected_json = {"status": "ok"}

    httpserver.expect_oneshot_request("/_up", method="GET").respond_with_json(expected_json)
    response = couch.server.server_status()

    assert response == expected_json

    httpserver.expect_oneshot_request("/_up", method="GET").respond_with_json({}, status=404)
    response = couch.server.server_status()
    assert isinstance(response, couchapy.CouchError) is True
    assert response.status_code == 404


def test_get_active_tasks(httpserver: test_server.HTTPServer):
    expected_json = [{
        "changes_done": 64438,
        "database": "mailbox",
        "pid": "<0.12986.1>",
        "progress": 84,
        "started_on": 1376116576,
        "total_changes": 76215,
        "type": "database_compaction",
        "updated_on": 1376116619
    }]

    httpserver.expect_oneshot_request("/_active_tasks", method="GET").respond_with_json(expected_json)
    response = couch.server.active_tasks()
    assert response == expected_json

    httpserver.expect_oneshot_request("/_active_tasks", method="GET").respond_with_json({}, status=401)
    response = couch.server.active_tasks()
    assert isinstance(response, couchapy.CouchError) is True
    assert response.status_code == 401


def test_get_database_names_without_params(httpserver: test_server.HTTPServer):
    expected_json = ["_users", "contacts", "docs", "invoices", "locations"]
    httpserver.expect_oneshot_request("/_all_dbs", method="GET").respond_with_json(expected_json)
    response = couch.server.database_names()
    assert response == expected_json


def test_get_database_names_with_params(httpserver: test_server.HTTPServer):
    expected_json = ["_users", "contacts", "docs", "invoices", "locations"]
    httpserver.expect_request("/_all_dbs", method="GET").respond_with_json(expected_json)

    for k in AllowedKeys.SERVER__ALL_DBS__PARAMS:
        response = couch.server.database_names(params={k: ''})
        assert isinstance(response, couchapy.CouchError) is False

    with pytest.raises(couchapy.InvalidKeysException):
        couch.server.database_names(params={'nonexisting_key': ''})


def test_get_databases_without_params(httpserver: test_server.HTTPServer):
    expected_json = []
    httpserver.expect_oneshot_request("/_dbs_info", method="POST").respond_with_json(expected_json)
    response = couch.server.databases()
    assert response == expected_json


def test_get_databases_with_params(httpserver: test_server.HTTPServer):
    expected_json = ["_users", "contacts", "docs", "invoices", "locations"]
    httpserver.expect_request("/_dbs_info", method="POST").respond_with_json(expected_json)

    for k in AllowedKeys.SERVER__DBS_INFO__PARAMS:
        response = couch.server.databases(data={k: ['test']})
        assert isinstance(response, couchapy.CouchError) is False

    with pytest.raises(couchapy.InvalidKeysException):
        couch.server.databases(data={'nonexisting_key': ''})


def test_get_databases_with_400_response_from_couch(httpserver: test_server.HTTPServer):
    httpserver.expect_request("/_dbs_info", method="POST").respond_with_json({}, status=400)
    response = couch.server.databases(data={'keys': []})
    assert isinstance(response, couchapy.CouchError) is True
    assert response.status_code == 400


def test_get_cluster_setup_with_params(httpserver: test_server.HTTPServer):
    expected_json = {"state": "cluster_enabled"}
    httpserver.expect_request("/_cluster_setup", method="GET").respond_with_json(expected_json)

    for k in AllowedKeys.SERVER__CLUSTER_SETUP__PARAMS:
        response = couch.server.cluster_setup(params={k: ['test']})
        assert isinstance(response, couchapy.CouchError) is False

    with pytest.raises(couchapy.InvalidKeysException):
        couch.server.cluster_setup(params={'nonexisting_key': ''})


def test_configure_cluster_setup(httpserver: test_server.HTTPServer):
    expected_json = {"state": "cluster_enabled"}
    httpserver.expect_request("/_cluster_setup", method="POST").respond_with_json(expected_json)

    for k in AllowedKeys.SERVER__CLUSTER_SETUP__DATA:
        response = couch.server.configure_cluster_setup(data={k: ['test']})
        assert isinstance(response, couchapy.CouchError) is False

    with pytest.raises(couchapy.InvalidKeysException):
        couch.server.configure_cluster_setup(data={'nonexisting_key': ''})


def test_get_database_updates(httpserver: test_server.HTTPServer):
    expected_json = {
        "results": [
            {
                "db_name": "mailbox",
                "type": "created",
                "seq": "1-g1AAAAFReJzLYWBg4MhgTmHgzcvPy09JdcjLz8gvLskBCjMlMiTJ____PyuDOZExFyjAnmJhkWaeaIquGIf2JAUgmWQPMiGRAZcaB5CaePxqEkBq6vGqyWMBkgwNQAqobD4h"},
            {
                "db_name": "mailbox",
                "type": "deleted",
                "seq": "2-g1AAAAFReJzLYWBg4MhgTmHgzcvPy09JdcjLz8gvLskBCjMlMiTJ____PyuDOZEpFyjAnmJhkWaeaIquGIf2JAUgmWQPMiGRAZcaB5CaePxqEkBq6vGqyWMBkgwNQAqobD4hdQsg6vYTUncAou4-IXUPIOpA7ssCAIFHa60"
            }
        ],
        "last_seq": "2-g1AAAAFReJzLYWBg4MhgTmHgzcvPy09JdcjLz8gvLskBCjMlMiTJ____PyuDOZEpFyjAnmJhkWaeaIquGIf2JAUgmWQPMiGRAZcaB5CaePxqEkBq6vGqyWMBkgwNQAqobD4hdQsg6vYTUncAou4-IXUPIOpA7ssCAIFHa60"
    }

    httpserver.expect_oneshot_request("/_db_updates", method="POST").respond_with_json(expected_json)
    response = couch.server.database_updates()
    assert response == expected_json

    httpserver.expect_oneshot_request("/_db_updates", method="POST").respond_with_json({}, status=401)
    response = couch.server.database_updates()
    assert isinstance(response, couchapy.CouchError) is True
    assert response.status_code == 401

    httpserver.expect_request("/_db_updates", method="POST").respond_with_json({})
    for k in AllowedKeys.SERVER__DB_UPDATES__PARAMS:
        response = couch.server.database_updates(params={k: ['test']})
        assert isinstance(response, couchapy.CouchError) is False

    with pytest.raises(couchapy.InvalidKeysException):
        couch.server.database_updates(params={'nonexisting_key': ''})


def test_get_membership(httpserver: test_server.HTTPServer):
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

    httpserver.expect_oneshot_request("/_membership", method="GET").respond_with_json(expected_json)
    response = couch.server.memberships()
    assert response == expected_json


def test_replicate(httpserver: test_server.HTTPServer):
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

    httpserver.expect_oneshot_request("/_replicate", method="POST").respond_with_json(expected_json)
    response = couch.server.replicate()
    assert response == expected_json

    for code in [202]:
        httpserver.expect_oneshot_request("/_replicate", method="POST").respond_with_json({}, status=code)
        response = couch.server.replicate()
        assert isinstance(response, couchapy.CouchError) is False

    for code in [400, 401, 404, 500]:
        httpserver.expect_oneshot_request("/_replicate", method="POST").respond_with_json({}, status=code)
        response = couch.server.replicate()
        assert isinstance(response, couchapy.CouchError) is True

    httpserver.expect_request("/_replicate", method="POST").respond_with_json({})
    for k in AllowedKeys.SERVER__REPLICATE__DATA:
        response = couch.server.replicate(data={k: ['test']})
        assert isinstance(response, couchapy.CouchError) is False

    with pytest.raises(couchapy.InvalidKeysException):
        couch.server.replicate(data={'nonexisting_key': ''})


def test_get_replication_updates(httpserver: test_server.HTTPServer):
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

    httpserver.expect_oneshot_request("/_scheduler/jobs", method="GET").respond_with_json(expected_json)
    response = couch.server.replication_updates()
    assert response == expected_json

    for code in [401]:
        httpserver.expect_oneshot_request("/_scheduler/jobs", method="GET").respond_with_json({}, status=code)
        response = couch.server.replication_updates()
        assert isinstance(response, couchapy.CouchError) is True

    httpserver.expect_request("/_scheduler/jobs", method="GET").respond_with_json({})
    for k in AllowedKeys.SERVER__SCHEDULER_JOBS__PARAMS:
        response = couch.server.replication_updates(params={k: ['test']})
        assert isinstance(response, couchapy.CouchError) is False

    with pytest.raises(couchapy.InvalidKeysException):
        couch.server.replication_updates(params={'nonexisting_key': ''})


def test_get_replication_docs(httpserver: test_server.HTTPServer):
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

    httpserver.expect_oneshot_request("/_scheduler/docs", method="GET").respond_with_json(expected_json)
    response = couch.server.replication_docs()
    assert response == expected_json

    for code in [401]:
        httpserver.expect_oneshot_request("/_scheduler/docs", method="GET").respond_with_json({}, status=code)
        response = couch.server.replication_docs()
        assert isinstance(response, couchapy.CouchError) is True

    httpserver.expect_request("/_scheduler/docs", method="GET").respond_with_json({})
    for k in AllowedKeys.SERVER__SCHEDULER_DOCS__PARAMS:
        response = couch.server.replication_docs(params={k: ['test']})
        assert isinstance(response, couchapy.CouchError) is False

    with pytest.raises(couchapy.InvalidKeysException):
        couch.server.replication_docs(params={'nonexisting_key': ''})


def test_get_replicator_docs(httpserver: test_server.HTTPServer):
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

    httpserver.expect_oneshot_request("/_scheduler/docs/other/_replicator", method="GET").respond_with_json(expected_json)
    response = couch.server.replicator_docs(uri_segments={'db': 'other'})
    assert response == expected_json

    for code in [401]:
        httpserver.expect_oneshot_request("/_scheduler/docs/other/_replicator", method="GET").respond_with_json({}, status=code)
        response = couch.server.replicator_docs(uri_segments={'db': 'other'})
        assert isinstance(response, couchapy.CouchError) is True

    httpserver.expect_request("/_scheduler/docs/other/_replicator", method="GET").respond_with_json({})
    for k in AllowedKeys.SERVER__SCHEDULER_DOCS__PARAMS:
        response = couch.server.replicator_docs(uri_segments={'db': 'other'}, params={k: ['test']})
        assert isinstance(response, couchapy.CouchError) is False

    with pytest.raises(couchapy.InvalidKeysException):
        couch.server.replicator_docs(uri_segments={'db': 'other'}, params={'nonexisting_key': ''})


def test_get_replicator_doc(httpserver: test_server.HTTPServer):
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

    httpserver.expect_oneshot_request("/_scheduler/docs/other/_replicator/replication-doc-id", method="GET").respond_with_json(expected_json)
    response = couch.server.replicator_doc(uri_segments={'db': 'other', 'docid': 'replication-doc-id'})
    assert response == expected_json

    for code in [401]:
        httpserver.expect_oneshot_request("/_scheduler/docs/other/_replicator/replication-doc-id", method="GET").respond_with_json({}, status=code)
        response = couch.server.replicator_doc(uri_segments={'db': 'other', 'docid': 'replication-doc-id'})
        assert isinstance(response, couchapy.CouchError) is True


def test_get_node_server_stats(httpserver: test_server.HTTPServer):
    expected_json = {
        "value": {
            "min": 0,
            "max": 0,
            "arithmetic_mean": 0,
            "geometric_mean": 0,
            "harmonic_mean": 0,
            "median": 0,
            "variance": 0,
            "standard_deviation": 0,
            "skewness": 0,
            "kurtosis": 0,
            "percentile": [[50, 0], [75, 0], [90, 0], [95, 0], [99, 0], [999, 0]],
            "histogram": [[0, 0]],
            "n": 0
        },
        "type": "histogram",
        "desc": "length of a request inside CouchDB without MochiWeb"
    }

    httpserver.expect_request("/_node/_local/_stats", method="GET").respond_with_json(expected_json)
    response = couch.server.node_stats(uri_segments={'node_name': '_local'})
    assert response == expected_json

    response = couch.server.node_stats()
    assert response == expected_json


def test_get_node_server_stat(httpserver: test_server.HTTPServer):
    expected_json = {
        "value": {
            "min": 0,
            "max": 0,
            "arithmetic_mean": 0,
            "geometric_mean": 0,
            "harmonic_mean": 0,
            "median": 0,
            "variance": 0,
            "standard_deviation": 0,
            "skewness": 0,
            "kurtosis": 0,
            "percentile": [[50, 0], [75, 0], [90, 0], [95, 0], [99, 0], [999, 0]],
            "histogram": [[0, 0]],
            "n": 0
        },
        "type": "histogram",
        "desc": "length of a request inside CouchDB without MochiWeb"
    }

    httpserver.expect_request("/_node/_local/_stats/couchdb/request_time", method="GET").respond_with_json(expected_json)
    response = couch.server.node_stat(uri_segments={'node_name': '_local', 'stat': 'couchdb/request_time'})
    assert response == expected_json

    response = couch.server.node_stat()
    assert response == expected_json


def test_get_node_system_stats(httpserver: test_server.HTTPServer):
    expected_json = {"uptime": 259, "memory": 1000}

    httpserver.expect_request("/_node/_local/_system", method="GET").respond_with_json(expected_json)
    response = couch.server.node_system_stats(uri_segments={'node_name': '_local'})
    assert response == expected_json

    response = couch.server.node_system_stats()
    assert response == expected_json


def test_restart_node(httpserver: test_server.HTTPServer):
    expected_json = {}

    httpserver.expect_request("/_node/_local/_restart", method="POST").respond_with_json(expected_json)
    response = couch.server.restart_node(uri_segments={'node_name': '_local'})
    assert isinstance(response, couchapy.CouchError) is False


def test_get_node_config(httpserver: test_server.HTTPServer):
    expected_json = {
        "attachments": {
            "compressible_types": "text/*, application/javascript, application/json,  application/xml",
            "compression_level": "8"
        },
        "couchdb": {
            "users_db_suffix": "_users",
            "database_dir": "/var/lib/couchdb",
            "delayed_commits": "true",
            "max_attachment_chunk_size": "4294967296",
            "max_dbs_open": "100",
            "os_process_timeout": "5000",
            "uri_file": "/var/lib/couchdb/couch.uri",
            "util_driver_dir": "/usr/lib64/couchdb/erlang/lib/couch-1.5.0/priv/lib",
            "view_index_dir": "/var/lib/couchdb"
        },
        "chttpd": {
            "backlog": "512",
            "bind_address": "0.0.0.0",
            "docroot": "./share/www",
            "port": "5984",
            "require_valid_user": "false",
            "socket_options": "[{sndbuf, 262144}, {nodelay, true}]",
            "server_options": "[{recbuf, undefined}]"
        },
        "httpd": {
            "allow_jsonp": "false",
            "authentication_handlers": "{couch_httpd_auth, cookie_authentication_handler}, {couch_httpd_auth, default_authentication_handler}",
            "bind_address": "192.168.0.2",
            "max_connections": "2048",
            "port": "5984",
            "secure_rewrites": "true"
        },
        "log": {"writer": "file", "file": "/var/log/couchdb/couch.log", "include_sasl": "true", "level": "info"},
        "query_server_config": {"reduce_limit": "true"},
        "replicator": {"max_http_pipeline_size": "10", "max_http_sessions": "10"},
        "stats": {"rate": "1000", "samples": "[0, 60, 300, 900]"},
        "uuids": {"algorithm": "utc_random"}
    }

    httpserver.expect_oneshot_request("/_node/_local/_config", method="GET").respond_with_json(expected_json)
    response = couch.server.node_config(uri_segments={'node_name': '_local'})
    assert response == expected_json

    for code in [401]:
        httpserver.expect_oneshot_request("/_node/_local/_config", method="GET").respond_with_json({}, status=code)
        response = couch.server.node_config(uri_segments={'node_name': '_local'})
        assert isinstance(response, couchapy.CouchError) is True


def test_get_config(httpserver: test_server.HTTPServer):
    expected_json = {
        "httpd": {
            "allow_jsonp": "false",
            "authentication_handlers": "{couch_httpd_auth, cookie_authentication_handler}, {couch_httpd_auth, default_authentication_handler}",
            "bind_address": "192.168.0.2",
            "max_connections": "2048",
            "port": "5984",
            "secure_rewrites": "true"
        }
    }

    httpserver.expect_oneshot_request("/_node/_local/_config/httpd", method="GET").respond_with_json(expected_json)
    response = couch.server.node_setting(uri_segments={'node_name': '_local', 'key': 'httpd'})
    assert response == expected_json

    for code in [401]:
        httpserver.expect_oneshot_request("/_node/_local/_config/httpd", method="GET").respond_with_json({}, status=code)
        response = couch.server.node_setting(uri_segments={'node_name': '_local', 'key': 'httpd'})
        assert isinstance(response, couchapy.CouchError) is True


def test_set_node_config(httpserver: test_server.HTTPServer):
    expected_json = {'data': "5984"}

    httpserver.expect_oneshot_request("/_node/_local/_config/httpd/port", method="PUT").respond_with_json(expected_json)
    response = couch.server.set_node_config(uri_segments={'node_name': '_local', 'key': 'httpd/port'}, data="5984")
    assert response == expected_json

    for code in [400, 401, 500]:
        httpserver.expect_oneshot_request("/_node/_local/_config/httpd/port", method="PUT").respond_with_json(expected_json, status=code)
        response = couch.server.set_node_config(uri_segments={'node_name': '_local', 'key': 'httpd/port'}, data="5984")
        assert isinstance(response, couchapy.CouchError) is True


def test_delete_node_config(httpserver: test_server.HTTPServer):
    expected_json = {'data': "5984"}

    httpserver.expect_oneshot_request("/_node/_local/_config/httpd/port", method="DELETE").respond_with_json(expected_json)
    response = couch.server.delete_node_config(uri_segments={'node_name': '_local', 'key': 'httpd/port'})
    assert response == expected_json

    for code in [400, 401]:
        httpserver.expect_oneshot_request("/_node/_local/_config/httpd/port", method="DELETE").respond_with_json(expected_json, status=code)
        response = couch.server.delete_node_config(uri_segments={'node_name': '_local', 'key': 'httpd/port'})
        assert isinstance(response, couchapy.CouchError) is True


def test_generate_uiids(httpserver: test_server.HTTPServer):
    expected_json = {
        "uuids": [
            "75480ca477454894678e22eec6002413",
            "75480ca477454894678e22eec600250b",
            "75480ca477454894678e22eec6002c41",
            "75480ca477454894678e22eec6003b90",
            "75480ca477454894678e22eec6003fca",
            "75480ca477454894678e22eec6004bef",
            "75480ca477454894678e22eec600528f",
            "75480ca477454894678e22eec6005e0b",
            "75480ca477454894678e22eec6006158",
            "75480ca477454894678e22eec6006161"
        ]
    }

    httpserver.expect_oneshot_request("/_uuids", method="GET").respond_with_json(expected_json)
    response = couch.server.generate_uuids()
    assert response == expected_json['uuids']

    expected_json = {"uuids": ["75480ca477454894678e22eec6002413"]}
    httpserver.expect_oneshot_request("/_uuids", method="GET").respond_with_json(expected_json)
    response = couch.server.generate_uuids()
    assert response == expected_json['uuids'][0]

    for code in [400]:
        httpserver.expect_oneshot_request("/_uuids", method="GET").respond_with_json(expected_json, status=code)
        response = couch.server.generate_uuids()
        assert isinstance(response, couchapy.CouchError) is True

    httpserver.expect_request("/_uuids", method="GET").respond_with_json(expected_json)
    for k in AllowedKeys.SERVER__UUIDS__PARAMS:
        response = couch.server.generate_uuids(params={k: ['test']})
        assert isinstance(response, couchapy.CouchError) is False

    with pytest.raises(couchapy.InvalidKeysException):
        couch.server.generate_uuids(params={'nonexisting_key': ''})


def test_get_uptime(httpserver: test_server.HTTPServer):
    expected_json = {"uptime": 259, "memory": 1000}

    httpserver.expect_request("/_node/_local/_system", method="GET").respond_with_json(expected_json)
    response = couch.server.uptime(uri_segments={'node_name': '_local'})
    assert response == expected_json['uptime']
