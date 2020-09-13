from elasticsearch_dsl import search

from workspace.dsl_search import ActivitySearch


search = ActivitySearch()
search.match_by_name(
    name="Crecentral General Workspace",
)
