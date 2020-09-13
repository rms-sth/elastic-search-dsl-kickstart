from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


client = Elasticsearch()

# s = Search(using=client)


s = Search(index='test.workspacevault.workspaces').using(client).query("match", name="Crecentral General Workspace")
# print(s.to_dict())

response = s.execute()

# print(response)

for r in response:
    print(r.name)
    print(r.updated_by.id)


