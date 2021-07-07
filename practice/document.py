#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

"""
Complex data model example modeling stackoverflow-like data.

It is used to showcase several key features of elasticsearch-dsl:

    * Object and Nested fields: see User and Comment classes and fields they
      are used in

        * method add_comment is used to add comments

    * Parent/Child relationship

        * See the Join field on Post creating the relationship between Question
          and Answer

        * Meta.matches allows the hits from same index to be wrapped in proper
          classes

        * to see how child objects are created see Question.add_answer

        * Question.search_answers shows how to query for children of a
          particular parent

"""
from datetime import datetime
from workspace.dsl_mappings import default

from elasticsearch_dsl import (
    Boolean,
    Date,
    Document,
    InnerDoc,
    Join,
    Keyword,
    Long,
    Nested,
    Object,
    Text,
    connections,
)
from elasticsearch_dsl.field import Integer


class User(InnerDoc):
    """
    Class used to represent a denormalized user stored on other objects.
    """

    id = Long(required=True)
    email = Text(fields={"keyword": Keyword()}, required=True)
    status = Keyword()


class Reference(InnerDoc):
    """
    Class wrapper for nested comment objects.
    """

    id = Long(required=True)
    slug = Keyword(normalizer="lowercase")
    object = Keyword()


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
            "id": Long(required=True),
            "object": Keyword(normalizer="lowercase"),
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
    tag_detail = Object()
    reference = Join(relations={"id": "", "slug": "", "object": ""})
    shared = Nested(Shared)
    starred = Nested(Shared)
    created_at = Date(default_timezone="UTC")
    updated_at = Date(default_timezone="UTC")
    created_by = Object(User, required=True)
    updated_by = Object(User, required=True)

    @classmethod
    def _matches(cls, hit):
        # Post is an abstract class, make sure it never gets used for
        # deserialization
        return False

    class Index:
        name = "documents"
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

    def add_starred(self, user, reference, created_at=None, commit=True):
        starred = Starred(
            user=user, reference=reference, created_at=created_at or datetime.now()
        )
        self.starred.append(starred)
        if commit:
            self.save()
        return starred

    def save(self, **kwargs):
        # if there is no date, use now
        if self.created is None:
            self.created = datetime.now()
        return super().save(**kwargs)

    def add_project(
        self,
        id,
        name,
        slug,
        description,
        reference,
        shared,
        starred,
        tag_detail,
        created_by,
        updated_by,
        type="project",
        created_at=None,
        updated_at=None,
        _object=None,
        commit=True,
    ):
        project = Project(
            # required make sure the answer is stored in the same shard
            _routing=self.meta.id,
            # since we don't have explicit index, ensure same index as self
            _index=self.meta.index,
            # set up the parent/child mapping
            reference={"id": self.meta.id, "slug": slug, "object": _object},
            _id=id,
            name=name,
            slug=slug,
            description=description,
            reference=reference,
            shared=shared,
            starred=starred,
            tag_detail=tag_detail,
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            updated_by=updated_by,
            type=type,
        )
        if commit:
            project.save()
        return project

    def add_media(
        self,
        id,
        name,
        slug,
        description,
        reference,
        shared,
        starred,
        tag_detail,
        metadata,
        text_extraction_pending,
        path,
        proxy_path,
        created_by,
        updated_by,
        type="project",
        created_at=None,
        updated_at=None,
        _object=None,
        commit=True,
    ):
        media = Media(
            # required make sure the answer is stored in the same shard
            _routing=self.meta.id,
            # since we don't have explicit index, ensure same index as self
            _index=self.meta.index,
            # set up the parent/child mapping
            reference={"id": self.meta.id, "slug": slug, "object": _object},
            _id=id,
            name=name,
            slug=slug,
            description=description,
            reference=reference,
            shared=shared,
            starred=starred,
            tag_detail=tag_detail,
            metadata=metadata,
            text_extraction_pending=text_extraction_pending,
            path=path,
            proxy_path=proxy_path,
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            updated_by=updated_by,
            type=type,
        )
        if commit:
            media.save()
        return media


class Project(Doc):
    @classmethod
    def _matches(cls, hit):
        """Use Question class for parent documents"""
        return hit["_source"]["reference"] == "project"

    @classmethod
    def search(cls, **kwargs):
        return cls._index.search(**kwargs).filter("term", reference="project")


class Media(Doc):
    # only for files
    metadata = Object(
        properties={
            "size": Long(),
            "content_type": Text(),
        }
    )
    text_extraction_pending = Boolean()
    path = Text(analyzer="stop")
    proxy_path = Text(analyzer="stop")

    @classmethod
    def _matches(cls, hit):
        """Use Question class for parent documents"""
        return hit["_source"]["reference"] == "media"

    @classmethod
    def search(cls, **kwargs):
        return cls._index.search(**kwargs).filter("term", reference="media")

    def search_answers(self):
        # search only our index
        s = Answer.search()
        # filter for answers belonging to us
        s = s.filter("parent_id", type="answer", id=self.meta.id)
        # add routing to only go to specific shard
        s = s.params(routing=self.meta.id)
        return s

    def get_answers(self):
        """
        Get answers either from inner_hits already present or by searching
        elasticsearch.
        """
        if "inner_hits" in self.meta and "answer" in self.meta.inner_hits:
            return self.meta.inner_hits.answer.hits
        return list(self.search_answers())

    def save(self, **kwargs):
        self.question_answer = "question"
        return super(Question, self).save(**kwargs)


class Answer(Post):
    is_accepted = Boolean()

    @classmethod
    def _matches(cls, hit):
        """Use Answer class for child documents with child name 'answer'"""
        return (
            isinstance(hit["_source"]["question_answer"], dict)
            and hit["_source"]["question_answer"].get("name") == "answer"
        )

    @classmethod
    def search(cls, **kwargs):
        return cls._index.search(**kwargs).exclude("term", question_answer="question")

    @property
    def question(self):
        # cache question in self.meta
        # any attributes set on self would be interpretted as fields
        if "question" not in self.meta:
            self.meta.question = Question.get(
                id=self.question_answer.parent, index=self.meta.index
            )
        return self.meta.question

    def save(self, **kwargs):
        # set routing to parents id automatically
        self.meta.routing = self.question_answer.parent
        return super(Answer, self).save(**kwargs)


def setup():
    """Create an IndexTemplate and save it into elasticsearch."""
    index_template = Post._index.as_template("base")
    index_template.save()


if __name__ == "__main__":
    # initiate the default connection to elasticsearch
    connections.create_connection()

    # create index
    setup()

    # user objects to use
    nick = User(
        id=47,
        signed_up=datetime(2017, 4, 3),
        username="fxdgear",
        email="nick.lang@elastic.co",
        location="Colorado",
    )
    honza = User(
        id=42,
        signed_up=datetime(2013, 4, 3),
        username="honzakral",
        email="honza@elastic.co",
        location="Prague",
    )

    # create a question object
    question = Question(
        _id=1,
        author=nick,
        tags=["elasticsearch", "python"],
        title="How do I use elasticsearch from Python?",
        body="""
        I want to use elasticsearch, how do I do it from Python?
        """,
    )
    question.save()
    answer = question.add_answer(honza, "Just use `elasticsearch-py`!")
