# conquest.AssetInspectionServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**asset_inspection_service_create_asset_inspection**](AssetInspectionServiceApi.md#asset_inspection_service_create_asset_inspection) | **POST** /api/asset_inspections/create_asset_inspection | 
[**asset_inspection_service_create_defect_for_asset_inspection**](AssetInspectionServiceApi.md#asset_inspection_service_create_defect_for_asset_inspection) | **POST** /api/asset_inspections/create_defect | 
[**asset_inspection_service_delete_asset_inspection**](AssetInspectionServiceApi.md#asset_inspection_service_delete_asset_inspection) | **POST** /api/asset_inspections/delete_asset_inspection | 
[**asset_inspection_service_get_asset_inspection**](AssetInspectionServiceApi.md#asset_inspection_service_get_asset_inspection) | **GET** /api/asset_inspections/{value} | 
[**asset_inspection_service_update_asset_inspection**](AssetInspectionServiceApi.md#asset_inspection_service_update_asset_inspection) | **POST** /api/asset_inspections/update_asset_inspection | 


# **asset_inspection_service_create_asset_inspection**
> int asset_inspection_service_create_asset_inspection(body)



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
api_instance = conquest.AssetInspectionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCreateAssetInspectionCommand() # ConquestApiCreateAssetInspectionCommand | 

try:
    api_response = api_instance.asset_inspection_service_create_asset_inspection(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetInspectionServiceApi->asset_inspection_service_create_asset_inspection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCreateAssetInspectionCommand**](ConquestApiCreateAssetInspectionCommand.md)|  | 

### Return type

**int**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_inspection_service_create_defect_for_asset_inspection**
> int asset_inspection_service_create_defect_for_asset_inspection(body)



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
api_instance = conquest.AssetInspectionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiCreateDefectForAssetInspectionCommand() # ConquestApiCreateDefectForAssetInspectionCommand | 

try:
    api_response = api_instance.asset_inspection_service_create_defect_for_asset_inspection(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetInspectionServiceApi->asset_inspection_service_create_defect_for_asset_inspection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiCreateDefectForAssetInspectionCommand**](ConquestApiCreateDefectForAssetInspectionCommand.md)|  | 

### Return type

**int**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_inspection_service_delete_asset_inspection**
> object asset_inspection_service_delete_asset_inspection(body)



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
api_instance = conquest.AssetInspectionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiDeleteAssetInspectionCommand() # ConquestApiDeleteAssetInspectionCommand | 

try:
    api_response = api_instance.asset_inspection_service_delete_asset_inspection(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetInspectionServiceApi->asset_inspection_service_delete_asset_inspection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiDeleteAssetInspectionCommand**](ConquestApiDeleteAssetInspectionCommand.md)|  | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_inspection_service_get_asset_inspection**
> ConquestApiAssetInspectionEntity asset_inspection_service_get_asset_inspection(value)



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
api_instance = conquest.AssetInspectionServiceApi(conquest.ApiClient(configuration))
value = 56 # int | The int32 value.

try:
    api_response = api_instance.asset_inspection_service_get_asset_inspection(value)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetInspectionServiceApi->asset_inspection_service_get_asset_inspection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **value** | **int**| The int32 value. | 

### Return type

[**ConquestApiAssetInspectionEntity**](ConquestApiAssetInspectionEntity.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **asset_inspection_service_update_asset_inspection**
> ConquestApiChangeSetResult asset_inspection_service_update_asset_inspection(body)



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
api_instance = conquest.AssetInspectionServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiAssetInspectionRecordChangeSet() # ConquestApiAssetInspectionRecordChangeSet | 

try:
    api_response = api_instance.asset_inspection_service_update_asset_inspection(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AssetInspectionServiceApi->asset_inspection_service_update_asset_inspection: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiAssetInspectionRecordChangeSet**](ConquestApiAssetInspectionRecordChangeSet.md)|  | 

### Return type

[**ConquestApiChangeSetResult**](ConquestApiChangeSetResult.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

