#%%
import os
import dotenv
import logging
logging.getLogger()
logging.basicConfig(filename='./test.log', level=logging.WARNING)
dotenv.load_dotenv()
API_HOST=os.environ['API_HOST']
PREFIX = 'Bearer'
API_TOKEN='{} {}'.format(PREFIX, os.environ['API_TOKEN'])
print('Using host {}'.format(API_HOST))

#%%
import conquest as c
config = c.Configuration()
config.host = API_HOST
config.api_key['Authorization'] = API_TOKEN
config.api_key_prefix['Authorizations'] = PREFIX
api_instance = c.ApiClient(configuration=config)

# %%
# The examples below show the API usage with increasing complexity

# %%
# Get the system version
# This is a simple request, it can be done without an access token
system = c.SystemServiceApi(api_instance).system_service_application_version()
print(system)
# %%
# Get an asset by ID
# With this request, an access token is required, but no body is needed
asset = c.AssetServiceApi(api_instance).asset_service_get_asset(2636)
print(asset.to_dict())
# %%
# Get a list of children
# This request requires a body, but it does not update the data, it is only reading
body = c.ConquestApiListHierarchyNodesQuery(
    include_ancestors=False, 
    include_children=True, 
    include_descendents=0, 
    include_siblings=False, 
    include_sub_items=False,
    object_key=c.ConquestApiObjectKey(
        int32_value=0, 
        object_type=c.ConquestApiObjectType.ASSET))
# At this point the body is built, but has extra fields that need to be removed
# See conquest_apiObjectKey at https://api-conquestdemo.conquest.live/swagger/#model-conquest_apiObjectKey
# del(body._object_key.string_value)
# del(body._object_key.timestamp_value)

print(body)
print(body.to_dict())
view = c.ViewServiceApi(api_instance).view_service_list_hierarchy_nodes(body)
print(view.to_dict())
# %%
