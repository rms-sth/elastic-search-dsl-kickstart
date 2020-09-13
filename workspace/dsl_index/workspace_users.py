import uuid
from datetime import datetime
from uuid import uuid4

from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch

from ..dsl_mappings.workspace_users import WorkspaceUserMapping


class WorkSpaceUserIndex:
    def __init__(self) -> None:
        self.es = Elasticsearch()
        connections.create_connection(hosts=['localhost'])

    def create_mapping(self):
        """
        create the mappings in elasticsearch
        """
        exists = self.es.indices.exists(
            index="test.workspacevault.workspace_users"
        )
        if exists:
            print('New mapping exists. Cannot proceed further')
            return
        WorkspaceUserMapping.init()
        print('Creating mapping...')

    def create_new_mapping(self):
        """
        deletes existing mapping and create new mapping
        """
        exists = self.es.indices.exists(
            index="test.workspacevault.workspace_users")
        if exists:
            print('New mapping exists. Deleting existing mapping and creating new one...')
            self.delete_mapping()

        # create the mappings in elasticsearch
        WorkspaceUserMapping.init()

    def delete_mapping(self):
        """
        delete mapping / indices and ignores if no mapping found
        """
        self.es.indices.delete(
            index='test.workspacevault.workspace_users',
            ignore=[400, 404]
        )

    def create_index(self):
        """
        create new Activity index
        """
        activity = WorkspaceUserMapping(
            meta={'id': uuid4()},
            name='Crecentral General Activity',
            slug='crecentral-general-Activity',
            description='It is the general Activity for crecentral.',
        )

        activity.add_created_by(uuid4(), 'Ramesh Pradhan')

        activity.save()
        print(activity)
