from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Match
from elasticsearch_dsl import Q


class DealSearch:
    def __init__(self) -> None:
        self.client = Elasticsearch(
            'https://chukhiros:chukh1r05@staging.elasticsearch.crecentric.app/')
        # s = Search(using=client

    def match_by_name(self, name: list):
        s = Search(index='dev.niroj.dealvault.deals').using(self.client)
        # s = s.query("match", name="Crecentral General Workspace")
        # s = s.query('match', name=name)

        # s = s.query("match", name='project')

        # s.query = Q(
        #     'bool', must=[Q('match', name='project') & Q('match', name='blue')]
        # )

        print(name, type(name))


        print([(Q('match', name=n)) for n in name])

        queries = [(Q('match', name=n)) for n in name]
        
        s.query = Q(
            'bool', must=[q for q in queries]
        )

        # s.query = Q(
        #     'bool', must=['&'.join(Q('match', name=n)) for n in name]
        # )

        q = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "name": "project"
                            }
                        },
                        {
                            "match": {
                                "name": "blue"
                            }
                        }
                    ]
                }
            }
        }
        s = s.update_from_dict(q)
        print(s.to_dict())

        response = s.execute()

        print(response)
        for r in response:
            print(f'{r.name}')


d = DealSearch()
d.match_by_name(["project", "blue"])
