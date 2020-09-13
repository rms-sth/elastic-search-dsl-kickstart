from elasticsearch_dsl import Keyword
from elasticsearch_dsl.field import Object

from .default import DefaultMapping


class UserMapping(DefaultMapping):
    workspace = Object(
        properties={'id': Keyword(multi=True), 'name': Keyword(multi=True)}
    )


class Index:
    name = 'test.workspacevault.users'
