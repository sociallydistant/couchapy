from .core import RelaxedDecorators, CouchError, AllowedKeys


class Database():
  def __init__(self, **kwargs):
    self.session = kwargs.get('session', None)
    self._db = kwargs.get('db', '_global_changes')
    self._predefined_segments = {'db': self._db}

  @RelaxedDecorators.endpoint('/:db:', method='head')
  def headers(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:', method='head')
  def exists(self, couch_data):
    """
    Convenience method

    :returns CouchError if an error occured accessing the couch api
    :returns bool True if the database exists, otherwise false.
    """
    return False if isinstance(couch_data, CouchError) else True

  @RelaxedDecorators.endpoint('/:db:')
  def get(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:', method='put', query_keys=AllowedKeys.DATABASE__DB__CREATE_PARAMS)
  def create(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:', method='delete')
  def delete(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:', method='post', query_keys=AllowedKeys.DATABASE__DB__SAVE__PARAMS)
  def save_doc(self, couch_data):
    """
    Saves a document to the specified database

    :returns CouchError if an error occured accessing the couch api
    """
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_ensure_full_commit', method='post')
  def flush(self, couch_data):
    """
    Force a manual request to commit documents created, updated, or deleted using CouchDB batch mode to persistent
    storage.

    See: http://docs.couchdb.org/en/stable/api/database/common.html#batch-mode-writes

    :returns CouchError if an error occured accessing the couch api
    """
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_all_docs', query_keys=AllowedKeys.VIEW__PARAMS)
  def get_docs(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_all_docs', method='post', data_keys=AllowedKeys.DATABASE__ALL_DOCS__DATA)
  def get_docs_by_key(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design_docs', query_keys=AllowedKeys.VIEW__PARAMS)
  def get_design_docs(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design_docs', method='post', data_keys=AllowedKeys.DATABASE__DESIGN_DOCS__DATA)
  def get_design_docs_by_key(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_all_docs/queries', method='post', data_keys=AllowedKeys.DATABASE__ALL_DOCS_QUERIES__DATA)
  def get_docs_by_query(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_design_docs/queries', method='post', data_keys=AllowedKeys.DATABASE__DESIGN_DOCS_QUERIES__DATA)
  def get_design_docs_by_query(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_local_docs/queries', method='post', data_keys=AllowedKeys.DATABASE__LOCAL_DOCS_QUERIES__DATA)
  def get_local_docs_by_query(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_bulk_get', method='post',
                              data_keys=AllowedKeys.DATABASE__BULK_GET__DATA,
                              query_keys=AllowedKeys.DATABASE__BULK_GET__PARAMS)
  def bulk_get(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_bulk_docs', method='post', data_keys=AllowedKeys.DATABASE__BULK_DOCS__DATA)
  def bulk_save(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_find', method='post', data_keys=AllowedKeys.DATABASE__FIND__DATA)
  def find(self, couch_data):
    return couch_data

  # TODO: need both query params and post data keys here
  @RelaxedDecorators.endpoint('/:db:/_index', method='post', data_keys=AllowedKeys.DATABASE__INDEX__DATA)
  def save_index(self, couch_data):
    return couch_data

  @RelaxedDecorators.endpoint('/:db:/_index', query_keys=AllowedKeys.VIEW__PARAMS)
  def get_indices(self, couch_data):
    return couch_data
