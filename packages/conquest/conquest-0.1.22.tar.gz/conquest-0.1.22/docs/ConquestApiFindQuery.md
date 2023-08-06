# ConquestApiFindQuery

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**context** | **str** | Context is a selection of fields with a predefined Criteria. It is like the &#39;from&#39; clause if a SQL query, a set of \&quot;joined tables\&quot;.  Contexts are defined in the Field Dictionary  This Context is parameterised with the ObjectID for it&#39;s respective ObjectType | [optional] 
**criteria** | [**ConquestApiCriteria**](ConquestApiCriteria.md) |  | [optional] 
**field_names** | **list[str]** | FieldNames is the list of fields that will be returned in the RecordSet.  If empty, the default selection of fields will be provided. Otherwise the selected field names, if defined by the Context, will be returned | [optional] 
**filter_id** | **int** | The ID for a UserView. A UserView is constructed using the filter builder. | [optional] 
**limit** | **int** |  | [optional] 
**map_view_id** | **int** | The ID for a MapView. A MapView is a collection of UserViews.  The ResultSet will have many groups. | [optional] 
**parameter_object_key** | [**ConquestApiObjectKey**](ConquestApiObjectKey.md) |  | [optional] 
**parameter_object_key2** | [**ConquestApiObjectKey**](ConquestApiObjectKey.md) |  | [optional] 
**without_default_criteria** | **bool** | If true, the PredefinedContextCriteria, enabled by default are not applied. | [optional] 
**x_include_coordinates** | **bool** |  | [optional] 
**x_include_related_contexts** | **bool** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


