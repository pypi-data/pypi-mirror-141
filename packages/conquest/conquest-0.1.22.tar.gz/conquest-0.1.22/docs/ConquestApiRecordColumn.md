# ConquestApiRecordColumn

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alias** | **str** | alias is the column name or SQL alias in a query or user view.  - An alias with a prefix of 2 underscores &#39;__&#39; are reserved for Conquest. These fields are subject to change, they&#39;re a temporary solution   For example, __Title, __Subtitle  WARNING alias is not finalized, don&#39;t write code that depends on it.  view.column for non-calculated values defined in a Context (a selection of fields in the Field Dictionary) | [optional] 
**caption** | **str** |  | [optional] 
**group** | **int** |  | [optional] 
**identity** | **bool** |  | [optional] 
**index** | **int** |  | [optional] 
**relation** | [**ConquestApiRelation**](ConquestApiRelation.md) |  | [optional] 
**value_type** | [**ConquestApiValueType**](ConquestApiValueType.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


