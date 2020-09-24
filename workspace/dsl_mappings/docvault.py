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


class MediaMapping(ElasticsearchBaseDocument):
    class Index:
        name = 'test.docvault.docs'

    metadata = Object(
        properties={
            "size": Object(properties={"values": Integer(), "unit": Keyword()}),
            "created_timestamp": Date(
                default_timezone="UTC",
                format="yyyy-MM-dd'T'HH:mm:ss.SSSSSS || yyyy-MM-dd'T'HH:mm:ss.SSS",
            ),
            "meme_type": Text(),
        }
    )
    status = Keyword()
    content = Keyword()
    processing = Object(
        properties={
            "indexing": Object(
                properties={
                    "status": Integer(),
                    "start_timestamp": Date(
                        default_timezone="UTC",
                        format="yyyy-MM-dd'T'HH:mm:ss.SSSSSS || yyyy-MM-dd'T'HH:mm:ss.SSS",
                    ),
                    "end_timestamp": Date(
                        default_timezone="UTC",
                        format="yyyy-MM-dd'T'HH:mm:ss.SSSSSS || yyyy-MM-dd'T'HH:mm:ss.SSS",
                    ),
                }
            )
        }
    )
    watermarking = Object(
        properties={
            "status": Integer(),
            "start_timestamp": Date(
                default_timezone="UTC",
                format="yyyy-MM-dd'T'HH:mm:ss.SSSSSS || yyyy-MM-dd'T'HH:mm:ss.SSS",
            ),
            "end_timestamp": Date(
                default_timezone="UTC",
                format="yyyy-MM-dd'T'HH:mm:ss.SSSSSS || yyyy-MM-dd'T'HH:mm:ss.SSS",
            ),
        }
    )
