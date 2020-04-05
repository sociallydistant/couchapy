import  couchapy
import  pytest
from    pytest_httpserver import HTTPServer


@pytest.fixture
def httpserver_listen_address():
    return ("127.0.0.1", 8000)


def test_authenticate(httpserver: HTTPServer):
    json_response = {"ok": True, "name": "root", "roles": ["_admin"]}

    httpserver.expect_oneshot_request("/_session", method="POST") \
              .respond_with_json(json_response,
                                 headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; '
                                                        'Version=1; Path=/; HttpOnly'})
    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000, auto_connect=False)
    couch.session.authenticate(data={'name': couch.name, 'password': couch.password})
    assert couch.session.auth_token == "cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw"


def test_get_session_info(httpserver: HTTPServer):
    expected_json = {
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

    httpserver.expect_request("/_session", method="POST").respond_with_json(expected_json, headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; Version=1; Path=/; HttpOnly'})
    httpserver.expect_oneshot_request("/_session", method="GET").respond_with_json(expected_json, headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; Version=1; Path=/; HttpOnly'})
    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000, auto_connect=True)
    response = couch.session.get_session_info()
    assert response == expected_json

    httpserver.expect_oneshot_request("/_session", method="GET").respond_with_json(expected_json, headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; Version=1; Path=/; HttpOnly'})
    response = couch.session.renew_session()
    assert response == expected_json

    for code in [401]:
        httpserver.expect_oneshot_request("/_session", method="GET").respond_with_json({}, status=code)
        response = couch.session.get_session_info()
        assert isinstance(response, couchapy.error.CouchError) is True


def test_close(httpserver: HTTPServer):
    httpserver.expect_request("/_session", method="DELETE").respond_with_json({})

    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000)
    response = couch.session.close()
    assert response is None


@pytest.mark.xfail(condition=True, reason="Authenticate via proxy is not implemented yet...", raises=None, run=True, strict=True)
def test_authenticate_via_proxy(httpserver: HTTPServer):
    assert False, "TEST STUB: Not Implemented"


def test_create_basic_auth_header(httpserver: HTTPServer):
    couch = couchapy.CouchDB(name="test", password="test", host="http://127.0.0.1", port=8000)
    basic_auth_header = couch.session._create_basic_auth_header()
    assert basic_auth_header == {'Authorization': 'Basic dGVzdDp0ZXN0'}
