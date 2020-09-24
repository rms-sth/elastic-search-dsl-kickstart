from datetime import datetime
from uuid import uuid4

from elasticsearch_dsl import Date, Document, InnerDoc, Keyword, Nested, Text
from elasticsearch_dsl.field import Double, Float, Object


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
        format="yyyy-MM-dd'T'HH:mm:ss.SSSSSS || yyyy-MM-dd'T'HH:mm:ss.SSS"
    )
    updated_at = Date(
        format="yyyy-MM-dd'T'HH:mm:ss.SSSSSS || yyyy-MM-dd'T'HH:mm:ss.SSS"
    )
    created_by = Object(
        properties={'id': Keyword(multi=True), 'name': Keyword(multi=True)}
    )
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


class ElasticsearchBaseDocument(Document):
    class Source(InnerDoc):
        id = Keyword()
        name = Keyword(normalizer="lowercase")

    class Workspace(InnerDoc):
        id = Keyword()
        name = Keyword()

    class Tag(InnerDoc):
        tag = Keyword()
        type = Text()
        weight = Float()

    class CreatedBy(InnerDoc):
        id = Keyword()
        name = Keyword(normalizer="lowercase")

    id = Keyword()
    name = Keyword(normalizer="lowercase")
    slug = Keyword()
    description = Text(analyzer="stop")
    source = Nested(Source)
    workspaces = Nested(Workspace)
    tags = Nested(Tag)
    references = Nested(
        properties={
            "vault": {"properties": {"id": Keyword()}},
            "app": {"properties": {"id": Keyword()}},
            "object": {"properties": {"id": Keyword(), "type": Keyword()}},
        }
    )
    created_at = Date(
        default_timezone="UTC",
        format="yyyy-MM-dd'T'HH:mm:ss.SSSSSS || yyyy-MM-dd'T'HH:mm:ss.SSS",
    )
    updated_at = Date(
        default_timezone="UTC",
        format="yyyy-MM-dd'T'HH:mm:ss.SSSSSS || yyyy-MM-dd'T'HH:mm:ss.SSS",
    )
    created_by = Object(
        properties={"id": Keyword(multi=True), "name": Keyword(multi=True)}
    )