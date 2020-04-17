import  couchapy.decorators as couch
import  couchapy.private.attachment as _attachment
import  couchapy.private.view as _view


class _DesignDocument():
    """
    Namespace class for design document related endpoints.

    This class is not intended for direct use and should be accessed through the database attribute of a CouchDB instance.
    """
    def __init__(self, parent, **kwargs):
        # TODO: rename this to reference the host couch instance
        self.parent = parent.parent
        self._db = parent._db
        self._predefined_segments = parent._predefined_segments
        self.attachment = _attachment._DesignDocAttachment(self)
        self.view = _view._View(self)

    @couch.endpoint('/:db:/_design_docs', method='post', data_keys=couch.AllowedKeys.DATABASE__DESIGN_DOCS__DATA)
    def get_by_post(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_design_docs
        """
        return couch_data

    @couch.endpoint('/:db:/_design_docs/queries', method='post', data_keys=couch.AllowedKeys.DATABASE__DESIGN_DOCS_QUERIES__DATA)
    def queries(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/database/bulk-api.html#post--db-_all_docs-queries
        """
        return couch_data

    @couch.endpoint('/:db:/_compact/:ddoc:', method='post')
    def compact(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/database/compact.html#post--db-_compact-ddoc
        """
        return couch_data

    @couch.endpoint('/:db:/_design_docs', query_keys=couch.AllowedKeys.VIEW__PARAMS)
    def all(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/database/bulk-api.html#get--db-_design_docs
        """
        return couch_data

    @couch.endpoint('/:db:/_design/:ddoc:', method='head', query_keys=couch.AllowedKeys.DATABASE__DOCUMENT__PARAMS)
    def headers(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/common.html#head--db-_design-ddoc
        See https://docs.couchdb.org/en/stable/api/document/common.html#head--db-docid
        """
        return kwargs.get("response_headers", None)

    @couch.endpoint('/:db:/_design/:ddoc:/_info')
    def info(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/common.html#get--db-_design-ddoc-_info
        """
        return couch_data

    @couch.endpoint('/:db:/_design/:ddoc:', query_keys=couch.AllowedKeys.DATABASE__DOCUMENT__PARAMS)
    def get(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/common.html#get--db-_design-ddoc
        See https://docs.couchdb.org/en/stable/api/document/common.html#get--db-docid
        """
        return couch_data

    @couch.endpoint('/:db:/_design/:ddoc:', method='put', query_keys=couch.AllowedKeys.DATABASE__DOCUMENT__NAMED_DOC__PARAMS)
    def save(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/common.html#put--db-_design-ddoc
        See https://docs.couchdb.org/en/stable/api/document/common.html#put--db-docid
        """
        return couch_data

    @couch.endpoint('/:db:/_design/:ddoc:', method='delete', query_keys=couch.AllowedKeys.DATABASE__DOCUMENT__DELETE__PARAMS)
    def delete(self, couch_data):
        """
        See https://docs.couchdb.org/en/stable/api/ddoc/common.html#delete--db-_design-ddoc
        See https://docs.couchdb.org/en/stable/api/document/common.html#delete--db-docid
        """
        return couch_data

    # TODO: implement custom verb handling in endpoint decorator
    # TODO: CouchDB COPY command uses custom headers to send data...need to implement a way to handle this too
    # see https://requests.readthedocs.io/en/master/user/advanced/
    # @couch.endpoint('/:db:/_design/:docid:', method='copy', query_keys=AllowedKeys.DATABASE__DOCUMENT__COPY__PARAMS)
    # def copy(self, couch_data):
    #     return couch_data
