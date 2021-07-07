import uuid
from datetime import datetime
from uuid import uuid4

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Date, Document, Float, InnerDoc, Keyword, Nested, Text
from elasticsearch_dsl.connections import connections


class Source(InnerDoc):
    id = Keyword()
    name = Keyword(normalizer="lowercase")


class Workspace(InnerDoc):
    id = Keyword()
    name = Text()


class Tag(InnerDoc):
    tag = Keyword(normalizer="lowercase")
    type = Keyword(normalizer="lowercase")
    weight = Float()


class CreatedBy(InnerDoc):
    id = Keyword()


class References(InnerDoc):
    vault = Nested(properties={"name": Keyword(normalizer="lowercase")})
    app = Nested(properties={"id": Keyword()})
    object = Nested(
        properties={"id": Keyword(), "type": Keyword(normalizer="lowercase")}
    )


es_index = "dev.ramesh.docvault.docs.activities"


class DocActivityMapping(Document):
    class Index:
        name = es_index

    name = Keyword(normalizer="lowercase")
    slug = Keyword(normalizer="lowercase")
    description = Text(analyzer="stop")
    source = Nested(Source)
    workspaces = Nested(Workspace)
    tags = Nested(Tag)
    references = Nested(References)

    created_at = Date(default_timezone="UTC")
    updated_at = Date(default_timezone="UTC")
    created_by = Keyword(normalizer="lowercase")
    updated_by = Keyword(normalizer="lowercase")

    doc_id = Keyword()
    doc_type = Keyword(normalizer="lowercase")
    activity_template_id = Keyword()
    activity_template_slug = Keyword()
    action = Keyword(normalizer="lowercase")
    status = Keyword()


class DocActivityTemplate:
    def __init__(self) -> None:
        self.es = Elasticsearch()
        connections.create_connection(hosts=["localhost"])

    def create_mapping(self):
        """
        create the mappings in elasticsearch
        """
        exists = self.es.indices.exists(index=es_index)
        if exists:
            print("New mapping exists. Cannot proceed further")
            return
        DocActivityMapping.init()
        print("Creating mapping...")

    def create_new_mapping(self):
        """
        deletes existing mapping and create new mapping
        """
        exists = self.es.indices.exists(index=es_index)
        print(exists)
        if exists:
            print(
                "Old mapping exists. Deleting existing mapping and creating new one..."
            )
            self.delete_mapping()
        else:
            print("creating new mapping...")
        # create the mappings in elasticsearch
        DocActivityMapping.init()

    def delete_mapping(self):
        """
        delete mapping / indices and ignores if no mapping found
        """
        self.es.indices.delete(index=es_index, ignore=[400, 404])

    def create_index(self):
        """
        create new Activity index
        """
        activity = DocActivityMapping(
            meta={"id": uuid4()},
            name="Crecentral General Activity",
            slug="crecentral-general-Activity",
            description="It is the general Activity for crecentral.",
        )

        activity.add_created_by(uuid4(), "Ramesh Pradhan")

        activity.save()
        print(activity)


data = DocActivityTemplate()
data.create_new_mapping()