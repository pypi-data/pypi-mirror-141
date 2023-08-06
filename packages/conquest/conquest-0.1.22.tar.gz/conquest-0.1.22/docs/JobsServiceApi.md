# conquest.JobsServiceApi

All URIs are relative to *https://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**jobs_service_get_job_state**](JobsServiceApi.md#jobs_service_get_job_state) | **POST** /api/jobs/current_state | 


# **jobs_service_get_job_state**
> ConquestApiGetJobStateResponse jobs_service_get_job_state(body)



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
api_instance = conquest.JobsServiceApi(conquest.ApiClient(configuration))
body = conquest.ConquestApiGetJobStateQuery() # ConquestApiGetJobStateQuery | 

try:
    api_response = api_instance.jobs_service_get_job_state(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobsServiceApi->jobs_service_get_job_state: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ConquestApiGetJobStateQuery**](ConquestApiGetJobStateQuery.md)|  | 

### Return type

[**ConquestApiGetJobStateResponse**](ConquestApiGetJobStateResponse.md)

### Authorization

[Api Key from App](../README.md#Api Key from App)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

