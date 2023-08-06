# ConquestApiGeoPackageTableDescription

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column_infos** | [**list[ConquestApigpkgColumnInfo]**](ConquestApigpkgColumnInfo.md) |  | [optional] 
**contents** | [**ConquestApigpkgContents**](ConquestApigpkgContents.md) |  | [optional] 
**data_columns** | [**list[ConquestApigpkgDataColumns]**](ConquestApigpkgDataColumns.md) | DataColumns are what could be identified in a geo package for a table. | [optional] 
**geometry_column** | [**ConquestApigpkgGeometryColumns**](ConquestApigpkgGeometryColumns.md) | GeometryColumn is the geometry column that will be used. There can only be one of these per table. | [optional] 
**geometry_columns** | [**list[ConquestApigpkgGeometryColumns]**](ConquestApigpkgGeometryColumns.md) | GeometryColumns are what could be identified in a geo package for a table. There can only be one of these per table. | [optional] 
**key_column_option** | [**ConquestApiGeoPackageKeyColumnDescriptionOption**](ConquestApiGeoPackageKeyColumnDescriptionOption.md) |  | [optional] 
**object_id_column** | [**ConquestApigpkgColumnInfo**](ConquestApigpkgColumnInfo.md) | This is identified by either the KeyColumnOption otherwise a it will be inferred based on a naming convention for Conquest IDs like asset_id or by annotated columns in DataColumns | [optional] 
**object_type** | [**ConquestApiObjectType**](ConquestApiObjectType.md) | ObjectType that will be used to key data to the Conquest Object.  This is identified by either the KeyColumnOption otherwise a it will be inferred based on a naming convention for Conquest IDs like asset_id or by annotated columns in DataColumns | [optional] 
**srs_supported** | **bool** |  | [optional] 
**table_name** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


