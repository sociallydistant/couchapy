import  couchapy.decorators as couch
import  couchapy.error
import  couchapy.private.changes as _changes
import  couchapy.private.design as _design
import  couchapy.private.document as _docs
import  couchapy.private.local as _local
import  couchapy.private.revisions as _revs
import  couchapy.private.security as _security


class Database():
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self._db = kwargs.get('db', '_global_changes')
        self._predefined_segments = kwargs.get('predefined_segments', {'db': self._db})
        self.revs = _revs._Revisions(self)
        self.security = _security._Security(self)
        self.design = _design._DesignDocument(self)
        self.local = _local._LocalDocuments(self)
        self.docs = _docs._Documents(self)
        self.changes = _changes._DatabaseChanges(self)

    @couch.endpoint('/:db:', method='head')
    def headers(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/database/common.html#db
        """
        return kwargs.get("response_headers", None)

    @couch.endpoint('/:db:', method='head')
    def exists(self, couch_data, **kwargs):
        """
        Convenience method

        :returns CouchError if an error occured accessing the couch api
        :returns bool True if the database exists, otherwise false.

        See https://docs.couchdb.org/en/stable/api/database/common.html#db
        """
        status_code = kwargs.get("status_code", None)

        if status_code != 200:
            return False
        elif isinstance(couch_data, couchapy.error.CouchError):
            return False
        else:
            return True

    @couch.endpoint('/:db:')
    def info(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/database/common.html#get--db
        """
        return couch_data

    @couch.endpoint('/:db:', method='post', query_keys=couch.AllowedKeys.DATABASE__DB__SAVE__PARAMS)
    def save(self, couch_data, **kwargs):
        """
        Saves a document to the specified database

        :returns CouchError if an error occured accessing the couch api

        See https://docs.couchdb.org/en/stable/api/database/common.html#post--db
        """
        return couch_data

    @couch.endpoint('/:db:/_ensure_full_commit', method='post')
    def flush(self, couch_data, **kwargs):
        """
        Force a manual request to commit documents created, updated, or deleted using CouchDB batch mode to persistent
        storage.

        Note: Changed in CouchDB 3.0.0: Deprecated; endpoint is a no-op.

        :returns CouchError if an error occured accessing the couch api

        See: https://docs.couchdb.org/en/stable/api/database/compact.html#db-ensure-full-commit
        """
        return couch_data

    @couch.endpoint('/:db:/_compact', method='post')
    def compact(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/database/compact.html#db-compact
        """
        return couch_data

    @couch.endpoint('/:db:/_purge', method='post')
    def purge(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/database/misc.html#post--db-_purge
        """
        return couch_data

    @couch.endpoint('/:db:/_purged_infos_limit')
    def get_purge_limit(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/database/misc.html#get--db-_purged_infos_limit
        """
        return couch_data

    @couch.endpoint('/:db:/_purged_infos_limit', method='put')
    def set_purge_limit(self, couch_data, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/database/misc.html#put--db-_purged_infos_limit
        """
        return couch_data

    @couch.endpoint('/:db:/_bulk_get', method='post',
                    data_keys=couch.AllowedKeys.DATABASE__BULK_GET__DATA,
                    query_keys=couch.AllowedKeys.DATABASE__BULK_GET__PARAMS)
    def bulk_get(self, couch_data, **kwargs):
        return couch_data

    @couch.endpoint('/:db:/_bulk_docs', method='post', data_keys=couch.AllowedKeys.DATABASE__BULK_DOCS__DATA)
    def bulk_save(self, couch_data, **kwargs):
        return couch_data

    @couch.endpoint('/:db:/_find', method='post', data_keys=couch.AllowedKeys.DATABASE__FIND__DATA)
    def find(self, couch_data, **kwargs):
        return couch_data

    # TODO: confirm body or query parameters.  couchdb docs suggest query parameters and not json body data
    @couch.endpoint('/:db:/_index', method='post', data_keys=couch.AllowedKeys.DATABASE__INDEX__DATA)
    def save_index(self, couch_data, **kwargs):
        return couch_data

    @couch.endpoint('/:db:/_index', query_keys=couch.AllowedKeys.VIEW__PARAMS)
    def get_indices(self, couch_data, **kwargs):
        return couch_data

    @couch.endpoint('/:db:/_index/:ddoc:/json/:index:')
    def get_index(self, couch_data, **kwargs):
        return couch_data

    @couch.endpoint('/:db:/_index/:ddoc:/json/:index:', method='delete')
    def delete_index(self, couch_data, **kwargs):
        return couch_data

    @couch.endpoint('/:db:/_explain', method='post', data_keys=couch.AllowedKeys.DATABASE__FIND__DATA)
    def explain(self, couch_data, **kwargs):
        return couch_data

    @couch.endpoint('/:db:/_shards')
    def get_shards(self, couch_data, **kwargs):
        return couch_data

    @couch.endpoint('/:db:/_shards/:shard:')
    def get_shard(self, couch_data, **kwargs):
        return couch_data

    @couch.endpoint('/:db:/_sync_shards', method='post')
    def sync_shards(self, couch_data, **kwargs):
        return couch_data
