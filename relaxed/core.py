# TODO: figure out how to implement hooks
from functools import wraps
import requests
from re import sub


class CouchDB():
    """
    Exposes an interface for interating with a CouchDB server's REST API.

    Usage:
      couchDb = CouchDB([username=<user>[, password=<password>][,<arg=<value>])
    """

    def __init__(self, **kwargs):
      self._context_manager = False
      self.session = Session(**kwargs)
      self.server = Server(session=self.session)
      self.db = Database(session=self.session)

    def __enter__(self):
      self._context_manager = True
      return self

    def __exit__(self, type, value, traceback):
      self._context_manager = False


class CouchError():
  def __init__(self, **kwargs):
    self.error = kwargs.get('error', None)
    self.reason = kwargs.get('reason', None)
    self.status_code = kwargs.get('code', None)


class InvalidKeysException(Exception):
  """The passed data contains keys that are not allowed"""
  pass


class CouchDBDecorators():
  ALLOWED_KEYS__VIEW__GET = {'conflicts': bool, 'descending': bool,
                             'startkey': [], 'start_key': [],
                             'startkey_docid': str, 'start_key_doc_id': str,
                             'endkey': [], 'end_key': [],
                             'endkey_docid': str, 'end_key_doc_id': str,
                             'group': bool, 'group_level': int,
                             'include_docs': bool, 'attachments': bool, 'att_encoding_info': bool, 'inclusive_end': bool,
                             'key': [], 'keys': [[]],
                             'limit': int, 'skip': int, 'reduce': bool, 'sorted': bool,
                             'stable': bool, 'stale': str,
                             'update': str, 'update_seq': bool}

  ALLOWED_KEYS__DB__ALL_DOCS__POST = {'keys': []}
  ALLOWED_KEYS__DB__ALL_DOCS_QUERIES__POST = {'queries': []}
  ALLOWED_KEYS__DB__DESIGN_DOCS_QUERIES__POST = {'queries': []}
  ALLOWED_KEYS__DB__DESIGN_DOCS__POST = {'keys': []}
  ALLOWED_KEYS__DB__LOCAL_DOCS_QUERIES__POST = {'queries': []}
  ALLOWED_KEYS__PARAMS__DB__BULK_GET__POST = {'revs': bool}
  ALLOWED_KEYS__DATA__DB__BULK_GET__POST = {'docs': [{}]}
  ALLOWED_KEYS__PARAMS__DB__BULK_GET__POST = {'revs': bool}
  ALLOWED_KEYS__DATA__DB__BULK_DOCS__POST = {'docs': [{}], 'new_edits': bool }
  ALLOWED_KEYS__DATA__DB__FIND__POST = {'selector': {}, 'limit': int, 'skip': int,
                                        'sort': {}, 'fields': [], 'use_index': [], 'r': int,
                                        'bookmark': str, 'update': bool,
                                        'stable': bool, 'stale': str, 'execution_stats': bool}
  ALLOWED_KEYS__DATA__DB__INDEX__POST = {'index': {}, 'ddoc': str, 'name': str,
                                        'type': str, 'partial_filter_selector': {}}

  def _process_filter_format(filter_format, filter):
    if (filter_format is not None):
      for key in filter.keys():
        if key not in filter_format:
          raise InvalidKeysException("The provided filter does not meet the expected format.")

  def _build_uri(template: str, segments: dict):
    def replace_with_segment(matches):
      #  dynamic segments are expected, but not provided at all
      if segments is None and len(matches.groups()) > 0:
        identifier = matches.group(1)
        raise Exception((
          'Invalid URI. This endpoint contains dynamic segments, but none were provided.  '
          f'Expected segment definition for "{identifier}".  '
          'Did you forget to pass a uri_segments dict?'))
      # a specific segment not provided
      elif len(matches.groups()) == 1 and matches.group(1) not in segments:
        identifier = matches.group(1)
        raise Exception(f'Invalid URI. Expected a dynamic segment for "{identifier}", but none was provided.')
      else:
        return segments[matches.group(1)]

    return sub(':([\w_]+):', replace_with_segment, template)

  def endpoint(*args, **kwargs):
    endpoint = args[0]
    filter_format = kwargs.get('filter_format', None)
    request_method = kwargs.get('method', 'get')
    request_action = getattr(requests, request_method)
    def set_endpoint(*eargs):
      fn = eargs[0]

      @wraps(fn)
      def wrapper(self, *query_params, **kwargs):
        dynamic_segments = getattr(self, '_predefined_segments', {})
        dynamic_segments.update(kwargs.get('uri_segments', {}))

        #print(dynamic_segments)

        cookies = {'AuthSession': self.session.auth_token or None}
        uri = CouchDBDecorators._build_uri(endpoint, dynamic_segments)

        if ('filter' in kwargs):
          CouchDBDecorators._process_filter_format(filter_format, kwargs.get('filter'))

        if (request_method == 'post'):
          response = request_action(f'{self.session.address}{uri}', headers=self.session._headers, cookies=cookies, json=kwargs.get('filter'))
        else:
          response = request_action(f'{self.session.address}{uri}', headers=self.session._headers, cookies=cookies, params=kwargs.get('filter'))

        if (response.status_code == requests.codes['ok']):
          self.session.set_auth_token_from_headers(response.headers)
          ret_val = response.json()
        else:
          result = response.json()
          result['code'] = response.status_code
          ret_val = CouchError(**result)

        return fn(self, ret_val)
      return wrapper
    return set_endpoint

from .session import Session
from .server import Server
from .db import Database
