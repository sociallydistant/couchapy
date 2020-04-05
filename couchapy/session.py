import requests

import  couchapy
import  couchapy.error
import  couchapy.decorators as couch

# TODO: Refactor to extend requests.Session and not dict


class Session():
    """
    Interacts with a CouchDB server's REST API for session management.

    This class is not intended to be instanced directly.

    Attributes:

    :param str auth_token: AuthSession value used to authenticate to the CouchDB server.
    If provided, authentication using AuthSession will be attempted. AuthSession is set/updated
    with successful authentication when connecting with username and password. (Default: None)

    :param CouchDB parent   CouchDB instance.
    :param str  auth_token  Most recent session token retreived from the CouchDB Server
                            specified by parent
    :param bool basic_auth  Sets authentication method to the CouchDB server to Basic. If basic authentication is used, auto_connect has no effect. (Default: False)
    """
    def __init__(self, parent, **kwargs):

        self.auth_token = kwargs.get('auth_token', None)
        self.basic_auth = kwargs.get('basic_auth', False)  # TODO: implement basic auth

        # reference to the parent CouchDB instance.
        # Primarily required for the endpoint decorator to access
        # server configuration such as host and port
        self.parent = parent

    def _create_basic_auth_header(self):
        return requests.auth.HTTPBasicAuth(self.parent.name, self.parent.password)(requests.Request()).headers

    def set_auth_token_from_headers(self, headers):
        # if a new auth token is issued, include it in the response, otherwise, return the original
        if ('Set-Cookie' in headers):
            self.auth_token = headers.get('Set-Cookie').split(';', 2)[0].split('=')[1]

    @couch.endpoint('/_session', method='post', data_keys={'name': str, 'password': str})
    def authenticate(self, doc):
        return doc

    @couch.endpoint('/_session')
    def get_session_info(self, doc):
        return doc

    @couch.endpoint('/_session', method='delete')
    def close(self, doc):
        return doc if isinstance(doc, couchapy.error.CouchError) else None

    def authenticate_via_proxy(self, username, roles, token):
        """
        Not implemented. See:
        https://docs.couchdb.org/en/stable/api/server/authn.html#proxy-authentication
        https://stackoverflow.com/a/40499853/3169479 (for implementation details)
        """
        pass

    def renew_session(self):
        """
        Alias for get_session_info()
        """
        return self.get_session_info()
