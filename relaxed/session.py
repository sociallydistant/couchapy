import requests

from timeloop import Timeloop
from datetime import timedelta

from .core import RelaxedDecorators, CouchError

# TODO: Refactor to extend requests.Session and not dict


class Session():
  """
  Interacts with a CouchDB server's REST API for session management.

  Examples:
    couchDB = Session(address="https://somehost.com", port="6984", username="admin", password="super_secure", address="https://somehost.com", port="6984")
    couchDB = Session(address="https://somehost.com", port="6984", auth_token="bGVlLmx1bm5AZGFsLmNhOjVERTQ4RjhCOq-IvL4mhVVUFn4k5H1bIYiggf3X")
    couchDB = Session(address="https://somehost.com", port="6984", username="admin", password="super_secure", keep_alive=290)

  Attributes:
  :param bool admin_party Determines whether or not to attempt connections to the CouchDB using Admin Party. (Default: False)
  :param str username: Username used to authenticate to the CouchDB server. (Default: None)
  :param str password: Password used to authenticate to the CouchDB server. (Default: None)
  :param str auth_token: AuthSession value used to authenticate to the CouchDB server.
    If provided, authentication using AuthSession will be attempted. AuthSession is set/updated
    with successful authentication when connecting with username and password. (Default: None)

  :param str host: Address that the CouchDB server is served from. (Default: http://127.0.0.1)
  :param int port: Port number that the CouchDB server is listening on. (Default: 5984)
  :param int keep_alive: Determines if automatic session renewal will be attempted and at what frequency. If > 0, session renewal is performed every keep_alive seconds. (Default: 0)
  :param bool auto_connect: Determines if an authentication attempt will be made during instancing of this object. (Default: False)
  :param bool basic_auth: Sets authentication method to the CouchDB server to Basic. If basic authentication is used, auto_connect has no effect. (Default: False)

  :param dict custom_headers: Dictionary of custom headers to add to each request to the CouchDB server. (Default: None)
  """

  def __init__(self, **kwargs):
    self._host = kwargs.get('host', 'http://127.0.0.1')
    self._port = kwargs.get('port', 5984)
    self.address = f'{self._host}:{self._port}'

    self.custom_headers = kwargs.get('custom_headers', {})  # TODO: implement

    self._keep_alive = kwargs.get('keep_alive', 0)
    self._keep_alive_timeloop = Timeloop()

    self._name = kwargs.get('username', None)
    self._password = kwargs.get('password', None)
    self.auth_token = kwargs.get('auth_token', None)

    self._auto_connect = kwargs.get('auto_connect', False)

    self._basic_auth = kwargs.get('basic_auth', False)  # TODO: implement basic auth
    self._admin_party = kwargs.get('admin_party', False)  # TODO: implement admin party

    self._headers = {
      'Content-type': 'application/json',
      'Accept': 'application/json'}

    # reference to this object is required for the CouchDBDecorators.endpoint to be able to update the auth token
    self.session = self

    # TODO: implement a generic Error class to hold error information that consumer can check
    if (self._auto_connect is True and self._basic_auth is False):
      self.authenticate(data={'name': self._name, 'password': self._password})

  def __del__(self):
    if (self._keep_alive > 0):
      self._keep_alive_timeloop.stop()

  def _create_basic_auth_header(self):
    return requests.auth.HTTPBasicAuth(self._name, self._password)(requests.Request()).headers

  def set_auth_token_from_headers(self, headers):
    # if a new auth token is issued, include it in the response, otherwise, return the original
    if ('Set-Cookie' in headers):
      self.auth_token = headers.get('Set-Cookie').split(';', 2)[0].split('=')[1]

  @RelaxedDecorators.endpoint('/_session', method='post', data_keys={'name': str, 'password': str})
  def authenticate(self, doc):
    return doc

  @RelaxedDecorators.endpoint('/_session')
  def get_session_info(self, doc):
    return doc

  @RelaxedDecorators.endpoint('/_session', method='delete')
  def close(self, doc):
    return doc if isinstance(doc, CouchError) else None

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

  def keep_alive(self, isEnabled=False):
    """
    Enables or disables keep alive.
    """
    if (isEnabled is False):
      self._keep_alive_timeloop.stop()
    elif (isEnabled and self._keep_alive > 0 and self.auth_token is not None):
      if (len(self._keep_alive_timeloop.jobs) == 0):
        self._keep_alive_timeloop._add_job(func=self.renew_session, interval=timedelta(seconds=self._keep_alive))
      self._keep_alive_timeloop.start()
