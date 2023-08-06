# conquest.ViewServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**view_service_find**](ViewServiceApi.md#view_service_find) | **POST** /api/find | Find will select all the provided FieldNames for a given Context
[**view_service_list_filters**](ViewServiceApi.md#view_service_list_filters) | **POST** /api/list_filters | 
[**view_service_list_hierarchy_nodes**](ViewServiceApi.md#view_service_list_hierarchy_nodes) | **POST** /api/list_hierarchy_nodes | ListHierarchyNodes returns the target HierarchyNode and a list of related HierarchyNodes as requested in the query


# **view_service_find**
> ConquestApiFindResult view_service_find(body)

Find will select all the provided FieldNames for a given Context

### Example
```python
from __future__ import print_function
import time
import conquest
from conquest.rest import ApiException
from pprint import pprint

# Configure API key authorization: Api Key from App
configuration = conquest.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = conquest.ViewServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiFindQuery() # ConquestApiFindQuery | 

try:
    # Find will select all the provided FieldNames for a given Context
    api_response = api_instance.view_service_find(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ViewServiceApi->view_service_find: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiFindQuery**](ConquestApiFindQuery.md)|  | 

### Return type

[**ConquestApiFindResult**](ConquestApiFindResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **view_service_list_filters**
> ConquestApiListFiltersResult view_service_list_filters(body)



### Example
```python
from __future__ import print_function
import time
import conquest
from conquest.rest import ApiException
from pprint import pprint

# Configure API key authorization: Api Key from App
configuration = conquest.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = conquest.ViewServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiListFiltersQuery() # ConquestApiListFiltersQuery | 

try:
    api_response = api_instance.view_service_list_filters(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ViewServiceApi->view_service_list_filters: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiListFiltersQuery**](ConquestApiListFiltersQuery.md)|  | 

### Return type

[**ConquestApiListFiltersResult**](ConquestApiListFiltersResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **view_service_list_hierarchy_nodes**
> ConquestApiObjectHeadersResult view_service_list_hierarchy_nodes(body)

ListHierarchyNodes returns the target HierarchyNode and a list of related HierarchyNodes as requested in the query

A hierarchy object is an object whose ObjectType and parents ObjectType are the same.

### Example
```python
from __future__ import print_function
import time
import conquest
from conquest.rest import ApiException
from pprint import pprint

# Configure API key authorization: Api Key from App
configuration = conquest.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = conquest.ViewServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiListHierarchyNodesQuery() # ConquestApiListHierarchyNodesQuery | 

try:
    # ListHierarchyNodes returns the target HierarchyNode and a list of related HierarchyNodes as requested in the query
    api_response = api_instance.view_service_list_hierarchy_nodes(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ViewServiceApi->view_service_list_hierarchy_nodes: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiListHierarchyNodesQuery**](ConquestApiListHierarchyNodesQuery.md)|  | 

### Return type

[**ConquestApiObjectHeadersResult**](ConquestApiObjectHeadersResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

