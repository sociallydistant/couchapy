from .core import CouchDBDecorators, CouchError


class Database():
  __ALLOWED_KEYS__DB__PUT = {'q': int, 'n': int}
  __ALLOWED_KEYS__DB__POST = {'batch': str}


  def __init__(self, **kwargs):
    self.session = kwargs.get('session', None)
    self._db = kwargs.get('db', '_global_changes')
    self._predefined_segments = {'db': self._db}

  @CouchDBDecorators.endpoint('/:db:', method='head')
  def headers(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:', method='head')
  def exists(self, couch_data):
    """
    Convenience method

    :returns CouchError if an error occured accessing the couch api
    :returns bool True if the database exists, otherwise false.
    """
    return False if isinstance(couch_data, CouchError) else True

  @CouchDBDecorators.endpoint('/:db:')
  def get(self, couch_data):
    return couch_data

  # TODO: build out decorators to handle status codes 201, 202.  Need to be able to handle
  # different cases for different endpoints.  Good solution is to allow a pre and post
  # handler to be supplied into the function?
  # i.e.  CouchDB.db.get(db=mydb, prefetch=do_this_before_request, post_fetch=do_this_after_response)
  @CouchDBDecorators.endpoint('/:db:', method='put', query_keys=__ALLOWED_KEYS__DB__PUT)
  def create(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:', method='delete')
  def delete(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:', method='post', query_keys=__ALLOWED_KEYS__DB__POST)
  def save(self, couch_data):
    """
    Saves a document to the specified database

    :returns CouchError if an error occured accessing the couch api
    """
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_ensure_full_commit', method='post')
  def flush(self, couch_data):
    """
    Force a manual request to commit documents created, updated, or deleted using CouchDB batch mode to persistent
    storage.

    See: http://docs.couchdb.org/en/stable/api/database/common.html#batch-mode-writes

    :returns CouchError if an error occured accessing the couch api
    """
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_all_docs', query_keys=CouchDBDecorators.ALLOWED_KEYS__VIEW__GET)
  def get_docs(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_all_docs', method='post', data_keys=CouchDBDecorators.ALLOWED_KEYS__DB__ALL_DOCS__POST)
  def get_docs_by_key(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_design_docs', query_keys=CouchDBDecorators.ALLOWED_KEYS__VIEW__GET)
  def get_design_docs(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_design_docs', method='post', data_keys=CouchDBDecorators.ALLOWED_KEYS__DB__DESIGN_DOCS__POST)
  def get_design_docs_by_key(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_all_docs/queries', method='post', data_keys=CouchDBDecorators.ALLOWED_KEYS__DB__ALL_DOCS_QUERIES__POST)
  def get_docs_by_query(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_design_docs/queries', method='post', data_keys=CouchDBDecorators.ALLOWED_KEYS__DB__DESIGN_DOCS_QUERIES__POST)
  def get_design_docs_by_query(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_local_docs/queries', method='post', data_keys=CouchDBDecorators.ALLOWED_KEYS__DB__LOCAL_DOCS_QUERIES__POST)
  def get_local_docs_by_query(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_bulk_get', method='post',
                              data_keys=CouchDBDecorators.ALLOWED_KEYS__DATA__DB__BULK_GET__POST,
                              query_keys=CouchDBDecorators.ALLOWED_KEYS__PARAMS__DB__BULK_GET__POST)
  def bulk_get(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_bulk_docs', method='post', data_keys=CouchDBDecorators.ALLOWED_KEYS__DATA__DB__BULK_DOCS__POST)
  def bulk_save(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_find', method='post', data_keys=CouchDBDecorators.ALLOWED_KEYS__DATA__DB__FIND__POST)
  def find(self, couch_data):
    return couch_data

  # TODO: need both query params and post data keys here
  @CouchDBDecorators.endpoint('/:db:/_index', method='post', query_keys=CouchDBDecorators.ALLOWED_KEYS__DATA__DB__INDEX__POST)
  def save_index(self, couch_data):
    return couch_data

  @CouchDBDecorators.endpoint('/:db:/_index')
  def get_indices(self, couch_data):
    return couch_data
