# conquest.DocumentServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**document_service_add_document**](DocumentServiceApi.md#document_service_add_document) | **POST** /api/documents/add_document | 
[**document_service_change_document_content**](DocumentServiceApi.md#document_service_change_document_content) | **POST** /api/documents/change_document_content | 
[**document_service_generate_document_link**](DocumentServiceApi.md#document_service_generate_document_link) | **POST** /api/documents/generate_document_link | 
[**document_service_get_documents**](DocumentServiceApi.md#document_service_get_documents) | **POST** /api/documents/list | 
[**document_service_list_document_locations**](DocumentServiceApi.md#document_service_list_document_locations) | **POST** /api/documents/list_locations | 
[**document_service_remove_document**](DocumentServiceApi.md#document_service_remove_document) | **POST** /api/documents/remove_document | 


# **document_service_add_document**
> ConquestApiAddDocumentResult document_service_add_document(body)



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
api_instance = conquest.DocumentServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiAddDocumentCommand() # ConquestApiAddDocumentCommand | 

try:
    api_response = api_instance.document_service_add_document(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DocumentServiceApi->document_service_add_document: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiAddDocumentCommand**](ConquestApiAddDocumentCommand.md)|  | 

### Return type

[**ConquestApiAddDocumentResult**](ConquestApiAddDocumentResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **document_service_change_document_content**
> ConquestApiAddDocumentResult document_service_change_document_content(body)



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
api_instance = conquest.DocumentServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiChangeDocumentContentCommand() # ConquestApiChangeDocumentContentCommand | 

try:
    api_response = api_instance.document_service_change_document_content(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DocumentServiceApi->document_service_change_document_content: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiChangeDocumentContentCommand**](ConquestApiChangeDocumentContentCommand.md)|  | 

### Return type

[**ConquestApiAddDocumentResult**](ConquestApiAddDocumentResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **document_service_generate_document_link**
> ConquestApiGenerateDocumentLinkResult document_service_generate_document_link(body)



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
api_instance = conquest.DocumentServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiGenerateDocumentLinkCommand() # ConquestApiGenerateDocumentLinkCommand | 

try:
    api_response = api_instance.document_service_generate_document_link(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DocumentServiceApi->document_service_generate_document_link: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiGenerateDocumentLinkCommand**](ConquestApiGenerateDocumentLinkCommand.md)|  | 

### Return type

[**ConquestApiGenerateDocumentLinkResult**](ConquestApiGenerateDocumentLinkResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **document_service_get_documents**
> ConquestApiGetDocumentsResult document_service_get_documents(body)



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
api_instance = conquest.DocumentServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiGetDocumentsQuery() # ConquestApiGetDocumentsQuery | 

try:
    api_response = api_instance.document_service_get_documents(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DocumentServiceApi->document_service_get_documents: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiGetDocumentsQuery**](ConquestApiGetDocumentsQuery.md)|  | 

### Return type

[**ConquestApiGetDocumentsResult**](ConquestApiGetDocumentsResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **document_service_list_document_locations**
> ConquestApiListDocumentLocationsResponse document_service_list_document_locations(body)



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
api_instance = conquest.DocumentServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiListDocumentLocationsQuery() # ConquestApiListDocumentLocationsQuery | 

try:
    api_response = api_instance.document_service_list_document_locations(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DocumentServiceApi->document_service_list_document_locations: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiListDocumentLocationsQuery**](ConquestApiListDocumentLocationsQuery.md)|  | 

### Return type

[**ConquestApiListDocumentLocationsResponse**](ConquestApiListDocumentLocationsResponse.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **document_service_remove_document**
> object document_service_remove_document(body)



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
api_instance = conquest.DocumentServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiRemoveDocumentCommand() # ConquestApiRemoveDocumentCommand | 

try:
    api_response = api_instance.document_service_remove_document(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DocumentServiceApi->document_service_remove_document: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiRemoveDocumentCommand**](ConquestApiRemoveDocumentCommand.md)|  | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

