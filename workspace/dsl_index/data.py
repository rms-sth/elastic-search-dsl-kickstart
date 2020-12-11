import uuid
from datetime import datetime
from uuid import uuid4

from elasticsearch_dsl.connections import connections
from elasticsearch import Elasticsearch

from ..dsl_mappings.data import DataMapping


class DataIndex:
    def __init__(self) -> None:
        self.es = Elasticsearch()
        connections.create_connection(hosts=["localhost"])

    def create_mapping(self):
        """
        create the mappings in elasticsearch
        """
        exists = self.es.indices.exists(index="dev.ramesh.docvault.test.data")
        if exists:
            print("New mapping exists. Cannot proceed further")
            return
        DataMapping.init()
        print("Creating mapping...")

    def create_new_mapping(self):
        """
        deletes existing mapping and create new mapping
        """
        exists = self.es.indices.exists(index="dev.ramesh.docvault.test.data")
        print(exists)
        if exists:
            print(
                "Old mapping exists. Deleting existing mapping and creating new one..."
            )
            self.delete_mapping()
        else:
            print("creating new mapping...")
        # create the mappings in elasticsearch
        DataMapping.init()

    def delete_mapping(self):
        """
        delete mapping / indices and ignores if no mapping found
        """
        self.es.indices.delete(index="dev.ramesh.docvault.test.data", ignore=[400, 404])

    def create_index(self):
        """
        create new Activity index
        """
        activity = DataMapping(
            meta={"id": uuid4()},
            name="Crecentral General Activity",
            slug="crecentral-general-Activity",
            description="It is the general Activity for crecentral.",
        )

        activity.add_created_by(uuid4(), "Ramesh Pradhan")

        activity.save()
        print(activity)
