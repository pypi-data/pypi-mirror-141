# ConquestApiAddDocumentResult

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document** | [**ConquestApiDocument**](ConquestApiDocument.md) |  | [optional] 
**upload_expire_time** | **datetime** |  | [optional] 
**upload_headers** | **dict(str, str)** |  | [optional] 
**upload_method** | **str** |  | [optional] 
**upload_uri** | **str** | UploadUri is where you must post the UploadData. It is a multipart HTTP upload with the field \&quot;document\&quot; for which the document is uploaded to.  For example, you can upload &#39;inspection-photo.png&#39; like this for a standard web form &#x60;&#x60;&#x60;   curl -i -X POST -H \&quot;Content-Type: multipart/form-data\&quot; -F \&quot;document&#x3D;@inspection-photo.png\&quot; \&quot;${ApiHost}${UploadUri}\&quot; &#x60;&#x60;&#x60;  Alternatively, use if no metadata needs to be submitted. &#x60;&#x60;&#x60;   curl --upload-file \&quot;${ApiHost}${UploadUri}\&quot; &#x60;&#x60;&#x60;  If the Uri is relative, prefix it with the api origin.  UploadUri will be empty if: - The Added Document was a link to an existing document (LinkExistingDocument&#x3D;true) - The Document Link is not relative to one of the Document Locations (see GetHierarchyNodesQuery{ObjectType&#x3D;DocumentContainer}) | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


