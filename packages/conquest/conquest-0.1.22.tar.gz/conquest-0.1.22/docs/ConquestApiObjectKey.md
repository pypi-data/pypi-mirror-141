# ConquestApiObjectKey

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**int32_value** | **int** | Choose one of &#39;int32Value&#39;, &#39;stringValue&#39; and &#39;timestampValue&#39;.  Typically, an id is a unary key with the int type and only this needs to be provided. | [optional] 
**object_type** | [**ConquestApiObjectType**](ConquestApiObjectType.md) |  | [optional] 
**string_value** | **str** | Choose one of &#39;int32Value&#39;, &#39;stringValue&#39; and &#39;timestampValue&#39;.  Not every id can be an integer, in the odd case, a &#39;stringValue&#39; will be used instead.  A guid, string like a uri, or an encoded composite key, eg \&quot;(DefectID,InspectionID)\&quot; when the ObjectType is DefectHistory | [optional] 
**timestamp_value** | **datetime** | Choose one of &#39;int32Value&#39;, &#39;stringValue&#39; and &#39;timestampValue&#39;.  Timestamp as an id is typically used to reference a new object that does not yet have an id.  NOTE: Although &#39;oneof&#39; should mean JSON clients do not serialize this if it&#39;s not set.       Unfortunately, this is not always the case, so please make sure you JSON client       doesn&#39;t serialize this when not set. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


