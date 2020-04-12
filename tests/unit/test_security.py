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
    assert couch.db.security.parent == couch.db.parent
    assert couch.db.security._db == couch.db._db
    assert couch.db.security._predefined_segments == couch.db._predefined_segments

    couch_without_db_args = couchapy.CouchDB()
    assert couch_without_db_args.db.security.parent == couch_without_db_args.db.parent
    assert couch_without_db_args.db.security._db == couch_without_db_args.db._db
    assert couch_without_db_args.db.security._predefined_segments == couch_without_db_args.db._predefined_segments


def test_save(httpserver: test_server.HTTPServer):
    expected = {"ok": True}

    request_data = {
        "admins": {
            "names": [
                "superuser"
            ],
            "roles": [
                "admins"
            ]
        },
        "members": {
            "names": [
                "user1",
                "user2"
            ],
            "roles": [
                "developers"
            ]
        }
    }

    httpserver.expect_request("/_local/_security", method="PUT").respond_with_json(expected)
    response = couch.db.security.save(uri_segments={'db': '_local'}, data=request_data)
    assert response == expected


def test_get(httpserver: test_server.HTTPServer):
    expected = {
        "admins": {
            "names": [
                "superuser"
            ],
            "roles": [
                "admins"
            ]
        },
        "members": {
            "names": [
                "user1",
                "user2"
            ],
            "roles": [
                "developers"
            ]
        }
    }

    httpserver.expect_request("/_local/_security").respond_with_json(expected)
    response = couch.db.security.get(uri_segments={'db': '_local'})
    assert response == expected
