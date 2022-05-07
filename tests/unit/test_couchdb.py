import  couchapy
import  pytest
import  pytest_httpserver as test_server

import  threading
import  time


@pytest.fixture(autouse=True)
def setup():
    """ setup any state specific to the execution of the given module."""
    global couch
    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000)
    yield


def test_empty_constructor():
    couch = couchapy.CouchDB()

    assert couch._context_manager is False
    assert couch._auto_renew_worker is None
    assert couch.host == 'http://127.0.0.1'
    assert couch.port == 5984
    assert couch.name is None
    assert couch.password is None
    assert couch.keep_alive == 0
    assert couch._admin_party is False
    assert isinstance(couch.session, couchapy.Session)
    assert isinstance(couch.session, couchapy.Session) and couch.session.auth_token is None


def test_constructor_with_params(httpserver: test_server.HTTPServer):
    json_response = {"ok": True, "name": "root", "roles": ["_admin"]}

    httpserver.expect_oneshot_request("/_session", method="POST") \
              .respond_with_json(json_response,
                                 headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; '
                                                        'Version=1; Path=/; HttpOnly'})

    couch = couchapy.CouchDB(custom_headers={"header_key": "header_value"},
                             session_timeout=60,
                             keep_alive=True,
                             host="https://localhost",
                             port=6984,
                             name="someadmin",
                             password="somepassword",
                             admin_party=True,
                             auto_connect=False)

    assert 'header_key' in couch.custom_headers and couch.custom_headers['header_key'] == 'header_value'
    assert couch.session_timeout == 60
    assert couch.keep_alive is True
    assert couch.host == "https://localhost"
    assert couch.port == 6984
    assert couch.name == "someadmin"
    assert couch.password == "somepassword"
    assert couch._admin_party is True
    assert couch.session.auth_token is None

    couch = couchapy.CouchDB(custom_headers={"header_key": "header_value"},
                             session_timeout=60,
                             port=8000,
                             keep_alive=True,
                             name="someadmin",
                             password="somepassword",
                             auto_connect=True)

    assert couch._auto_renew_worker is not None


def test_context_manager():
    with couchapy.CouchDB() as couch:
        assert couch._context_manager is True, \
            "Expected context manager flag to be True inside of a with block"

    assert couch._context_manager is False, \
        "Expected context manager flag to be False outisde of a with block"


def test_auto_connect_on_initialization(httpserver: test_server.HTTPServer):
    json_response = {"ok": True, "name": "root", "roles": ["_admin"]}

    httpserver.expect_oneshot_request("/_session", method="POST") \
              .respond_with_json(json_response,
                                 headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; '
                                                        'Version=1; Path=/; HttpOnly'})

    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000, auto_connect=True)
    assert couch.session.auth_token == 'cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw', \
        "Expected session auth token to match, but it didn't"

    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000, auto_connect=False)
    assert couch.session.auth_token is None, \
        "Expected auth token to be None when auto_connect is False"

    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000)
    assert couch.session.auth_token is None, \
        "Expected session auth token to be None when auto_connect is not provided"

    for code in [401]:
        httpserver.expect_oneshot_request("/_session", method="POST").respond_with_json({}, status=code)
        couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000)
        response = couch.session.authenticate()
        assert isinstance(response, couchapy.error.CouchError) is True


def test_auto_session_renewal(httpserver: test_server.HTTPServer):
    authentication_response = {"ok": True, "name": "root", "roles": ["_admin"]}
    renewal_response = {
        "info": {
            "authenticated": "cookie",
            "authentication_db": "_users",
            "authentication_handlers": [
                "cookie",
                "default"
            ]
        },
        "ok": True,
        "userCtx": {
            "name": "root",
            "roles": [
                "_admin"
            ]
        }
    }

    httpserver.expect_oneshot_request("/_session", method="POST") \
              .respond_with_json(authentication_response,
                                 headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; '
                                                        'Version=1; Path=/; HttpOnly'})

    httpserver.expect_request("/_session", method="GET") \
              .respond_with_json(renewal_response,
                                 headers={'Set-Cookie': 'AuthSession=some_new_auth_token; Version=1; Path=/; HttpOnly'})

    assert couch._auto_renew_worker is None, \
        "Expected session renewal worker to be None"

    couch.keep_alive = True
    couch.session_timeout = 0.5
    couch.start_auto_session()

    assert isinstance(couch._auto_renew_worker, threading.Thread), \
        "Expected session renewal worker to be an instance of Thread"

    # wait for the thread to renew the session before checking that it was changed
    time.sleep(0.75)
    assert couch.session.auth_token == "some_new_auth_token"
    couch.stop_auto_session()

    # give the thread time to shut down
    time.sleep(0.2)
    assert couch._auto_renew_worker is None


# def test_creating_a_valid_user(httpserver: HTTPServer):
#     expected_json = {"ok": True, "id": "org.couchdb.user:test", "rev": "1-e0ebfb84005b920488fc7a8cc5470cc0"}
#
#     httpserver.expect_request("/_users/org.couchdb.user:test", method="PUT").respond_with_json(expected_json)
#     response = couch.user.create(name='test', password='test')
#
#     assert response == expected_json
#
#
# def test_get_a_valid_user(httpserver: HTTPServer):
#     expected_json = {"ok": True, "id": "org.couchdb.user:test", "rev": "1-e0ebfb84005b920488fc7a8cc5470cc0"}
#
#     httpserver.expect_request("/_users/org.couchdb.user:testuser", method="GET").respond_with_json(expected_json)
#     response = couch.user.get(id='testuser')
#
#     assert response == expected_json
