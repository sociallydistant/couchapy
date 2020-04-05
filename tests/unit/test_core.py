# import pytest
# from pytest_httpserver import HTTPServer
#
# from relaxed import AllowedKeys, CouchDB, CouchError, InvalidKeysException
# from relaxed.server import Server
#
# @pytest.fixture
# def httpserver_listen_address():
#     return ("127.0.0.1", 8000)
#
#
# @pytest.fixture(autouse=True)
# def setup():
#   """ setup any state specific to the execution of the given module."""
#   global couch
#   couch = CouchDB(username="test", password="test", host="http://127.0.0.1", port=8000)
#   yield
#
#
# def test_creating_a_valid_user(httpserver: HTTPServer):
#   expected_json = {"ok": True, "id": "org.couchdb.user:test", "rev": "1-e0ebfb84005b920488fc7a8cc5470cc0"}
#
#   httpserver.expect_request("/_users/org.couchdb.user:test",  method="PUT").respond_with_json(expected_json)
#   response = couch.user.create(name='test', password='test')
#
#   assert response == expected_json
#
# def test_get_a_valid_user(httpserver: HTTPServer):
#   expected_json = {"ok": True, "id": "org.couchdb.user:test", "rev": "1-e0ebfb84005b920488fc7a8cc5470cc0"}
#
#   httpserver.expect_request("/_users/org.couchdb.user:testuser",  method="GET").respond_with_json(expected_json)
#   response = couch.user.get(id='testuser')
#
#   assert response == expected_json
