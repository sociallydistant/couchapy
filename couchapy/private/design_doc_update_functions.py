import  couchapy.decorators as couch


class _UpdateFunction():
    """
    Namespace class for design document related endpoints for executing update functions.

    This class is not intended for direct use and should be accessed through the database attribute of a CouchDB instance.
    """
    def __init__(self, parent, **kwargs):
        # TODO: rename this to reference the host couch instance
        self.parent = parent.parent
        self._db = parent._db
        self._predefined_segments = parent._predefined_segments

    @couch.endpoint('/:db:/_design/:ddocid:/_update/:update_function:', query_keys=couch.AllowedKeys.VIEW__PARAMS)
    def run(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/views.html#get--db-_design-ddoc-_view-view
        """
        return couch_data

    @couch.endpoint('/:db:/_design/:ddocid:/_update/:update_function:/:docid:', method='put', data_keys=couch.AllowedKeys.DATABASE__VIEW_BY_KEY__DATA)
    def run_on_doc(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/views.html#post--db-_design-ddoc-_view-view
        """
        return couch_data
