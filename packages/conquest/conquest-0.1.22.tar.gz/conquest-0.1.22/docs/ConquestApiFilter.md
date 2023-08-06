# ConquestApiFilter

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**context** | **str** | Context is a selection of fields with a predefined Criteria. It is like the &#39;from&#39; clause if a SQL query, a set of \&quot;joined tables\&quot;.  Contexts are defined in the Field Dictionary  This Context is parameterised with the ObjectID for it&#39;s respective ObjectType | [optional] 
**description** | **str** |  | [optional] 
**filter_id** | **int** | The ID for a UserView. A UserView is constructed using the filter builder. | [optional] 
**filter_name** | **str** |  | [optional] 
**map_view_id** | **int** | The ID for a MapView. A MapView is a collection of UserViews. The ResultSet will have many groups. | [optional] 
**system** | **bool** |  | [optional] 
**user_views** | [**list[ConquestApiUserViewFilter]**](ConquestApiUserViewFilter.md) |  | [optional] 
**usr** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


