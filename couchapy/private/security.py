import  couchapy.decorators as couch


class _Security():
    """
    Namespace class for security object endpoints.

    This class is not intended for direct use and should be accessed through
    the database attribute of a CouchDB instance.
    """
    def __init__(self, parent, **kwargs):
        # TODO: rename this to reference the host couch instance
        self.parent = parent.parent
        self._db = parent._db
        self._predefined_segments = parent._predefined_segments

    @couch.endpoint('/:db:/_security')
    def get(self, couch_data):
        """
        Get the database security document

        See https://docs.couchdb.org/en/stable/api/database/security.html#get--db-_security
        """
        return couch_data

    @couch.endpoint('/:db:/_security', method='put', data_keys=couch.AllowedKeys.DATABASE__SECURITY__DATA)
    def save(self, couch_data):
        """
        Sets the database security document

        See https://docs.couchdb.org/en/stable/api/database/security.html#put--db-_security
        """
        return couch_data
