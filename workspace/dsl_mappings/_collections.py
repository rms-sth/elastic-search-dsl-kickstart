from workspace.dsl_mappings.default import ElasticsearchBaseDocument
from elasticsearch_dsl import (
    Date,
    Field,
    InnerDoc,
    Integer,
    Keyword,
    Nested,
    Object,
    Text,
    analyzer,
)


class CollectionMapping(ElasticsearchBaseDocument):
    class Index:
        name = 'dev.ramesh.docvault.test.collections'
    status = Keyword()
   
