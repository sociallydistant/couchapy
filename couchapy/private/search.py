import  couchapy.decorators as couch


class _Search():
    """
    Namespace class for search index related endpoints.

    This class is not intended for direct use and should be accessed through the database attribute of a CouchDB instance.
    """
    def __init__(self, parent, **kwargs):
        # TODO: rename this to reference the host couch instance
        self.parent = parent.parent
        self._db = parent._db
        self._predefined_segments = parent._predefined_segments

    @couch.endpoint('/:db:/_design/:docid:/_search/:index:', query_keys=couch.AllowedKeys.SEARCH__PARAMS)
    def get(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/search.html#get--db-_design-ddoc-_search-index
        """
        return couch_data

    @couch.endpoint('/:db:/_design/:docid:/_search_info/:index:')
    def info(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/search.html#get--db-_design-ddoc-_search_info-index
        """
        return couch_data
