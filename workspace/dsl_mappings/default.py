from datetime import datetime
import uuid

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Date, Document, InnerDoc, Keyword, Nested, Text
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.field import Double, Object
from uuid import uuid4


class Tags(InnerDoc):
    tag = Keyword()
    name = Text(analyzer='simple')
    weight = Double()


class References(InnerDoc):
    vault = Nested(properties={'id': Keyword()})
    app = Nested(properties={'id': Keyword()})
    object = Nested(
        properties={'id': Keyword(), 'name': Keyword(), 'type': Keyword()}
    )


class DefaultMapping(Document):
    id = Text()
    name = Text(analyzer='simple')
    slug = Keyword()
    description = Text(analyzer='simple')
    source = Nested(properties={'id': Keyword(), 'name': Keyword()})
    tags = Nested(Tags)
    created_at = Date(
        format="yyyy-MM-dd'T'HH:mm:ss.SSSSSS || yyyy-MM-dd'T'HH:mm:ss.SSS")
    updated_at = Date(
        format="yyyy-MM-dd'T'HH:mm:ss.SSSSSS || yyyy-MM-dd'T'HH:mm:ss.SSS")
    created_by = Object(properties={'id': Keyword(
        multi=True), 'name': Keyword(multi=True)})
    updated_by = Object(properties={'id': Keyword(), 'name': Keyword()})
    references = Nested(References)

    def add_created_by(self, id, name, commit=True):
        self.updated_by.name = 'Ramesh Pradhan'
        self.updated_by.id = uuid4()
        if commit:
            self.save()

    def save(self, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        return super().save(**kwargs)
