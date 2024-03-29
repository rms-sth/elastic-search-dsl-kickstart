from elasticsearch_dsl import Date, Document, InnerDoc, Keyword, Object
from elasticsearch_dsl.field import Nested


# class Media(InnerDoc):
#     id = Keyword(normalizer="lowercase")


# class DataMapping(Document):
#     class Index:
#         name = "dev.ramesh.docvault.test.data"

#     project_id = Keyword(normalizer="lowercase")
#     template_id = Keyword(normalizer="lowercase")
#     content = Object(required=True)
#     data_extracted_media_id = Object(Media)
#     status = Keyword()
#     created_by = Keyword(normalizer="lowercase")  # implies user_id
#     updated_by = Keyword(normalizer="lowercase")
#     created_at = Date(default_timezone="UTC")
#     updated_at = Date(default_timezone="UTC")


class ExtractedMedia(InnerDoc):
    id = Keyword(normalizer="lowercase")


class DataMapping(Document):
    class Index:
        name = "dev.ramesh.docvault.test.data"

    project_id = Keyword(normalizer="lowercase")
    template_id = Keyword(normalizer="lowercase")
    content = Object(required=True)
    data_extracted_media_id = Nested(ExtractedMedia)
    # data_extracted_media_id = Object(ExtractedMedia)
    status = Keyword()
    created_by = Keyword(normalizer="lowercase")  # implies user_id
    updated_by = Keyword(normalizer="lowercase")
    created_at = Date(default_timezone="UTC")
    updated_at = Date(default_timezone="UTC")

    def add_media_id(self, id: str, commit=False):
        self.data_extracted_media_id.append(ExtractedMedia(id=id))
        if commit:
            self.save()
