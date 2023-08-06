# conquest.RequestServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**request_service_create_request**](RequestServiceApi.md#request_service_create_request) | **POST** /api/requests/create_request | 
[**request_service_delete_request**](RequestServiceApi.md#request_service_delete_request) | **POST** /api/requests/delete_request | 
[**request_service_get_request**](RequestServiceApi.md#request_service_get_request) | **GET** /api/requests/{value} | 
[**request_service_update_request**](RequestServiceApi.md#request_service_update_request) | **POST** /api/requests/update_request | 


# **request_service_create_request**
> int request_service_create_request(body)



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
api_instance = conquest.RequestServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCreateRequestCommand() # ConquestApiCreateRequestCommand | 

try:
    api_response = api_instance.request_service_create_request(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RequestServiceApi->request_service_create_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCreateRequestCommand**](ConquestApiCreateRequestCommand.md)|  | 

### Return type

**int**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_service_delete_request**
> object request_service_delete_request(body)



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
api_instance = conquest.RequestServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiDeleteRequestCommand() # ConquestApiDeleteRequestCommand | 

try:
    api_response = api_instance.request_service_delete_request(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RequestServiceApi->request_service_delete_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiDeleteRequestCommand**](ConquestApiDeleteRequestCommand.md)|  | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_service_get_request**
> ConquestApiRequestEntity request_service_get_request(value)



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
api_instance = conquest.RequestServiceApi(conquest.ApiClient(configuration))
value = 56 # int | The int32 value.

try:
    api_response = api_instance.request_service_get_request(value)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RequestServiceApi->request_service_get_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **value** | **int**| The int32 value. | 

### Return type

[**ConquestApiRequestEntity**](ConquestApiRequestEntity.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_service_update_request**
> ConquestApiChangeSetResult request_service_update_request(body)



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
api_instance = conquest.RequestServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiRequestRecordChangeSet() # ConquestApiRequestRecordChangeSet | 

try:
    api_response = api_instance.request_service_update_request(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RequestServiceApi->request_service_update_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiRequestRecordChangeSet**](ConquestApiRequestRecordChangeSet.md)|  | 

### Return type

[**ConquestApiChangeSetResult**](ConquestApiChangeSetResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

