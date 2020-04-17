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
    assert couch.db.revs.parent == couch.db.parent
    assert couch.db.revs._db == couch.db._db
    assert couch.db.revs._predefined_segments == couch.db._predefined_segments

    couch_without_db_args = couchapy.CouchDB()
    assert couch_without_db_args.db.revs.parent == couch_without_db_args.db.parent
    assert couch_without_db_args.db.revs._db == couch_without_db_args.db._db
    assert couch_without_db_args.db.revs._predefined_segments == couch_without_db_args.db._predefined_segments


def test_get_limit(httpserver: test_server.HTTPServer):
    expected = 1000

    httpserver.expect_request("/_local/_revs_limit").respond_with_data("1000")
    response = couch.db.revs.get_limit(uri_segments={'db': '_local'})
    assert response == expected


def test_set_limit(httpserver: test_server.HTTPServer):
    expected = {"ok": True}

    httpserver.expect_request("/_local/_revs_limit", method="PUT").respond_with_json(expected)
    response = couch.db.revs.set_limit(uri_segments={'db': '_local'}, data=1000)
    assert response == expected


def test_diff(httpserver: test_server.HTTPServer):
    expected = {
        "190f721ca3411be7aa9477db5f948bbb": {
            "missing": [
                "3-bb72a7682290f94a985f7afac8b27137",
                "5-067a00dff5e02add41819138abb3284d"
            ],
            "possible_ancestors": [
                "4-10265e5a26d807a3cfa459cf1a82ef2e"
            ]
        }
    }

    request_data = {
        "190f721ca3411be7aa9477db5f948bbb": [
            "3-bb72a7682290f94a985f7afac8b27137",
            "4-10265e5a26d807a3cfa459cf1a82ef2e",
            "5-067a00dff5e02add41819138abb3284d"
        ]
    }

    httpserver.expect_request("/_local/_revs_diff", method="POST").respond_with_json(expected)
    response = couch.db.revs.diff(uri_segments={'db': '_local'}, data=request_data)
    assert response == expected


def test_missing(httpserver: test_server.HTTPServer):
    expected = {
        "missed_revs": {
            "c6114c65e295552ab1019e2b046b10e": [
                "3-b06fcd1c1c9e0ec7c480ee8aa467bf3b"
            ]
        }
    }

    request_data = {
        "c6114c65e295552ab1019e2b046b10e": [
            "3-b06fcd1c1c9e0ec7c480ee8aa467bf3b",
            "3-0e871ef78849b0c206091f1a7af6ec41"
        ]
    }

    httpserver.expect_request("/_local/_missing_revs", method="POST").respond_with_json(expected)
    response = couch.db.revs.missing(uri_segments={'db': '_local'}, data=request_data)
    assert response == expected
