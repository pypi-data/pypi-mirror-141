# conquest.KnowledgeBaseServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**knowledge_base_service_describe_enumeration**](KnowledgeBaseServiceApi.md#knowledge_base_service_describe_enumeration) | **POST** /api/knowledge_base/describe_enumeration | 
[**knowledge_base_service_get_attribute_set_field_names**](KnowledgeBaseServiceApi.md#knowledge_base_service_get_attribute_set_field_names) | **POST** /api/knowledge_base/list_field_names_for_attribute_set | 
[**knowledge_base_service_get_code_lists**](KnowledgeBaseServiceApi.md#knowledge_base_service_get_code_lists) | **POST** /api/knowledge_base/list_code_lists | 
[**knowledge_base_service_list_attribute_sets**](KnowledgeBaseServiceApi.md#knowledge_base_service_list_attribute_sets) | **POST** /api/knowledge_base/list_attribute_sets | 
[**knowledge_base_service_list_standard_defect_responses**](KnowledgeBaseServiceApi.md#knowledge_base_service_list_standard_defect_responses) | **POST** /api/knowledge_base/list_standard_defect_responses | 
[**knowledge_base_service_list_view_fields**](KnowledgeBaseServiceApi.md#knowledge_base_service_list_view_fields) | **POST** /api/knowledge_base/list_view_fields_for_context | 


# **knowledge_base_service_describe_enumeration**
> ConquestApiDescribeEnumerationResult knowledge_base_service_describe_enumeration(body)



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
api_instance = conquest.KnowledgeBaseServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiDescribeEnumerationRequest() # ConquestApiDescribeEnumerationRequest | 

try:
    api_response = api_instance.knowledge_base_service_describe_enumeration(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling KnowledgeBaseServiceApi->knowledge_base_service_describe_enumeration: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiDescribeEnumerationRequest**](ConquestApiDescribeEnumerationRequest.md)|  | 

### Return type

[**ConquestApiDescribeEnumerationResult**](ConquestApiDescribeEnumerationResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **knowledge_base_service_get_attribute_set_field_names**
> ConquestApiGetAttributeSetFieldNamesResponse knowledge_base_service_get_attribute_set_field_names(body)



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
api_instance = conquest.KnowledgeBaseServiceApi(conquest.ApiClient(configuration))
body = NULL # object | 

try:
    api_response = api_instance.knowledge_base_service_get_attribute_set_field_names(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling KnowledgeBaseServiceApi->knowledge_base_service_get_attribute_set_field_names: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **object**|  | 

### Return type

[**ConquestApiGetAttributeSetFieldNamesResponse**](ConquestApiGetAttributeSetFieldNamesResponse.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **knowledge_base_service_get_code_lists**
> ConquestApiGetCodeListsResult knowledge_base_service_get_code_lists(body)



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
api_instance = conquest.KnowledgeBaseServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiGetCodeListsQuery() # ConquestApiGetCodeListsQuery | 

try:
    api_response = api_instance.knowledge_base_service_get_code_lists(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling KnowledgeBaseServiceApi->knowledge_base_service_get_code_lists: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiGetCodeListsQuery**](ConquestApiGetCodeListsQuery.md)|  | 

### Return type

[**ConquestApiGetCodeListsResult**](ConquestApiGetCodeListsResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **knowledge_base_service_list_attribute_sets**
> ConquestApiAttributeSetsResult knowledge_base_service_list_attribute_sets(body)



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
api_instance = conquest.KnowledgeBaseServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiListAttributeSetsQuery() # ConquestApiListAttributeSetsQuery | 

try:
    api_response = api_instance.knowledge_base_service_list_attribute_sets(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling KnowledgeBaseServiceApi->knowledge_base_service_list_attribute_sets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiListAttributeSetsQuery**](ConquestApiListAttributeSetsQuery.md)|  | 

### Return type

[**ConquestApiAttributeSetsResult**](ConquestApiAttributeSetsResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **knowledge_base_service_list_standard_defect_responses**
> ConquestApiListStandardDefectResponsesResult knowledge_base_service_list_standard_defect_responses(body)



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
api_instance = conquest.KnowledgeBaseServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiListStandardDefectResponsesQuery() # ConquestApiListStandardDefectResponsesQuery | 

try:
    api_response = api_instance.knowledge_base_service_list_standard_defect_responses(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling KnowledgeBaseServiceApi->knowledge_base_service_list_standard_defect_responses: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiListStandardDefectResponsesQuery**](ConquestApiListStandardDefectResponsesQuery.md)|  | 

### Return type

[**ConquestApiListStandardDefectResponsesResult**](ConquestApiListStandardDefectResponsesResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **knowledge_base_service_list_view_fields**
> ConquestApiViewContext knowledge_base_service_list_view_fields(body)



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
api_instance = conquest.KnowledgeBaseServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiListViewFieldsQuery() # ConquestApiListViewFieldsQuery | 

try:
    api_response = api_instance.knowledge_base_service_list_view_fields(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling KnowledgeBaseServiceApi->knowledge_base_service_list_view_fields: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiListViewFieldsQuery**](ConquestApiListViewFieldsQuery.md)|  | 

### Return type

[**ConquestApiViewContext**](ConquestApiViewContext.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

