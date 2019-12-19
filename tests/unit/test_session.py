import pytest
from pytest_httpserver import HTTPServer

from relaxed import CouchDB, CouchError
from relaxed.session import Session


@pytest.fixture
def httpserver_listen_address():
    return ("127.0.0.1", 8000)


def test_session_auto_connect(httpserver: HTTPServer):
  expected_json = {"ok": True, "name": "root", "roles": ["_admin"]}

  httpserver.expect_oneshot_request("/_session",  method="POST").respond_with_json(expected_json, headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; Version=1; Path=/; HttpOnly'})
  couch = CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000, auto_connect=True)
  assert couch.session.auth_token == 'cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw'

  for code in [401]:
    httpserver.expect_oneshot_request("/_session",  method="POST").respond_with_json({}, status=code)
    couch = CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000)
    response = couch.session.authenticate()
    assert isinstance(response, CouchError) is True


def test_auto_renew_session_terminates_on_instance_destruction(httpserver: HTTPServer):
  expected_json = {"ok": True, "name": "root", "roles": ["_admin"]}

  httpserver.expect_request("/_session",  method="POST").respond_with_json(expected_json, headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; Version=1; Path=/; HttpOnly'})

  for k in range(1, 50):
    couch = CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000, auto_connect=True, keep_alive=300)
    assert couch.session._keep_alive == 300
    del couch  # brittle means of getting the code coverage on destructor.


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

  httpserver.expect_request("/_session",  method="POST").respond_with_json(expected_json, headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; Version=1; Path=/; HttpOnly'})
  httpserver.expect_oneshot_request("/_session", method="GET").respond_with_json(expected_json, headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; Version=1; Path=/; HttpOnly'})
  couch = CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000, auto_connect=True)
  response = couch.session.get_session_info()
  assert response == expected_json

  httpserver.expect_oneshot_request("/_session", method="GET").respond_with_json(expected_json, headers={'Set-Cookie': 'AuthSession=cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw; Version=1; Path=/; HttpOnly'})
  response = couch.session.renew_session()
  assert response == expected_json


  for code in [401]:
    httpserver.expect_oneshot_request("/_session",  method="GET").respond_with_json({}, status=code)
    response = couch.session.get_session_info()
    assert isinstance(response, CouchError) is True

def test_close(httpserver: HTTPServer):
  httpserver.expect_request("/_session",  method="DELETE").respond_with_json({})

  couch = CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000)
  response = couch.session.close()
  assert response is None

@pytest.mark.xfail(condition=True, reason="Authenticate via proxy is not implemented yet...", raises=None, run=True, strict=True)
def test_authenticate_via_proxy(httpserver: HTTPServer):
  session = Session()
  session.authenticate_via_proxy('some_user', 'some_roles', 'some_token')
  assert False

def test_keep_alive(httpserver: HTTPServer):
  session = Session(keep_alive=300, auth_token='cm9vdDo1MEJCRkYwMjq0LO0ylOIwShrgt8y-UkhI-c6BGw')
  session.keep_alive(True)
  assert 1 == len(session._keep_alive_timeloop.jobs)

  # only 1 keep alive is allowed
  session.keep_alive(True)
  assert 1 == len(session._keep_alive_timeloop.jobs)

  # keep alive should not work without an auth token
  session.auth_token = None
  session.keep_alive(True)
  assert 1 == len(session._keep_alive_timeloop.jobs)

  session.keep_alive(False)
  assert 1 == len(session._keep_alive_timeloop.jobs)

def test_create_basic_auth_header(httpserver: HTTPServer):
  session = Session(username="test", password="test")
  basic_auth_header = session._create_basic_auth_header()
  assert basic_auth_header == {'Authorization': 'Basic dGVzdDp0ZXN0'}
