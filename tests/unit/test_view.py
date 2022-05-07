import  couchapy
import  pytest
import  pytest_httpserver as test_server




@pytest.fixture(autouse=True)
def setup():
    """ setup any state specific to the execution of the given module."""
    global couch
    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000, database_kwargs={"db": '_local'})
    yield


def test_initializer(httpserver: test_server.HTTPServer):
    assert couch.db.design.view.parent == couch.db.parent
    assert couch.db.design.view._db == couch.db._db
    assert couch.db.design.view._predefined_segments == couch.db._predefined_segments

    couch_without_db_args = couchapy.CouchDB()
    assert couch_without_db_args.db.design.view.parent == couch_without_db_args.db.parent
    assert couch_without_db_args.db.design.view._db == couch_without_db_args.db._db
    assert couch_without_db_args.db.design.view._predefined_segments == couch_without_db_args.db._predefined_segments


def test_get(httpserver: test_server.HTTPServer):
    expected = {
        "offset": 0,
        "rows": [
            {
                "id": "SpaghettiWithMeatballs",
                "key": "meatballs",
                "value": 1
            },
            {
                "id": "SpaghettiWithMeatballs",
                "key": "spaghetti",
                "value": 1
            },
            {
                "id": "SpaghettiWithMeatballs",
                "key": "tomato sauce",
                "value": 1
            }
        ],
        "total_rows": 3
    }

    httpserver.expect_request("/_local/_design/docid/_view/view_name").respond_with_json(expected)
    response = couch.db.design.view.get(uri_segments={'db': '_local', 'docid': 'docid', 'view': 'view_name'})
    assert response == expected


def test_get_by_post(httpserver: test_server.HTTPServer):
    expected = {
        "offset": 0,
        "rows": [
            {
                "id": "SpaghettiWithMeatballs",
                "key": "meatballs",
                "value": 1
            },
            {
                "id": "SpaghettiWithMeatballs",
                "key": "spaghetti",
                "value": 1
            },
            {
                "id": "SpaghettiWithMeatballs",
                "key": "tomato sauce",
                "value": 1
            }
        ],
        "total_rows": 3
    }

    httpserver.expect_request("/_local/_design/docid/_view/view_name", method="POST").respond_with_json(expected)
    response = couch.db.design.view.get_by_post(uri_segments={'db': '_local', 'docid': 'docid', 'view': 'view_name'})
    assert response == expected


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

    httpserver.expect_request("/_local/_design/id/_view/view/queries", method="POST").respond_with_json(expected)
    response = couch.db.design.view.queries(uri_segments={'db': '_local', 'docid': 'id', 'view': 'view'}, data=request_data)
    assert response == expected


def test_flush(httpserver: test_server.HTTPServer):
    expected = {"ok": True}

    httpserver.expect_request("/_local/_view_cleanup", method="POST").respond_with_json(expected)
    response = couch.db.design.view.flush(uri_segments={'db': '_local'})
    assert response == expected
