from elasticsearch_dsl import Keyword
from elasticsearch_dsl.field import Object

from .default import DefaultMapping


class WorkspaceAcl(DefaultMapping):
    workspace = Object(
        properties={'id': Keyword(multi=True), 'name': Keyword(multi=True)}
    )
    user = Object(
        properties={'id': Keyword(multi=True), 'name': Keyword(multi=True)}
    )
    role = Object(
        properties={'id': Keyword(multi=True), 'name': Keyword(multi=True)}
    )
    policy = Object(
        properties={'id': Keyword(multi=True), 'name': Keyword(multi=True)}
    )
    resource = Object(
        properties={'id': Keyword(multi=True), 'name': Keyword(multi=True)}
    )


class Index:
    name = 'test.workspacevault.workspace_acl'
