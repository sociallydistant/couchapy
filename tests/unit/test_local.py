import  couchapy
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
    assert couch.db.local.parent == couch.db.parent
    assert couch.db.local._db == couch.db._db
    assert couch.db.local._predefined_segments == couch.db._predefined_segments

    couch_without_db_args = couchapy.CouchDB()
    assert couch_without_db_args.db.local.parent == couch_without_db_args.db.parent
    assert couch_without_db_args.db.local._db == couch_without_db_args.db._db
    assert couch_without_db_args.db.local._predefined_segments == couch_without_db_args.db._predefined_segments


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

    httpserver.expect_request("/_local/_local_docs/queries", method="POST").respond_with_json(expected)
    response = couch.db.local.queries(uri_segments={'db': '_local'}, data=request_data)
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

    httpserver.expect_request("/_local/_local_docs", method="POST").respond_with_json(expected)
    response = couch.db.local.get_by_post(uri_segments={'db': '_local'}, data=request_data)
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

    httpserver.expect_request("/_local/_local_docs", method="GET").respond_with_json(expected)
    response = couch.db.local.all(uri_segments={'db': '_local'})
    assert response == expected


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

    httpserver.expect_request("/_local/_local/SpaghettiWithMeatballs", method="GET").respond_with_json(expected)
    response = couch.db.local.get(uri_segments={'db': '_local', 'docid': 'SpaghettiWithMeatballs'})
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

    httpserver.expect_request("/_local/_local/SpaghettiWithMeatballs", method="PUT").respond_with_json(expected)
    response = couch.db.local.save(uri_segments={'db': '_local', 'docid': 'SpaghettiWithMeatballs'}, data=request_data)
    assert response == expected


def test_delete(httpserver: test_server.HTTPServer):
    expected_json = {
        "id": "FishStew",
        "ok": True,
        "rev": "2-056f5f44046ecafc08a2bc2b9c229e20"
    }

    httpserver.expect_oneshot_request("/_local/_local/FishStew", method="DELETE").respond_with_json(expected_json)
    response = couch.db.local.delete(uri_segments={'db': '_local', 'docid': 'FishStew'})
    assert response == expected_json

    for code in [202]:
        httpserver.expect_oneshot_request("/_local/_local/FishStew", method="DELETE").respond_with_json({}, status=code)
        response = couch.db.local.delete(uri_segments={'db': '_local', 'docid': 'FishStew'})
        assert isinstance(response, couchapy.CouchError) is False

    for code in [400, 401, 404, 409]:
        httpserver.expect_oneshot_request("/_local/_local/FishStew", method="DELETE").respond_with_json({}, status=code)
        response = couch.db.local.delete(uri_segments={'db': '_local', 'docid': 'FishStew'})
        assert isinstance(response, couchapy.CouchError) is True
