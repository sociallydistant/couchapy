import threading

import couchapy.session
import couchapy.server
import couchapy.database


class CouchDB():
    """
    Exposes an interface for interating with a CouchDB server's REST API.

    :param str  host:           Address that the CouchDB server is served from. (Default: http://127.0.0.1)
    :param int  port:           Port number that the CouchDB server is listening on. (Default: 5984)

    :param str  username:       Username used to authenticate to the CouchDB server. (Default: None)
    :param str  password:       Password used to authenticate to the CouchDB server. (Default: None)

    :param bool auto_connect:   Determines if an authentication attempt will be made during instancing of this object. (Default: False)
    :param int  keep_alive:     Determines if automatic session renewal will be attempted and at what frequency.
                                If > 0, session renewal is performed every keep_alive seconds. (Default: 0)
    :param bool admin_party     Determines whether or not to attempt connections to the CouchDB using Admin Party. (Default: False)

    Usage Examples:
      couchDb = CouchDB([username=<user>[, password=<password>][,<arg=<value>])
    """

    def __init__(self, **kwargs):
        self._context_manager = False

        self._headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        self.custom_headers = kwargs.get('custom_headers', {})  # TODO: implement

        self._auto_renew_worker = None
        self._auto_renew_worker_lock = threading.RLock()

        self.host = kwargs.get('host', 'http://127.0.0.1')
        self.port = kwargs.get('port', 5984)

        self.name = kwargs.get('name', None)
        self.password = kwargs.get('password', None)

        self.keep_alive = kwargs.get('keep_alive', 0)

        self._admin_party = kwargs.get('admin_party', False)  # TODO: implement admin party

        self.session = couchapy.session.Session(self, **kwargs)
        # self.server = couchapy.server.Server(session=self.session)
        # self.db = couchapy.database.Database(session=self.session, **kwargs)
        # self.user = User(session=self.session, db=self.db)

        # TODO: implement a generic Error class to hold error information that consumer can check
        if (kwargs.get('auto_connect', False) is True and self.session.basic_auth is False):
            self.session.authenticate(data={'name': self.name, 'password': self.password})

        if self.session.auth_token and self.keep_alive > 0:
            self._auto_renew_session(self._keep_alive)

    def __enter__(self):
        self._context_manager = True
        return self

    def __exit__(self, type, value, traceback):
        self._context_manager = False

    def start_auto_renew(self):
        # ensure only one session renewal thread can run
        with self._auto_renew_worker_lock:
            if self._auto_renew_worker is None:
                self._auto_renew_worker = threading.Thread(target=self._auto_renew_session,
                                                           args=(self._keep_alive),
                                                           daemon=True)
                self._auto_renew_worker.start()

    def _auto_renew_session(self, session_timeout):
        stop_auto_renew = threading.Event()
        while not stop_auto_renew.is_set():
            stop_auto_renew.wait(session_timeout)

            if self._keep_alive > 0:
                self.session.renew_session()
            else:
                stop_auto_renew.set()
