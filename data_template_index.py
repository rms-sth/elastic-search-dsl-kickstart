# python3 -m activities_index

# from workspace.dsl_index import ActivityIndex

# activity = ActivityIndex()

# activity.create_new_mapping()
# # activity.create_mapping()
# # activity.delete_mapping()
# activity.create_index()


from workspace.dsl_index import DataTemplateIndex

# media = MediaIndex()
# media.create_new_mapping()


data = DataTemplateIndex()
data.create_new_mapping()