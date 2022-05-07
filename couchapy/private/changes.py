import  couchapy.decorators as couch


class _DatabaseChanges():
    """
    Namespace class for design document related endpoints.

    This class is not intended for direct use and should be accessed through the database attribute of a CouchDB instance.
    """
    def __init__(self, parent, **kwargs):
        # TODO: rename this to reference the host couch instance
        self.parent = parent.parent
        self._db = parent._db
        self._predefined_segments = parent._predefined_segments

    @couch.endpoint('/:db:/_changes', method='post',
                    data_keys=couch.AllowedKeys.DATABASE__CHANGES__DATA,
                    query_keys=couch.AllowedKeys.DATABASE__CHANGES__PARAMS)
    def get_by_post(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_design_docs
        """
        return couch_data

    @couch.endpoint('/:db:/_changes', query_keys=couch.AllowedKeys.DATABASE__CHANGES__PARAMS)
    def get(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/common.html#get--db-_design-ddoc
        See https://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid
        """
        return couch_data
