import os
import json
import time
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, Response
from common.s3 import S3Utils

logger = Logger(service="file-upload-service")
tracer = Tracer(service="file-upload-service")
app = ApiGatewayResolver()

@app.post("/files/upload-url")
@tracer.capture_method
def get_upload_url():
    try:
        # Lấy body từ request
        body = app.current_event.json_body
        file_name = body.get('fileName')
        content_type = body.get('contentType')
        folder_path = body.get('folderPath', 'default')
        
        if not file_name or not content_type:
            return Response(
                status_code=400,
                content_type="application/json",
                body=json.dumps({
                    "message": "fileName và contentType là bắt buộc"
                })
            )
        
        # Tạo unique key cho file
        key = f"{folder_path}/{int(time.time())}-{file_name}"
        attachments_bucket = os.environ.get('ATTACHMENTS_BUCKET')
        
        # Khởi tạo S3Utils từ common layer
        s3_utils = S3Utils(bucket_name=attachments_bucket)
        
        # Tạo presigned URL
        presigned_url = s3_utils.generate_presigned_url(
            key=key,
            http_method="PUT",
            content_type=content_type,
            expiration=3600
        )
        
        return Response(
            status_code=200,
            content_type="application/json",
            body=json.dumps({
                "uploadUrl": presigned_url,
                "key": key
            })
        )
    except Exception as e:
        logger.exception("Error creating presigned URL")
        return Response(
            status_code=500,
            content_type="application/json",
            body=json.dumps({
                "message": f"Error creating upload URL: {str(e)}"
            })
        )

@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context) 