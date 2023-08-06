# conquest.CsvImportServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**csv_import_service_add_csv_import**](CsvImportServiceApi.md#csv_import_service_add_csv_import) | **POST** /api/import/add/{ImportType} | 
[**csv_import_service_delete_csv_import**](CsvImportServiceApi.md#csv_import_service_delete_csv_import) | **DELETE** /api/import/delete/{JobID} | Remove import
[**csv_import_service_get_csv_import_state**](CsvImportServiceApi.md#csv_import_service_get_csv_import_state) | **GET** /api/import/state/{JobID} | Get status for import
[**csv_import_service_start_csv_import**](CsvImportServiceApi.md#csv_import_service_start_csv_import) | **POST** /api/import/start | 


# **csv_import_service_add_csv_import**
> str csv_import_service_add_csv_import(import_type, file)



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
api_instance = conquest.CsvImportServiceApi(conquest.ApiClient(configuration))
import_type = 'import_type_example' # str | Action, Asset, Defect, Request, AssetInspection, RiskEvent, LogBook
file = '/path/to/file.txt' # file | CSV file data

try:
    api_response = api_instance.csv_import_service_add_csv_import(import_type, file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CsvImportServiceApi->csv_import_service_add_csv_import: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **import_type** | **str**| Action, Asset, Defect, Request, AssetInspection, RiskEvent, LogBook | 
 **file** | **file**| CSV file data | 

### Return type

**str**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **csv_import_service_delete_csv_import**
> object csv_import_service_delete_csv_import(job_id)

Remove import

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
api_instance = conquest.CsvImportServiceApi(conquest.ApiClient(configuration))
job_id = 'job_id_example' # str | aka. ProcessID/BatchID

try:
    # Remove import
    api_response = api_instance.csv_import_service_delete_csv_import(job_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CsvImportServiceApi->csv_import_service_delete_csv_import: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| aka. ProcessID/BatchID | 

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **csv_import_service_get_csv_import_state**
> ConquestApiCsvImportStateResponse csv_import_service_get_csv_import_state(job_id)

Get status for import

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
api_instance = conquest.CsvImportServiceApi(conquest.ApiClient(configuration))
job_id = 'job_id_example' # str | aka. ProcessID/BatchID

try:
    # Get status for import
    api_response = api_instance.csv_import_service_get_csv_import_state(job_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CsvImportServiceApi->csv_import_service_get_csv_import_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| aka. ProcessID/BatchID | 

### Return type

[**ConquestApiCsvImportStateResponse**](ConquestApiCsvImportStateResponse.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **csv_import_service_start_csv_import**
> object csv_import_service_start_csv_import()



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
api_instance = conquest.CsvImportServiceApi(conquest.ApiClient(configuration))

try:
    api_response = api_instance.csv_import_service_start_csv_import()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CsvImportServiceApi->csv_import_service_start_csv_import: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

