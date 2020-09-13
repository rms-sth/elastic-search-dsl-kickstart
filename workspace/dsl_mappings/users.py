from workspace.dsl_mappings.roles import UserMapping
from elasticsearch_dsl import Text
from elasticsearch_dsl.field import Nested

from .default import DefaultMapping


class UserMapping(DefaultMapping):
    first_name = Text(analyzer='simple')
    middle_name = Text(analyzer='simple')
    last_name = Text(analyzer='simple')
    gender = Text(analyzer='simple')
    email = Text(analyzer='simple')
    address = Nested(properties={'name': Text()})
    contact_number = Nested(properties={'contact_number': Text()})


class Index:
    name = 'test.workspacevault.users'
