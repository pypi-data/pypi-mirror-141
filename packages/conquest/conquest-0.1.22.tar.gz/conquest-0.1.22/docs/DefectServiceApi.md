# conquest.DefectServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**defect_service_calculate_defect_response_date**](DefectServiceApi.md#defect_service_calculate_defect_response_date) | **POST** /api/defects/calculate_defect_response_date | 
[**defect_service_complete_defect**](DefectServiceApi.md#defect_service_complete_defect) | **POST** /api/defects/complete_defect | 
[**defect_service_create_action_for_defect**](DefectServiceApi.md#defect_service_create_action_for_defect) | **POST** /api/defects/create_action | 
[**defect_service_delete_defect**](DefectServiceApi.md#defect_service_delete_defect) | **POST** /api/defects/delete_defect | 
[**defect_service_get_defect**](DefectServiceApi.md#defect_service_get_defect) | **GET** /api/defects/{value} | 
[**defect_service_update_defect**](DefectServiceApi.md#defect_service_update_defect) | **POST** /api/defects/update_defect | 


# **defect_service_calculate_defect_response_date**
> ConquestApiCalculateDefectResponseDateResponse defect_service_calculate_defect_response_date(body)



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
api_instance = conquest.DefectServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCalculateDefectResponseDateRequest() # ConquestApiCalculateDefectResponseDateRequest | 

try:
    api_response = api_instance.defect_service_calculate_defect_response_date(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefectServiceApi->defect_service_calculate_defect_response_date: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCalculateDefectResponseDateRequest**](ConquestApiCalculateDefectResponseDateRequest.md)|  | 

### Return type

[**ConquestApiCalculateDefectResponseDateResponse**](ConquestApiCalculateDefectResponseDateResponse.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **defect_service_complete_defect**
> object defect_service_complete_defect(body)



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
api_instance = conquest.DefectServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCompleteDefectCommand() # ConquestApiCompleteDefectCommand | 

try:
    api_response = api_instance.defect_service_complete_defect(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefectServiceApi->defect_service_complete_defect: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCompleteDefectCommand**](ConquestApiCompleteDefectCommand.md)|  | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **defect_service_create_action_for_defect**
> int defect_service_create_action_for_defect(body)



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
api_instance = conquest.DefectServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCreateActionForDefectCommand() # ConquestApiCreateActionForDefectCommand | 

try:
    api_response = api_instance.defect_service_create_action_for_defect(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefectServiceApi->defect_service_create_action_for_defect: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCreateActionForDefectCommand**](ConquestApiCreateActionForDefectCommand.md)|  | 

### Return type

**int**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **defect_service_delete_defect**
> object defect_service_delete_defect(body)



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
api_instance = conquest.DefectServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiDeleteDefectCommand() # ConquestApiDeleteDefectCommand | 

try:
    api_response = api_instance.defect_service_delete_defect(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefectServiceApi->defect_service_delete_defect: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiDeleteDefectCommand**](ConquestApiDeleteDefectCommand.md)|  | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **defect_service_get_defect**
> ConquestApiDefectEntity defect_service_get_defect(value)



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
api_instance = conquest.DefectServiceApi(conquest.ApiClient(configuration))
value = 56 # int | The int32 value.

try:
    api_response = api_instance.defect_service_get_defect(value)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefectServiceApi->defect_service_get_defect: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **value** | **int**| The int32 value. | 

### Return type

[**ConquestApiDefectEntity**](ConquestApiDefectEntity.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **defect_service_update_defect**
> ConquestApiChangeSetResult defect_service_update_defect(body)



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
api_instance = conquest.DefectServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiDefectRecordChangeSet() # ConquestApiDefectRecordChangeSet | 

try:
    api_response = api_instance.defect_service_update_defect(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefectServiceApi->defect_service_update_defect: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiDefectRecordChangeSet**](ConquestApiDefectRecordChangeSet.md)|  | 

### Return type

[**ConquestApiChangeSetResult**](ConquestApiChangeSetResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

