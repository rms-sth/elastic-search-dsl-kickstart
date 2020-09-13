from elasticsearch_dsl import Keyword
from elasticsearch_dsl.field import Object

from .default import DefaultMapping


class WorkspaceUserMapping(DefaultMapping):
    workspace = Object(
        properties={'id': Keyword(multi=True), 'name': Keyword(multi=True)}
    )
    users = Object(
        properties={'id': Keyword(multi=True), 'name': Keyword(multi=True)}
    )


class Index:
    name = 'test.workspacevault.workspace_users'
