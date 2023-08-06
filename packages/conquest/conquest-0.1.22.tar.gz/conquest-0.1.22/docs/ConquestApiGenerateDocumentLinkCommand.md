# ConquestApiGenerateDocumentLinkCommand

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document_id** | **int** |  | [optional] 
**object_key** | [**ConquestApiObjectKey**](ConquestApiObjectKey.md) |  | [optional] 
**x_thumbnail_parameter** | **str** | Currently the only supported value is \&quot;medium\&quot;  Regarding Blob Storage:      A thumbnail lives in a different container to the actual documents.      The thumbnail mount, that corresponds to another mount, has the suffix \&quot;.thumbnails\&quot;. For example: \&quot;mount&#x3D;{mount}.thumbnails\&quot;      The layout of a thumbnail container is the following          by_size/{size}/{blobName}      For example, for the given blob address (mount&#x3D;default):          blob://default/Assets/1/image.png      The address for a &#39;medium&#39; sized image will be:          blob://default.thumbnails/by_size/medium/Assets/1/image.png | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


