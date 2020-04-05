import couchapy.decorators as couch
import couchapy.error


class Server():
    def __init__(self, **kwargs):
        self.session = kwargs.get('session', None)
        self._predefined_segments = {'node_name': '_local'}

    @couch.endpoint('/')
    def get_info(self, couch_data):
        return couch_data

    @couch.endpoint('/_up')
    def get_server_status(self, couch_data):
        return couch_data

    @couch.endpoint('/_active_tasks')
    def get_active_tasks(self, couch_data):
        return couch_data

    @couch.endpoint('/_all_dbs', query_keys=couch.AllowedKeys.SERVER__ALL_DBS__PARAMS)
    def get_database_names(self, couch_data):
        return couch_data

    @couch.endpoint('/_dbs_info', method='post', data_keys=couch.AllowedKeys.SERVER__DBS_INFO__PARAMS)
    def get_databases(self, couch_data):
        return couch_data

    @couch.endpoint('/_cluster_setup', query_keys=couch.AllowedKeys.SERVER__CLUSTER_SETUP__PARAMS)
    def get_cluster_setup(self, couch_data):
        return couch_data

    @couch.endpoint('/_cluster_setup', method='post', data_keys=couch.AllowedKeys.SERVER__CLUSTER_SETUP__DATA)
    def configure_cluster_setup(self, couch_data):
        return couch_data

    @couch.endpoint('/_db_updates', method='post', query_keys=couch.AllowedKeys.SERVER__DB_UPDATES__PARAMS)
    def get_database_updates(self, couch_data):
        return couch_data

    @couch.endpoint('/_membership')
    def get_membership(self, couch_data):
        return couch_data

    @couch.endpoint('/_replicate', method='post', data_keys=couch.AllowedKeys.SERVER__REPLICATE__DATA)
    def replicate(self, couch_data):
        return couch_data

    @couch.endpoint('/_scheduler/jobs', query_keys=couch.AllowedKeys.SERVER__SCHEDULER_JOBS__PARAMS)
    def get_replication_updates(self, couch_data):
        """
        Retrieves the status of replication jobs that are currently active.
        """
        return couch_data

    @couch.endpoint('/_scheduler/docs', query_keys=couch.AllowedKeys.SERVER__SCHEDULER_DOCS__PARAMS)
    def get_replication_docs(self, couch_data):
        """
        All Replication documents
        """
        return couch_data

    @couch.endpoint('/_scheduler/docs/:db:/_replicator', query_keys=couch.AllowedKeys.SERVER__SCHEDULER_DOCS__PARAMS)
    def get_replicator_docs(self, couch_data):
        """
        Replication documents for a specific replicator database
        """
        return couch_data

    @couch.endpoint('/_scheduler/docs/:db:/_replicator/:docid:')
    def get_replicator_doc(self, couch_data):
        """
        Retrives a single replication document for the specified replicator database
        """
        return couch_data

    @couch.endpoint('/_node/:node_name:/_stats')
    def get_node_server_stats(self, couch_data):
        """
        Get statistics for the running server with name :node_name:
        """
        return couch_data

    @couch.endpoint('/_node/:node_name:/_stats/:stat:')
    def get_node_server_stat(self, couch_data):
        """
        Get a section or subsection of the statistics for the running server with name :node_name:
        """
        return couch_data

    @couch.endpoint('/_node/:node_name:/_system')
    def get_node_system_stats(self, couch_data):
        """
        Get system statistics for the running server with name :node_name:
        """
        return couch_data

    @couch.endpoint('/_node/:node_name:/_restart', method='post')
    def restart_node(self, couch_data):
        """
        Restart the specified node
        """
        return couch_data

    @couch.endpoint('/_node/:node_name:/_config')
    def get_server_config(self, couch_data):
        """
        Gets the entire server configuration of the specified node.
        """
        return couch_data

    @couch.endpoint('/_node/:node_name:/_config/:key:')
    def get_config(self, couch_data):
        """
        Gets the server configuration section or key defined by :key: of the specified node.
        """
        return couch_data

    # TODO: implement put in endpoint decorator
    @couch.endpoint('/_node/:node_name:/_config/:key:', method='put')
    def set_config(self, couch_data):
        """
        Create or update the server configuration key defined by :key: of the specified node.
        """
        return couch_data

    @couch.endpoint('/_node/:node_name:/_config/:key:', method='delete')
    def delete_config(self, couch_data):
        """
        Delete the server configuration key defined by :key: of the specified node.
        """
        return couch_data

    @couch.endpoint('/_uuids', query_keys=couch.AllowedKeys.SERVER__UUIDS__PARAMS)
    def generate_uuids(self, couch_data):
        """
        Retrieves new UUIDS from the CouchDB server

        :param int count Number of uuids to generate (Default: 1).
        """
        if isinstance(couch_data, couchapy.error.CouchError):
            return couch_data

        if len(couch_data.get('uuids')) == 1:
            return couch_data.get('uuids')[0]

        return couch_data.get('uuids')

    @couch.endpoint('/_node/:node_name:/_system')
    def get_uptime(self, couch_data):
        """
        Get the up time, in seconds, for the specified node.

        :returns CouchError if an error occured accessing the couch api
        :returns int Number of seconds that the server has been running, or -1 if the uptime key is missing.

        Usage: couchdb_instance.get_uptime(node_name='_local')
        """
        return couch_data if isinstance(couch_data, couchapy.error.CouchError) else couch_data.get('uptime', -1)
