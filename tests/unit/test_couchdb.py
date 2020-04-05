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
    couch = couchapy.CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000)
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


def test_constructor_with_params():
    assert False, \
        "TEST STUB: Not implemented"


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

    couch = couchapy.CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000, auto_connect=True)
    assert couch.session.auth_token == 'cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw', \
        "Expected session auth token to match, but it didn't"

    couch = couchapy.CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000, auto_connect=False)
    assert couch.session.auth_token is None, \
        "Expected auth token to be None when auto_connect is False"

    couch = couchapy.CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000)
    assert couch.session.auth_token is None, \
        "Expected session auth token to be None when auto_connect is not provided"

    for code in [401]:
        httpserver.expect_oneshot_request("/_session", method="POST").respond_with_json({}, status=code)
        couch = couchapy.CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000)
        response = couch.session.authenticate()
        assert isinstance(response, couchapy.error.CouchError) is True


def test_auto_session_renewal_works():
    assert False, \
        "TEST STUB: Not implemented"


def test_stopping_session_renewal_exits_gracefully():
    assert False, \
        "TEST STUB: Not implemented"

