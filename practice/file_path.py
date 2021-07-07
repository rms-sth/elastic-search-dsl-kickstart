from datetime import datetime

from elasticsearch_dsl import (
    Boolean,
    Date,
    Document,
    InnerDoc,
    Keyword,
    Long,
    Nested,
    Object,
    Text,
    connections,
    analyzer,
    tokenizer,
)


path_hierarchy_tokenizer = tokenizer(
    name_or_instance="path_hierarchy_tokenizer",
    type="path_hierarchy",
    delimiter="/",
)

path_hierarchy_analyzer = analyzer(
    "path_hierarchy_analyzer",
    tokenizer=path_hierarchy_tokenizer,
    filter=["lowercase"],
)

path_hierarchy_tokenizer_reversed = tokenizer(
    name_or_instance="path_hierarchy_tokenizer_reversed",
    type="path_hierarchy",
    delimiter="/",
    reversed=True,
)

path_hierarchy_analyzer_reversed = analyzer(
    "path_hierarchy_analyzer_reversed",
    tokenizer=path_hierarchy_tokenizer_reversed,
    filter=["lowercase"],
)


class User(InnerDoc):
    """
    Class used to represent a de-normalized user stored on other objects.
    """

    id = Long(required=True)
    email = Text(fields={"keyword": Keyword()}, required=True)
    name = Keyword(normalizer="lowercase")
    status = Keyword(normalizer="lowercase")


class Reference(InnerDoc):
    """
    Class wrapper for nested comment objects.
    """

    reference_id = Long(required=True)
    reference_slug = Keyword(normalizer="lowercase")
    reference_object = Keyword(normalizer="lowercase")


class Shared(InnerDoc):
    """
    Class wrapper for nested comment objects.
    """

    user = Object(User, required=True)
    permission = Object(
        properties={
            "read": Boolean(),
            "write": Boolean(),
            "delete": Boolean(),
            "edit": Boolean(),
            "manage": Boolean(),
        }
    )
    created_at = Date(default_timezone="UTC")


class Starred(InnerDoc):
    """
    Class wrapper for nested comment objects.
    """

    user = Object(User, required=True)
    reference = Object(
        properties={
            "reference_id": Long(required=True),
            "reference_slug": Keyword(normalizer="lowercase"),
            "reference_object": Keyword(normalizer="lowercase"),
        }
    )
    created_at = Date(default_timezone="UTC")


class Doc(Document):
    """
    Base class for Files, Folders and Projects containing the common fields.
    """

    id = Long(required=True)
    name = Keyword(normalizer="lowercase")
    slug = Keyword(normalizer="lowercase")
    description = Text(analyzer="stop")
    type = Keyword(normalizer="lowercase")
    collection = Text(
        fields={
            "tree": Text(analyzer=path_hierarchy_analyzer),
            "tree_reversed": Text(analyzer=path_hierarchy_analyzer_reversed),
            "keyword": Keyword(normalizer="lowercase"),
        }
    )
    # collection = Text(analyzer=path_hierarchy_analyzer, fields={"keyword": Keyword()})
    tag_detail = Object()
    reference = Object()
    shared = Nested(Shared)
    starred = Nested(Starred)
    created_at = Date(default_timezone="UTC")
    updated_at = Date(default_timezone="UTC")
    created_by = Object(User, required=True)
    updated_by = Object(User, required=True)
    tag_detail = Object()

    # files data
    path = Text(analyzer="stop")
    proxy_path = Text(analyzer="stop")
    metadata = Object(
        properties={
            "size": Long(),
            "content_type": Text(),
        }
    )
    text_extraction_pending = Boolean()

    @classmethod
    def _matches(cls, hit):
        # Post is an abstract class, make sure it never gets used for
        # de-serialization
        return False

    class Index:
        name = "file_path"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    def add_shared(self, user, permission, created_at=None, commit=True):
        shared = Shared(
            user=user, permission=permission, created_at=created_at or datetime.now()
        )
        self.shared.append(shared)
        if commit:
            self.save()
        return shared

    def add_starred(self, user, created_at=None, commit=True):
        starred = Starred(user=user, created_at=created_at or datetime.now())
        self.starred.append(starred)
        if commit:
            self.save()
        return starred

    def save(self, **kwargs):
        # if there is no date, use now
        if self.created_at is None:
            self.created_at = datetime.now()
        return super().save(**kwargs)


def setup():
    """Create an IndexTemplate and save it into elasticsearch."""
    index_template = Doc._index.as_template("base")
    index_template.save()


if __name__ == "__main__":
    # initiate the default connection to elasticsearch
    connections.create_connection()

    # create index
    setup()

    # user objects to use
    ramesh1 = User(
        id=47,
        email="ramesrest@gmail.com",
        name="Ramesh Pradhan",
        status="active",
    )
    ramesh2 = User(
        id=42,
        email="ramesh.pradhan@chuchuro.com",
        name="Ramesh Pradhan",
        status="active",
    )

    reference = {
        "reference_id": 4439,
        "reference_slug": "python_venv_project_fa1c032e-17fc-4c9f-a479-a4f755622853",
        "reference_object": "projects",
    }
    permission = {
        "read": 1,
        "write": 1,
        "edit": 1,
        "delete": 1,
        "manage": 1,
    }

    data = {
        "id": 61460,
        "name": "www.YTS.MX.jpg",
        "slug": "wwwytsmxjpg_72803e60-04f4-4107-9c80-cff387285047",
        "description": "www.YTS.MX.jpg",
        "collection": "/123_681ef55d-a704-461e-a2ee-7d508e109bbf/77_c4902b0b-3c7c-4c37-b00f-0a75db43caa7/91_356d4974-6a66-42ef-8284-b06dd899ca27",
        "type": "file",
        "path": "/storage/933b49c3-995c-4795-a4f7-b75028215d55.jpg",
        "proxy_path": None,
        "text_extraction_pending": False,
        "metadata": {"size": "53226", "content_type": "image/jpeg"},
        "created_at": datetime.now(),
        "created_by": ramesh1,
        "updated_by": ramesh2,
        "tag_detail": {"client": "drc", "application": "docvault"},
    }

    # create a question object
    doc = Doc(**data)
    doc.add_shared(user=ramesh2, permission=permission)
    doc.add_starred(user=ramesh2)
    if doc.save():
        print("Data saved successfully.")

    data = {
        "id": 61460,
        "name": "www.YTS.MX.jpg",
        "slug": "wwwytsmxjpg_72803e60-04f4-4107-9c80-cff387285047",
        "description": "www.YTS.MX.jpg",
        "collection": "/123_681ef55d-a704-461e-a2ee-7d508e109bbf/77_c4902b0b-3c7c-4c37-b00f-0a75db43caa7",
        "type": "file",
        "path": "/storage/933b49c3-995c-4795-a4f7-b75028215d55.jpg",
        "proxy_path": None,
        "text_extraction_pending": False,
        "metadata": {"size": "53226", "content_type": "image/jpeg"},
        "created_at": datetime.now(),
        "created_by": ramesh1,
        "updated_by": ramesh2,
        "tag_detail": {"client": "drc", "application": "docvault"},
    }

    # create a question object
    doc = Doc(**data)
    doc.add_shared(user=ramesh2, permission=permission)
    doc.add_starred(user=ramesh2)
    if doc.save():
        print("Data saved successfully.")

    data = {
        "id": 61460,
        "name": "www.YTS.MX.jpg",
        "slug": "wwwytsmxjpg_72803e60-04f4-4107-9c80-cff387285047",
        "description": "www.YTS.MX.jpg",
        "collection": "/123_681ef55d-a704-461e-a2ee-7d508e109bbf",
        "type": "file",
        "path": "/storage/933b49c3-995c-4795-a4f7-b75028215d55.jpg",
        "proxy_path": None,
        "text_extraction_pending": False,
        "metadata": {"size": "53226", "content_type": "image/jpeg"},
        "created_at": datetime.now(),
        "created_by": ramesh1,
        "updated_by": ramesh2,
        "tag_detail": {"client": "drc", "application": "docvault"},
    }

    # create a question object
    doc = Doc(**data)
    doc.add_shared(user=ramesh2, permission=permission)
    doc.add_starred(user=ramesh2)
    if doc.save():
        print("Data saved successfully.")
