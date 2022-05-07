import pytest


@pytest.fixture(scope='session')
def httpserver_listen_address():
    return ("127.0.0.1", 8000)
