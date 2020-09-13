from datetime import datetime

from elasticsearch_dsl import (Boolean, Completion, Date, Document, InnerDoc,
                               Keyword, Nested, Text, analyzer)
from elasticsearch_dsl.connections import connections

# html_strip = analyzer('html_strip',
#                       tokenizer="standard",
#                       filter=["standard", "lowercase", "stop", "snowball"],
#                       char_filter=["html_strip"]
#                       )

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])


class Comment(InnerDoc):
    author = Text(fields={'raw': Keyword()})
    content = Text(analyzer='snowball')
    created_at = Date()

    def age(self):
        return datetime.now() - self.created_at


class Post(Document):
    title = Text()
    title_suggest = Completion()
    created_at = Date()
    published = Boolean()
    category = Text(
        analyzer='simple',
        fields={'raw': Keyword()}
    )

    comments = Nested(Comment)

    class Index:
        name = 'post'

    def add_comment(self, author, content):
        self.comments.append(
            Comment(author=author, content=content, created_at=datetime.now()))

    def save(self, ** kwargs):
        self.created_at = datetime.now()
        return super().save(** kwargs)


# create the mappings in elasticsearch
Post.init()