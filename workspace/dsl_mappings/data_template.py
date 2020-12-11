from elasticsearch_dsl import Date, Keyword, Object, Text
from elasticsearch_dsl.document import Document


class DataTemplate(Document):
    class Index:
        name = "dev.ramesh.docvault.test.datatemplate"

    title = Keyword(normalizer="lowercase")
    slug = Keyword(normalizer="lowercase")
    description = Text(analyzer="stop")
    forms = Object()
    created_by = Keyword(normalizer="lowercase")  # implies user_id
    updated_by = Keyword(normalizer="lowercase")
    created_at = Date(default_timezone="UTC")
    updated_at = Date(default_timezone="UTC")
