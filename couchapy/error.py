
class CouchError():
    def __init__(self, **kwargs):
        self.error = kwargs.get('error', None)
        self.reason = kwargs.get('reason', None)
        self.status_code = kwargs.get('code', None)
