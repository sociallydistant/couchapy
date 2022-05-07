import  couchapy
import  pytest
import  pytest_httpserver as test_server
import  requests
from    werkzeug.wrappers.response import Response


@pytest.fixture(autouse=True)
def setup():
    """ setup any state specific to the execution of the given module."""
    global couch
    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000, database_kwargs={"db": '_local'})
    yield


def test_initializer(httpserver: test_server.HTTPServer):
    assert couch.db.design.parent == couch.db.parent
    assert couch.db.design._db == couch.db._db
    assert couch.db.design._predefined_segments == couch.db._predefined_segments

    couch_without_db_args = couchapy.CouchDB()
    assert couch_without_db_args.db.design.parent == couch_without_db_args.db.parent
    assert couch_without_db_args.db.design._db == couch_without_db_args.db._db
    assert couch_without_db_args.db.design._predefined_segments == couch_without_db_args.db._predefined_segments


def test_queries(httpserver: test_server.HTTPServer):
    expected = {
        "results": [
            {
                "offset": 0,
                "rows": [
                    {"id": "SpaghettiWithMeatballs", "key": "meatballs", "value": 1},
                    {"id": "SpaghettiWithMeatballs", "key": "spaghetti", "value": 1},
                    {"id": "SpaghettiWithMeatballs", "key": "tomato sauce", "value": 1}
                ],
                "total_rows": 3
            }
        ]
    }

    request_data = {
        "queries": [
            {"keys": ["meatballs", "spaghetti"]},
            {"limit": 3, "skip": 2}
        ]
    }

    httpserver.expect_request("/_local/_design_docs/queries", method="POST").respond_with_json(expected)
    response = couch.db.design.queries(uri_segments={'db': '_local', 'docid': 'id'}, data=request_data)
    assert response == expected


def test_compact(httpserver: test_server.HTTPServer):
    expected = {"ok": True}

    httpserver.expect_request("/_local/_compact/ddoc_name", method="POST").respond_with_json(expected)
    response = couch.db.design.compact(uri_segments={'db': '_local', 'ddoc': 'ddoc_name'})
    assert response == expected


def test_get_by_post(httpserver: test_server.HTTPServer):
    expected = {
        "total_rows": 5,
        "rows": [
            {
                "value": {
                    "rev": "1-d942f0ce01647aa0f46518b213b5628e"
                },
                "id": "_design/ddoc02",
                "key": "_design/ddoc02"
            },
            {
                "value": {
                    "rev": "1-af856babf9cf746b48ae999645f9541e"
                },
                "id": "_design/ddoc05",
                "key": "_design/ddoc05"
            }
        ],
        "offset": 0
    }

    request_data = {
        "keys": [
            "_design/ddoc02",
            "_design/ddoc05"
        ]
    }

    httpserver.expect_request("/_local/_design_docs", method="POST").respond_with_json(expected)
    response = couch.db.design.get_by_post(uri_segments={'db': '_local'}, data=request_data)
    assert response == expected


def test_all(httpserver: test_server.HTTPServer):
    expected = {
        "offset": 0,
        "rows": [
            {
                "id": "_design/ddoc01",
                "key": "_design/ddoc01",
                "value": {
                    "rev": "1-7407569d54af5bc94c266e70cbf8a180"
                }
            },
            {
                "id": "_design/ddoc02",
                "key": "_design/ddoc02",
                "value": {
                    "rev": "1-d942f0ce01647aa0f46518b213b5628e"
                }
            }
        ]
    }

    httpserver.expect_request("/_local/_design_docs", method="GET").respond_with_json(expected)
    response = couch.db.design.all(uri_segments={'db': '_local'})
    assert response == expected


def test_headers(httpserver: test_server.HTTPServer):
    expected = {
        "Cache-Control": "must-revalidate",
        "Content-Type": "application/json",
        "Date": "Mon, 12 Aug 2013 01:27:41 GMT",
        "Server": "CouchDB (Erlang/OTP)",
        "Content-Length": "2"
    }

    httpserver.expect_request("/_local/_design/ddoc_name", method="HEAD").respond_with_json({}, headers=expected)
    response = couch.db.design.headers(uri_segments={'db': '_local', 'ddoc': 'ddoc_name'})
    assert response == expected


def test_info(httpserver: test_server.HTTPServer):
    expected = {
        "name": "recipe",
        "view_index": {
            "compact_running": False,
            "language": "python",
            "purge_seq": 0,
            "signature": "a59a1bb13fdf8a8a584bc477919c97ac",
            "sizes": {
                "active": 926691,
                "disk": 1982704,
                "external": 1535701
            },
            "update_seq": 12397,
            "updater_running": False,
            "waiting_clients": 0,
            "waiting_commit": False
        }
    }

    httpserver.expect_request("/_local/_design/ddoc_name/_info").respond_with_json(expected)
    response = couch.db.design.info(uri_segments={'db': '_local', 'ddoc': 'ddoc_name'})
    assert response == expected


def test_attachment_headers(httpserver: test_server.HTTPServer):
    expected = {
        "Accept-Ranges": "none",
        "Cache-Control": "must-revalidate",
        "Content-Encoding": "gzip",
        "Content-Length": '2',
        "Content-Type": "application/json",
        "Date": "Thu, 15 Aug 2013 12:42:42 GMT",
        "ETag": "vVa/YgiE1+Gh0WfoFJAcSg==",
        "Server": "CouchDB (Erlang/OTP)"
    }

    httpserver.expect_request("/_local/_design/ddoc_name/attachment", method="HEAD").respond_with_json({}, headers=expected)
    response = couch.db.design.attachment.headers(uri_segments={'db': '_local', 'ddoc': 'ddoc_name', 'attname': 'attachment'})
    assert response == expected


def test_get_attachment(httpserver: test_server.HTTPServer):
    dummy_response = Response()

    httpserver.expect_request("/_local/_design/ddoc_name/attachment_name", method="GET").respond_with_response(dummy_response)
    response = couch.db.design.attachment.get(uri_segments={'db': '_local', 'ddoc': 'ddoc_name', 'attname': 'attachment_name'})
    assert isinstance(response, requests.Response)


def test_get(httpserver: test_server.HTTPServer):
    expected = {
        "_id": "SpaghettiWithMeatballs",
        "_rev": "1-917fa2381192822767f010b95b45325b",
        "description": "An Italian-American dish that usually consists of spaghetti, tomato sauce and meatballs.",
        "ingredients": [
            "spaghetti",
            "tomato sauce",
            "meatballs"
        ],
        "name": "Spaghetti with meatballs"
    }

    httpserver.expect_request("/_local/_design/SpaghettiWithMeatballs", method="GET").respond_with_json(expected)
    response = couch.db.design.get(uri_segments={'db': '_local', 'ddoc': 'SpaghettiWithMeatballs'})
    assert response == expected


def test_save(httpserver: test_server.HTTPServer):
    expected = {
        "id": "SpaghettiWithMeatballs",
        "ok": True,
        "rev": "1-917fa2381192822767f010b95b45325b"
    }

    request_data = {
        "description": "An Italian-American dish that usually consists of spaghetti, tomato sauce and meatballs.",
        "ingredients": [
            "spaghetti",
            "tomato sauce",
            "meatballs"
        ],
        "name": "Spaghetti with meatballs"
    }

    httpserver.expect_request("/_local/_design/SpaghettiWithMeatballs", method="PUT").respond_with_json(expected)
    response = couch.db.design.save(uri_segments={'db': '_local', 'ddoc': 'SpaghettiWithMeatballs'}, data=request_data)
    assert response == expected


def test_delete(httpserver: test_server.HTTPServer):
    expected_json = {
        "id": "FishStew",
        "ok": True,
        "rev": "2-056f5f44046ecafc08a2bc2b9c229e20"
    }

    httpserver.expect_oneshot_request("/_local/_design/FishStew", method="DELETE").respond_with_json(expected_json)
    response = couch.db.design.delete(uri_segments={'db': '_local', 'ddoc': 'FishStew'})
    assert response == expected_json

    for code in [202]:
        httpserver.expect_oneshot_request("/_local/_design/FishStew", method="DELETE").respond_with_json({}, status=code)
        response = couch.db.design.delete(uri_segments={'db': '_local', 'ddoc': 'FishStew'})
        assert isinstance(response, couchapy.CouchError) is False

    for code in [400, 401, 404, 409]:
        httpserver.expect_oneshot_request("/_local/_design/FishStew", method="DELETE").respond_with_json({}, status=code)
        response = couch.db.design.delete(uri_segments={'db': '_local', 'ddoc': 'FishStew'})
        assert isinstance(response, couchapy.CouchError) is True
