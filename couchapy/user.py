# class User():
#   class __This():
#     __allowed_keys = ['session', 'db']
#
#     def __init__(self, **kwargs):
#       for k in kwargs.keys():
#         if k in self.__allowed_keys:
#           self.__setattr__(k, kwargs.get(k, None))
#
#     def create(self, name, password, **kwargs):
#       docid = f'org.couchdb.user:{name}'
#       userdoc = {'name': name, 'password': password, 'roles': kwargs.get('roles', []), 'type': "user"}
#       userdoc.update(**kwargs)
#       return self.db.save_named_doc(uri_segments={'db': '_users', 'docid': docid}, data=userdoc)
#
#     def get(self, id):
#       docid = f'org.couchdb.user:{id}';
#       return self.db.get_doc(uri_segments={'db': '_users', 'docid': docid})
#
#   __self = None
#
#   def __init__(self, **kwargs):
#     if not User.__self:
#       User.__self = User.__This(**kwargs)
#     else:
#       for k in kwargs.keys():
#         self.__self.__setattr__(k, kwargs.get(k, getattr(self.__self, k)))
#
#   def __getattr__(self, name):
#     return getattr(self.__self, name)
