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
    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000, database_kwargs={"db": '_local'})
    yield


def test_initializer(httpserver: test_server.HTTPServer):
    assert couch.db.parent == couch
    assert couch.db._db == '_local'
    assert couch.db._predefined_segments == {"db": "_local"}

    couch_without_db_args = couchapy.CouchDB()
    assert couch_without_db_args.db.parent == couch_without_db_args
    assert couch_without_db_args.db._db == '_global_changes'
    assert couch_without_db_args.db._predefined_segments == {"db": "_global_changes"}


def test_headers(httpserver: test_server.HTTPServer):
    expected = {
        "Cache-Control": "must-revalidate",
        "Content-Type": "application/json",
        "Date": "Mon, 12 Aug 2013 01:27:41 GMT",
        "Server": "CouchDB (Erlang/OTP)",
        "Content-Length": "2"
    }

    httpserver.expect_request("/_local", method="HEAD").respond_with_json({}, headers=expected, status=404)
    response = couch.db.headers(uri_segments={'db': '_local'})
    assert response == expected


def test_database_exists(httpserver: test_server.HTTPServer):
    httpserver.expect_request("/_local", method="HEAD").respond_with_json({}, headers={'ETag': 'revidhere'}, status=200)

    # simulate a 404
    httpserver.expect_request("/doesnotexist", method="HEAD").respond_with_json({}, headers={'ETag': 'revidhere'}, status=404)
    response = couch.db.exists(uri_segments={'db': '_local'})
    assert response is True

    response = couch.db.exists(uri_segments={'db': 'doesnotexist'})
    assert response is False

    response = couch.db.exists(uri_segments={'db': 'generateinternalservererror'})
    assert response is False


def test_database_info(httpserver: test_server.HTTPServer):
    expected = {
        "cluster": {
            "n": 3,
            "q": 8,
            "r": 2,
            "w": 2
        },
        "compact_running": False,
        "db_name": "receipts",
        "disk_format_version": 6,
        "doc_count": 6146,
        "doc_del_count": 64637,
        "instance_start_time": "0",
        "props": {},
        "purge_seq": 0,
        "sizes": {
            "active": 65031503,
            "external": 66982448,
            "file": 137433211
        },
        "update_seq": "292786-g1AAAAF..."
    }

    httpserver.expect_request("/_local").respond_with_json(expected)
    response = couch.db.info(uri_segments={'db': '_local'})
    assert response == expected


def test_save_new_doc(httpserver: test_server.HTTPServer):
    expected = {
        "id": "ab39fe0993049b84cfa81acd6ebad09d",
        "ok": True,
        "rev": "1-9c65296036141e575d32ba9c034dd3ee"
    }

    request_data = {
        "servings": 4,
        "subtitle": "Delicious with fresh bread",
        "title": "Fish Stew"
    }

    httpserver.expect_request("/_local", method="POST").respond_with_json(expected)
    response = couch.db.save(uri_segments={'db': '_local'}, data=request_data)
    assert response == expected


def test_delete(httpserver: test_server.HTTPServer):
    expected_json = {"ok": True}

    httpserver.expect_oneshot_request("/somedb", method="DELETE").respond_with_json(expected_json)
    response = couch.server.delete_database(uri_segments={'db': 'somedb'})
    assert response == expected_json

    for code in [202]:
        httpserver.expect_oneshot_request("/somedb", method="DELETE").respond_with_json({}, status=code)
        response = couch.server.delete_database()
        assert isinstance(response, couchapy.CouchError) is False

    for code in [400, 401, 404, 500]:
        httpserver.expect_oneshot_request("/somedb", method="DELETE").respond_with_json({}, status=code)
        response = couch.server.delete_database()
        assert isinstance(response, couchapy.CouchError) is True


def test_flush(httpserver: test_server.HTTPServer):
    expected = {
        "instance_start_time": "0",
        "ok": True
    }

    httpserver.expect_request("/_local/_ensure_full_commit", method="POST").respond_with_json(expected)
    response = couch.db.flush(uri_segments={'db': '_local'})
    assert response == expected


def test_purge(httpserver: test_server.HTTPServer):
    expected = {
        "purge_seq": None,
        "purged": {
            "c6114c65e295552ab1019e2b046b10e": {
                "purged": ["3-c50a32451890a3f1c3e423334cc92745"]
            }
        }
    }

    request_data = {
        "c6114c65e295552ab1019e2b046b10e": [
            "3-b06fcd1c1c9e0ec7c480ee8aa467bf3b",
            "3-c50a32451890a3f1c3e423334cc92745"
        ]
    }

    httpserver.expect_request("/_local/_purge", method="POST").respond_with_json(expected)
    response = couch.db.purge(uri_segments={'db': '_local'}, data=request_data)
    assert response == expected


def test_get_purge_limit(httpserver: test_server.HTTPServer):
    expected = 1000

    httpserver.expect_request("/_local/_purged_infos_limit").respond_with_data("1000")
    response = couch.db.get_purge_limit(uri_segments={'db': '_local'})
    assert response == expected


def test_set_purge_limit(httpserver: test_server.HTTPServer):
    expected = {"ok": True}

    httpserver.expect_request("/_local/_purged_infos_limit", method="PUT").respond_with_json(expected)
    response = couch.db.set_purge_limit(uri_segments={'db': '_local'}, data=1000)
    assert response == expected


def test_compact(httpserver: test_server.HTTPServer):
    expected = {"ok": True}

    httpserver.expect_request("/_local/_compact", method="POST").respond_with_json(expected)
    response = couch.db.compact(uri_segments={'db': '_local'})
    assert response == expected


def test_get_doc_info(httpserver: test_server.HTTPServer):
    expected = 'revidhere'

    httpserver.expect_request("/_local/testdoc", method="HEAD").respond_with_json({}, headers={'ETag': 'revidhere'})
    response = couch.db.get_doc_info(uri_segments={'docid': 'testdoc'})

    assert response == expected
