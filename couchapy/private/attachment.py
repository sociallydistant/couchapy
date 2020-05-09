import  couchapy.decorators as couch
import  functools

class _Attachment():
    _type = '/'
    _doc_key = 'docid'

    """
    Namespace class for design document related endpoints.

    This class is not intended for direct use and should be accessed through the database attribute of a CouchDB instance.
    """
    def __init__(self, parent, **kwargs):
        # TODO: rename this to reference the host couch instance
        self.parent = parent.parent
        self._db = parent._db
        self._predefined_segments = parent._predefined_segments
        self._type = '/'
        self._doc_key = 'docid'

    def headers(self, *args, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/document/attachments.html#head--db-docid-attname
        """
        @couch.endpoint(f'/:db:{self._type}:{self._doc_key}:/:attname:', method='head', query_keys=couch.AllowedKeys.DATABASE__ATTACHMENT__INFO_PARAMS)
        def attachment_headers(self, couch_data, **kwargs):
            return kwargs.get("response_headers", None)

        return attachment_headers(self, **kwargs)

    # TODO: implement ability for endpoint to return non-json data
    def get(self, *args, **kwargs):
        """
        See https://docs.couchdb.org/en/stable/api/document/attachments.html#get--db-docid-attname
        """
        @couch.endpoint(f'/:db:{self._type}:{self._doc_key}:/:attname:', query_keys=couch.AllowedKeys.DATABASE__ATTACHMENT__GET__PARAMS)
        def get_attachment(self, couch_data, **wargs):
            return wargs.get('response')
            # return couch_data['data'] if 'data' in couch_data else couch_data

        return get_attachment(self, **kwargs)

    # TODO: confirm ability to pass custom headers to endpoint decorator
    def save(self, *args, **kwargs):
        @couch.endpoint(f'/:db:{self._type}:{self._doc_key}:/:attname:', method='put', query_keys=couch.AllowedKeys.DATABASE__ATTACHMENT__SAVE__PARAMS)
        def save_attachment(self, couch_data, **wargs):
            return couch_data

        return save_attachment(self, *args, **kwargs)

    def delete(self, *args, **kwargs):
        @couch.endpoint(f'/:db:{self._type}:{self._doc_key}:/:attname:', method='delete', query_keys=couch.AllowedKeys.DATABASE__ATTACHMENT__DELETE__PARAMS)
        def delete_attachment(self, couch_data, **wargs):
            return couch_data

        return delete_attachment(self, **kwargs)


class _DesignDocAttachment(_Attachment):
    def __init__(self, parent, **kwargs):
        # TODO: rename this to reference the host couch instance
        self.parent = parent.parent
        self._db = parent._db
        self._predefined_segments = parent._predefined_segments
        self._type = '/_design/'
        self._doc_key = 'ddoc'
