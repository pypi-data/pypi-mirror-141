# conquest.ActionServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**action_service_apply_standard_action**](ActionServiceApi.md#action_service_apply_standard_action) | **POST** /api/actions/apply_standard_action | 
[**action_service_complete_action**](ActionServiceApi.md#action_service_complete_action) | **POST** /api/actions/complete_action | 
[**action_service_create_succeeding_action**](ActionServiceApi.md#action_service_create_succeeding_action) | **POST** /api/actions/create_succeeding_action | 
[**action_service_delete_action**](ActionServiceApi.md#action_service_delete_action) | **POST** /api/actions/delete_action | 
[**action_service_get_action**](ActionServiceApi.md#action_service_get_action) | **GET** /api/actions/{value} | 
[**action_service_get_action_completion_details**](ActionServiceApi.md#action_service_get_action_completion_details) | **POST** /api/actions/completion_details | 
[**action_service_move_action**](ActionServiceApi.md#action_service_move_action) | **POST** /api/actions/move_action | 
[**action_service_reverse_action_completion**](ActionServiceApi.md#action_service_reverse_action_completion) | **POST** /api/actions/reverse_action_completion | 
[**action_service_update_action**](ActionServiceApi.md#action_service_update_action) | **POST** /api/actions/update_action | 


# **action_service_apply_standard_action**
> object action_service_apply_standard_action(body)



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
api_instance = conquest.ActionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiApplyStandardActionCommand() # ConquestApiApplyStandardActionCommand | 

try:
    api_response = api_instance.action_service_apply_standard_action(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActionServiceApi->action_service_apply_standard_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiApplyStandardActionCommand**](ConquestApiApplyStandardActionCommand.md)|  | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **action_service_complete_action**
> ConquestApiCompleteActionResult action_service_complete_action(body)



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
api_instance = conquest.ActionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCompleteActionCommand() # ConquestApiCompleteActionCommand | 

try:
    api_response = api_instance.action_service_complete_action(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActionServiceApi->action_service_complete_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCompleteActionCommand**](ConquestApiCompleteActionCommand.md)|  | 

### Return type

[**ConquestApiCompleteActionResult**](ConquestApiCompleteActionResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **action_service_create_succeeding_action**
> int action_service_create_succeeding_action(body)



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
api_instance = conquest.ActionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCreateSucceedingActionCommand() # ConquestApiCreateSucceedingActionCommand | 

try:
    api_response = api_instance.action_service_create_succeeding_action(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActionServiceApi->action_service_create_succeeding_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCreateSucceedingActionCommand**](ConquestApiCreateSucceedingActionCommand.md)|  | 

### Return type

**int**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **action_service_delete_action**
> object action_service_delete_action(body)



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
api_instance = conquest.ActionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiDeleteActionCommand() # ConquestApiDeleteActionCommand | 

try:
    api_response = api_instance.action_service_delete_action(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActionServiceApi->action_service_delete_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiDeleteActionCommand**](ConquestApiDeleteActionCommand.md)|  | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **action_service_get_action**
> ConquestApiActionEntity action_service_get_action(value)



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
api_instance = conquest.ActionServiceApi(conquest.ApiClient(configuration))
value = 56 # int | The int32 value.

try:
    api_response = api_instance.action_service_get_action(value)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActionServiceApi->action_service_get_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **value** | **int**| The int32 value. | 

### Return type

[**ConquestApiActionEntity**](ConquestApiActionEntity.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **action_service_get_action_completion_details**
> ConquestApiGetActionCompletionDetailsResponse action_service_get_action_completion_details(body)



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
api_instance = conquest.ActionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiGetActionCompletionDetailsRequest() # ConquestApiGetActionCompletionDetailsRequest | 

try:
    api_response = api_instance.action_service_get_action_completion_details(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActionServiceApi->action_service_get_action_completion_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiGetActionCompletionDetailsRequest**](ConquestApiGetActionCompletionDetailsRequest.md)|  | 

### Return type

[**ConquestApiGetActionCompletionDetailsResponse**](ConquestApiGetActionCompletionDetailsResponse.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **action_service_move_action**
> object action_service_move_action(body)



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
api_instance = conquest.ActionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiMoveActionCommand() # ConquestApiMoveActionCommand | 

try:
    api_response = api_instance.action_service_move_action(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActionServiceApi->action_service_move_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiMoveActionCommand**](ConquestApiMoveActionCommand.md)|  | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **action_service_reverse_action_completion**
> ConquestApiReverseActionCompletionResult action_service_reverse_action_completion(body)



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
api_instance = conquest.ActionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiReverseActionCompletionCommand() # ConquestApiReverseActionCompletionCommand | 

try:
    api_response = api_instance.action_service_reverse_action_completion(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActionServiceApi->action_service_reverse_action_completion: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiReverseActionCompletionCommand**](ConquestApiReverseActionCompletionCommand.md)|  | 

### Return type

[**ConquestApiReverseActionCompletionResult**](ConquestApiReverseActionCompletionResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **action_service_update_action**
> ConquestApiChangeSetResult action_service_update_action(body)



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
api_instance = conquest.ActionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiActionRecordChangeSet() # ConquestApiActionRecordChangeSet | 

try:
    api_response = api_instance.action_service_update_action(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActionServiceApi->action_service_update_action: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiActionRecordChangeSet**](ConquestApiActionRecordChangeSet.md)|  | 

### Return type

[**ConquestApiChangeSetResult**](ConquestApiChangeSetResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

