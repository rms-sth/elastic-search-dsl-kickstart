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
        name = 'dev.ramesh.docvault.test.docs'

    metadata = Object(
        properties={
            "size": Object(properties={"values": Integer(), "unit": Keyword()}),
            "created_timestamp": Date(
                default_timezone="UTC",
                # format="yyyy-MM-dd'T'HH:mm:ss.SSSSSSZ || yyyy-MM-dd'T'HH:mm:ss.SSSZ",
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
                        # format="yyyy-MM-dd'T'HH:mm:ss.SSSSSSZ || yyyy-MM-dd'T'HH:mm:ss.SSSZ",
                    ),
                    "end_timestamp": Date(
                        default_timezone="UTC",
                        # format="yyyy-MM-dd'T'HH:mm:ss.SSSSSSZ || yyyy-MM-dd'T'HH:mm:ss.SSSZ",
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
                # format="yyyy-MM-dd'T'HH:mm:ss.SSSSSSZ || yyyy-MM-dd'T'HH:mm:ss.SSSZ",
            ),
            "end_timestamp": Date(
                default_timezone="UTC",
                # format="yyyy-MM-dd'T'HH:mm:ss.SSSSSSZ || yyyy-MM-dd'T'HH:mm:ss.SSSZ",
            ),
        }
    )
