from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, UpdateByQuery

client = Elasticsearch()
ubq = UpdateByQuery(using=client, index="blog") \
      .query("match", title="python")   \
      .exclude("match", description="beta") \
      .script(source="ctx._source.likes++", lang="painless")

response = ubq.execute()