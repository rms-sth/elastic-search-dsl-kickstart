from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


class ActivitySearch:
    def __init__(self) -> None:
        self.client = Elasticsearch()
        # s = Search(using=client

    def match_by_name(self, name):
        s = Search(index='test.workspacevault.activities').using(self.client)
        # s = s.query("match", name="Crecentral General Workspace")
        s = s.query('match', name=name)

        response = s.execute()

        # print(response)
        for r in response:
            print(f'{r.name} | {r.updated_by.id}')
