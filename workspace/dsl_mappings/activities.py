from elasticsearch_dsl import Keyword, Text
from elasticsearch_dsl.field import Object

from .default import DefaultMapping


class ActivityMapping(DefaultMapping):
    workspace = Object(
        properties={'id': Keyword(multi=True), 'name': Keyword(multi=True)}
    )
    user = Object(
        properties={'id': Keyword(multi=True), 'name': Keyword(multi=True)}
    )
    message = Text(analyzer='simple')
    action = Text(analyzer='simple')

    class Index:
        name = 'test.workspacevault.activities'
