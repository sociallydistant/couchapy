import  couchapy.decorators as couch


class _Revisions():
    """
    Namespace class for revision related endpoints.

    This class is not intended for direct use and should be accessed through the database attribute of a CouchDB instance.
    """
    def __init__(self, parent, **kwargs):
        # TODO: rename this to reference the host couch instance
        self.parent = parent.parent
        self._db = parent._db
        self._predefined_segments = parent._predefined_segments

    @couch.endpoint('/:db:/_missing_revs', method='post')
    def missing(self, couch_data):
        """
        Example:
        missing_revs = couch.db.revs.missing(data={"docid": ["rev1", "rev2", "rev3"]})

        Example:
        missing_revs = couch.db.revs.missing(uri_segments={'db': 'some_database', data={"docid": ["rev1", "rev2", "rev3"]})

        See: https://docs.couchdb.org/en/stable/api/database/misc.html#post--db-_missing_revs
        """

        return couch_data

    @couch.endpoint('/:db:/_revs_diff', method='post')
    def diff(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/database/misc.html#post--db-_revs_diff
        """
        return couch_data

    @couch.endpoint('/:db:/_revs_limit')
    def get_limit(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/database/misc.html#get--db-_revs_limit
        """
        return couch_data

    @couch.endpoint('/:db:/_revs_limit', method='put')
    def set_limit(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/database/misc.html#put--db-_revs_limit
        """
        return couch_data
