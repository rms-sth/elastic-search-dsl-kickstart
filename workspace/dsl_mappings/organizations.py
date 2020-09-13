from elasticsearch_dsl import Text
from elasticsearch_dsl.field import Nested

from .default import DefaultMapping


class OrganizationMapping(DefaultMapping):
    email = Text(analyzer='simple')
    address = Nested(properties={'name': Text()})
    contact_number = Nested(properties={'contact_number': Text()})


class Index:
    name = 'test.workspacevault.organizations'
