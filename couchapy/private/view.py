import  couchapy.decorators as couch


class _View():
    """
    Namespace class for design document related endpoints.

    This class is not intended for direct use and should be accessed through the database attribute of a CouchDB instance.
    """
    def __init__(self, parent, **kwargs):
        # TODO: rename this to reference the host couch instance
        self.parent = parent.parent
        self._db = parent._db
        self._predefined_segments = parent._predefined_segments

    @couch.endpoint('/:db:/_design/:docid:/_view/:view:', query_keys=couch.AllowedKeys.VIEW__PARAMS)
    def get(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/views.html#get--db-_design-ddoc-_view-view
        """
        return couch_data

    @couch.endpoint('/:db:/_design/:docid:/_view/:view:', method='post', data_keys=couch.AllowedKeys.DATABASE__VIEW_BY_KEY__DATA)
    def get_by_post(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/views.html#post--db-_design-ddoc-_view-view
        """
        return couch_data

    @couch.endpoint('/:db:/_design/:docid:/_view/:view:/queries', method='post', data_keys=couch.AllowedKeys.DATABASE__VIEW_QUERIES__DATA)
    def queries(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/views.html#post--db-_design-ddoc-_view-view-queries
        """
        return couch_data

    @couch.endpoint('/:db:/_view_cleanup', method='post')
    def flush(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/database/compact.html#post--db-_view_cleanup
        """
        return couch_data
