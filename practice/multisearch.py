# ms = MultiSearch(index="blogs")

# ms = ms.add(Search().filter("term", tags="python"))
# ms = ms.add(Search().filter("term", tags="elasticsearch"))

q2 = Q(
    "bool",
    should=[
        Q("match", references__object__id=parent_id)
        for parent_id in collection_search_criteria.parent_ids
    ],
)
q1 = Q("nested", path="references.object", query=q2)

df = pd.DataFrame()
df.query = {}

ms = self._elasticsearch_client.get_multi_search_dsl()

# ms = ms.add(Search(doc_type=Collection).filter(q1))
ms = ms.add(Search(doc_type=Collection).filter(q1))
ms = ms.add(Search(doc_type=Media).filter(q1))
print(ms.to_dict())
responses = ms.execute()
# return responses
# print(responses)

response = [response.to_dict() for response in responses]
print(response)
return response

ms = ms.add(
    Search()
    .extra(size=10000)
    .query("match_phrase", statuses=status)
    .query("match", path=location)
    .filter(
        "range",
        **{
            "@timestamp": {
                "gte": start_time.isoformat(),
                "lt": end_time.isoformat(),
            }
        },
    )
    .sort("@timestamp")
)