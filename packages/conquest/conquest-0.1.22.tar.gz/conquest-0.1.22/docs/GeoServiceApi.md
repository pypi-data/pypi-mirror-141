# conquest.GeoServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**geo_service_add_geo_package**](GeoServiceApi.md#geo_service_add_geo_package) | **POST** /api/geo/add_geo_package | 


# **geo_service_add_geo_package**
> str geo_service_add_geo_package(file)



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
api_instance = conquest.GeoServiceApi(conquest.ApiClient(configuration))
file = '/path/to/file.txt' # file | A GeoPackage file (sqlite with the geopackage schema, .gpkg)

try:
    api_response = api_instance.geo_service_add_geo_package(file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GeoServiceApi->geo_service_add_geo_package: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **file**| A GeoPackage file (sqlite with the geopackage schema, .gpkg) | 

### Return type

**str**

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

