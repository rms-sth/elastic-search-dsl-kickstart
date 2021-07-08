from colorama import init

init()
import random
import string
import time
import uuid
from datetime import datetime

from colorama import Style
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
    analyzer,
    connections,
    tokenizer,
)
from termcolor import colored

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
    Class wrapper for reference objects.
    """

    reference_id = Long(required=True)
    reference_slug = Keyword(normalizer="lowercase")
    reference_object = Keyword(normalizer="lowercase")


class Shared(InnerDoc):
    """
    Class wrapper for nested shared objects.
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
    Class wrapper for nested starred objects.
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
    name = Text(
        fields={
            "text": Text(),
            "keyword": Keyword(normalizer="lowercase"),
        }
    )
    # name = Keyword(normalizer="lowercase")
    slug = Keyword(normalizer="lowercase")
    description = Text(analyzer="stop")
    type = Keyword(normalizer="lowercase")
    xpath = Text(
        fields={
            "tree": Text(analyzer=path_hierarchy_analyzer),
            "tree_reversed": Text(analyzer=path_hierarchy_analyzer_reversed),
            "keyword": Keyword(normalizer="lowercase"),
        }
    )
    # xpath = Text(analyzer=path_hierarchy_analyzer, fields={"keyword": Keyword()})
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


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def get_random_slug():
    result_str = get_random_string(8) + str(uuid.uuid4())
    return result_str


def get_random_extension():
    valid_extensions = ["jpg", "png", "exe", "xls", "json", "pdf", "html"]
    return random.choice(valid_extensions)


def get_random_xpath(min=10, max=100):
    length = random.randint(min, max)
    s = ""
    for _ in range(length):
        s = s + f"/{uuid.uuid4()}"
    return s


def get_xpath(length=15):
    s = ""
    for _ in range(length):
        s = s + f"/{uuid.uuid4()}"
    return s


def get_random_document():
    valid_extensions = ["file", "folder", "project"]
    return random.choice(valid_extensions)


def get_random_path():
    path = f"/storage/{uuid.uuid4()}.{get_random_extension()}"
    return path


def get_random_pending():
    pending = [True, False]
    return random.choice(pending)


def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, "%m/%d/%Y %I:%M %p", prop)


def get_random_user():
    users = [ramesh1, ramesh2]
    return random.choice(users)


def import_random_data(xpath_length=10, child_docs=100):
    """import random data to ES

    Args:
        xpath_length (int, optional): length of xpath to create. Defaults to 10.
        child_docs (int, optional): no of child in each child docs. Defaults to 100.
    Eg:
        data = {
            "id": 61460,
            "name": "www.YTS.MX.jpg",
            "slug": "wwwytsmxjpg_72803e60-04f4-4107-9c80-cff387285047",
            "description": "www.YTS.MX.jpg",
            "xpath": "/123_681ef55d-a704-461e-a2ee-7d508e109bbf",
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
    """
    extension = get_random_extension()
    name = f"{get_random_string(12)}.{extension}"
    description = str(name) + get_random_string(150)
    slug = get_random_slug()
    xpath = get_random_xpath(4, 15)
    type = get_random_document()
    text_extraction_pending = get_random_pending()
    path = get_random_path()
    created_at = random_date("1/1/2008 1:30 PM", "1/1/2021 4:50 AM", random.random())
    created_by = get_random_user()
    updated_by = get_random_user()
    # xpath = get_random_xpath(4, 15)
    xpath = get_xpath(xpath_length)
    tree_split = xpath.split("/")

    for i in range(1, len(tree_split) + 1):
        xpath = "/".join(tree_split[:i])
        print(
            f"{Style.BRIGHT}==============================================================================================================================================="
        )
        print(i)
        print(colored(xpath or "/", "green"))
        for _ in range(child_docs):
            name = f"{get_random_string(12)}.{extension}"
            description = str(name) + get_random_string(150)
            slug = get_random_slug()
            type = get_random_document()
            text_extraction_pending = get_random_pending()
            path = get_random_path()
            created_at = random_date(
                "1/1/2008 1:30 PM", "1/1/2021 4:50 AM", random.random()
            )
            data = {
                "id": 61460,
                "name": name,
                "slug": slug,
                "description": description,
                "xpath": xpath or "/",
                "type": type,
                "path": path,
                "text_extraction_pending": text_extraction_pending,
                "created_at": created_at,
                "created_by": created_by,
                "updated_by": updated_by,
            }

            # create a question object
            doc = Doc(**data)
            doc.add_shared(user=created_by, permission=permission)
            doc.add_starred(user=updated_by)


if __name__ == "__main__":
    connections.create_connection()

    setup()

    import_random_data(xpath_length=10, child_docs=10)
