from elasticsearch_dsl import FacetedSearch, TermsFacet, DateHistogramFacet
from blog import Article

class BlogSearch(FacetedSearch):
    doc_types = [Article, ]
    # fields that should be searched
    fields = ['tags', 'title', 'body']

    facets = {
        # use bucket aggregations to define facets
        'tags': TermsFacet(field='tags'),
        'publishing_frequency': DateHistogramFacet(field='published_from', interval='month')
    }


# empty search
bs = BlogSearch()
response = bs.execute()

for hit in response:
    print(hit, hit.meta.score)
    # print(hit.meta.score, hit.title)

# for (tag, count, selected) in response.facets.tags:
#     print(tag, ' (SELECTED):' if selected else ':', count)

# for (month, count, selected) in response.facets.publishing_frequency:
#     print(month.strftime('%B %Y'), ' (SELECTED):' if selected else ':', count)
