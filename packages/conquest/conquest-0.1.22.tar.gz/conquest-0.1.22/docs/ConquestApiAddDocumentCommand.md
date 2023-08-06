# ConquestApiAddDocumentCommand

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address** | **str** | Address is a URI with a supported scheme (blob://, file://, https://, conquest://, trim://).  Addresses tell the server in what location a document should be put. Use ListDocumentLocationsQuery to list available locations.  Locations are pre-defined and are identified by a prefix like \&quot;{scheme}://{location-name}\&quot;.  The default location, known as the \&quot;System Document Directory\&quot; is  - \&quot;file://conquest_documents/\&quot; for site installations  - \&quot;blob://default/\&quot; for cloud installations (the location name may differ).  When choosing an address, prefix it with a known location, followed by a relative path. For example:       \&quot;blob://default/Assets/1/receipt.txt\&quot;  After a successful upload, reference this document using both the ObjectKey and the returned Document.DocumentID when using the download endpoint. For example:       \&quot;/download/document?object_type&#x3D;...&amp;object_id&#x3D;...&amp;document_id&#x3D;...\&quot;  This endpoint may redirect (provide an address in the Location header) you to a download. | [optional] 
**content_length** | **str** |  | [optional] 
**content_type** | **str** |  | [optional] 
**create_time** | **datetime** | CreateTime is unique. When adding a document, there is no DocumentID yet, the CreateTime should be used as a key until the DocumentID is retrieved. | [optional] 
**document_description** | **str** |  | [optional] 
**hashes** | **list[str]** | A list of calculated hashes / checksum of the file to be uploaded. | [optional] 
**link_existing_document** | **bool** |  | [optional] 
**object_key** | [**ConquestApiObjectKey**](ConquestApiObjectKey.md) | ObjectKey (please reference the ObjectKey documentation). | [optional] 
**prefix** | **str** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


