from elasticsearch_dsl import Text

from .default import DefaultMapping


class Workspace(DefaultMapping):
    access_type = Text(analyzer='simple')

    class Index:
        name = 'test.workspacevault.workspaces'
