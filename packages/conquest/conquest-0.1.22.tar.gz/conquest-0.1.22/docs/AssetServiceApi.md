# conquest.AssetServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**asset_service_change_asset_type**](AssetServiceApi.md#asset_service_change_asset_type) | **POST** /api/assets/change_asset_type | 
[**asset_service_copy_asset**](AssetServiceApi.md#asset_service_copy_asset) | **POST** /api/assets/copy_asset | 
[**asset_service_create_action_for_asset**](AssetServiceApi.md#asset_service_create_action_for_asset) | **POST** /api/assets/create_action | 
[**asset_service_create_asset**](AssetServiceApi.md#asset_service_create_asset) | **POST** /api/assets/create_asset | 
[**asset_service_create_defect_for_asset**](AssetServiceApi.md#asset_service_create_defect_for_asset) | **POST** /api/assets/create_defect | 
[**asset_service_delete_asset**](AssetServiceApi.md#asset_service_delete_asset) | **POST** /api/assets/delete_asset | 
[**asset_service_get_asset**](AssetServiceApi.md#asset_service_get_asset) | **GET** /api/assets/{value} | 
[**asset_service_list_inspections_for_asset**](AssetServiceApi.md#asset_service_list_inspections_for_asset) | **POST** /api/assets/list_inspections | 
[**asset_service_move_asset**](AssetServiceApi.md#asset_service_move_asset) | **POST** /api/assets/move_asset | 
[**asset_service_new_condition_inspection**](AssetServiceApi.md#asset_service_new_condition_inspection) | **POST** /api/assets/new_condition_inspection | 
[**asset_service_tag_as_inspected**](AssetServiceApi.md#asset_service_tag_as_inspected) | **POST** /api/assets/tag_as_inspected | 
[**asset_service_update_asset**](AssetServiceApi.md#asset_service_update_asset) | **POST** /api/assets/update_asset | 


# **asset_service_change_asset_type**
> object asset_service_change_asset_type(body)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiChangeAssetTypeCommand() # ConquestApiChangeAssetTypeCommand | 

try:
    api_response = api_instance.asset_service_change_asset_type(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_change_asset_type: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiChangeAssetTypeCommand**](ConquestApiChangeAssetTypeCommand.md)|  | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_service_copy_asset**
> ConquestApiCopyAssetResult asset_service_copy_asset(body)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCopyAssetCommand() # ConquestApiCopyAssetCommand | 

try:
    api_response = api_instance.asset_service_copy_asset(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_copy_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCopyAssetCommand**](ConquestApiCopyAssetCommand.md)|  | 

### Return type

[**ConquestApiCopyAssetResult**](ConquestApiCopyAssetResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_service_create_action_for_asset**
> int asset_service_create_action_for_asset(body)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCreateActionForAssetCommand() # ConquestApiCreateActionForAssetCommand | 

try:
    api_response = api_instance.asset_service_create_action_for_asset(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_create_action_for_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCreateActionForAssetCommand**](ConquestApiCreateActionForAssetCommand.md)|  | 

### Return type

**int**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_service_create_asset**
> int asset_service_create_asset(body)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCreateAssetCommand() # ConquestApiCreateAssetCommand | 

try:
    api_response = api_instance.asset_service_create_asset(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_create_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCreateAssetCommand**](ConquestApiCreateAssetCommand.md)|  | 

### Return type

**int**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_service_create_defect_for_asset**
> int asset_service_create_defect_for_asset(body)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCreateDefectForAssetCommand() # ConquestApiCreateDefectForAssetCommand | 

try:
    api_response = api_instance.asset_service_create_defect_for_asset(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_create_defect_for_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCreateDefectForAssetCommand**](ConquestApiCreateDefectForAssetCommand.md)|  | 

### Return type

**int**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_service_delete_asset**
> object asset_service_delete_asset(body)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiDeleteAssetCommand() # ConquestApiDeleteAssetCommand | 

try:
    api_response = api_instance.asset_service_delete_asset(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_delete_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiDeleteAssetCommand**](ConquestApiDeleteAssetCommand.md)|  | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_service_get_asset**
> ConquestApiAssetEntity asset_service_get_asset(value)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
value = 56 # int | The int32 value.

try:
    api_response = api_instance.asset_service_get_asset(value)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_get_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **value** | **int**| The int32 value. | 

### Return type

[**ConquestApiAssetEntity**](ConquestApiAssetEntity.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_service_list_inspections_for_asset**
> ConquestApiInspectionsForAssetResponse asset_service_list_inspections_for_asset(body)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiInspectionsForAssetQuery() # ConquestApiInspectionsForAssetQuery | 

try:
    api_response = api_instance.asset_service_list_inspections_for_asset(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_list_inspections_for_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiInspectionsForAssetQuery**](ConquestApiInspectionsForAssetQuery.md)|  | 

### Return type

[**ConquestApiInspectionsForAssetResponse**](ConquestApiInspectionsForAssetResponse.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_service_move_asset**
> object asset_service_move_asset(body)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiMoveAssetCommand() # ConquestApiMoveAssetCommand | 

try:
    api_response = api_instance.asset_service_move_asset(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_move_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiMoveAssetCommand**](ConquestApiMoveAssetCommand.md)|  | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_service_new_condition_inspection**
> ConquestApiObjectKey asset_service_new_condition_inspection(body)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiNewConditionInspectionCommand() # ConquestApiNewConditionInspectionCommand | 

try:
    api_response = api_instance.asset_service_new_condition_inspection(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_new_condition_inspection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiNewConditionInspectionCommand**](ConquestApiNewConditionInspectionCommand.md)|  | 

### Return type

[**ConquestApiObjectKey**](ConquestApiObjectKey.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_service_tag_as_inspected**
> int asset_service_tag_as_inspected(body)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiTagAsInspectedCommand() # ConquestApiTagAsInspectedCommand | 

try:
    api_response = api_instance.asset_service_tag_as_inspected(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_tag_as_inspected: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiTagAsInspectedCommand**](ConquestApiTagAsInspectedCommand.md)|  | 

### Return type

**int**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_service_update_asset**
> ConquestApiChangeSetResult asset_service_update_asset(body)



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
api_instance = conquest.AssetServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiAssetRecordChangeSet() # ConquestApiAssetRecordChangeSet | 

try:
    api_response = api_instance.asset_service_update_asset(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetServiceApi->asset_service_update_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiAssetRecordChangeSet**](ConquestApiAssetRecordChangeSet.md)|  | 

### Return type

[**ConquestApiChangeSetResult**](ConquestApiChangeSetResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

