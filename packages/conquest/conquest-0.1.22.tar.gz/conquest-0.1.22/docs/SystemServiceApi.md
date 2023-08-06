# conquest.SystemServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**system_service_application_version**](SystemServiceApi.md#system_service_application_version) | **GET** /api/system/version | 


# **system_service_application_version**
> ConquestApiSystemVersionResponse system_service_application_version()



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
api_instance = conquest.SystemServiceApi(conquest.ApiClient(configuration))

try:
    api_response = api_instance.system_service_application_version()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemServiceApi->system_service_application_version: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ConquestApiSystemVersionResponse**](ConquestApiSystemVersionResponse.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

