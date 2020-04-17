import  couchapy.decorators as couch


class _LocalDocuments():
    """
    Namespace class for local non-replicating document related endpoints.

    This class is not intended for direct use and should be accessed through the database attribute of a CouchDB instance.
    """
    def __init__(self, parent, **kwargs):
        # TODO: rename this to reference the host couch instance
        self.parent = parent.parent
        self._db = parent._db
        self._predefined_segments = parent._predefined_segments

    @couch.endpoint('/:db:/_local_docs', method='post', data_keys=couch.AllowedKeys.DATABASE__LOCAL_DOCS__DATA)
    def get_by_post(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/local.html#post--db-_local_docs
        """
        return couch_data

    @couch.endpoint('/:db:/_local_docs/queries', method='post', data_keys=couch.AllowedKeys.DATABASE__LOCAL_DOCS_QUERIES__DATA)
    def queries(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_all_docs-queries
        """
        return couch_data

    @couch.endpoint('/:db:/_local_docs', query_keys=couch.AllowedKeys.VIEW__PARAMS)
    def all(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/local.html#get--db-_local_docs
        """
        return couch_data

    @couch.endpoint('/:db:/_local/:docid:', query_keys=couch.AllowedKeys.DATABASE__DOCUMENT__PARAMS)
    def get(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/local.html#get--db-_local-docid
        See https://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid
        """
        return couch_data

    @couch.endpoint('/:db:/_local/:docid:', method='put', query_keys=couch.AllowedKeys.DATABASE__DOCUMENT__NAMED_DOC__PARAMS)
    def save(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/local.html#put--db-_local-docid
        See https://docs.couchdb.org/en/stable/api/document/common.html#put--db-docid
        """
        return couch_data

    @couch.endpoint('/:db:/_local/:docid:', method='delete', query_keys=couch.AllowedKeys.DATABASE__DOCUMENT__DELETE__PARAMS)
    def delete(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/local.html#delete--db-_local-docid
        See https://docs.couchdb.org/en/stable/api/document/common.html#delete--db-docid
        """
        return couch_data

    # TODO: implement custom verb handling in endpoint decorator
    # TODO: CouchDB COPY command uses custom headers to send data...need to implement a way to handle this too
    # see https://requests.readthedocs.io/en/master/user/advanced/
    # @couch.endpoint('/:db:/_local/:docid:', method='copy', query_keys=AllowedKeys.DATABASE__DOCUMENT__COPY__PARAMS)
    # def copy(self, couch_data):
    #     """
    #     See https://docs.couchdb.org/en/stable/api/local.html#copy--db-_local-docid
    #     """
    #     return couch_data
