import os
import json
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, Response
from src.common.s3 import create_presigned_get_url, check_object_exists

logger = Logger(service="file-download-service")
tracer = Tracer(service="file-download-service")
app = ApiGatewayResolver()

@app.get("/files/download-url")
@tracer.capture_method
def get_download_url():
    try:
        # Lấy query parameters
        key = app.current_event.get_query_string_value(name="key", default_value=None)
        bucket_name = app.current_event.get_query_string_value(name="bucket", default_value=None)
        
        if not key:
            return Response(
                status_code=400,
                content_type="application/json",
                body=json.dumps({
                    "message": "key là bắt buộc"
                })
            )
        
        # Xác định bucket
        if not bucket_name:
            bucket_name = os.environ.get('ATTACHMENTS_BUCKET')
        
        # Kiểm tra file có tồn tại không
        if not check_object_exists(bucket_name, key):
            return Response(
                status_code=404,
                content_type="application/json",
                body=json.dumps({
                    "message": f"File không tồn tại: {key}"
                })
            )
        
        # Tạo presigned URL
        download_url = create_presigned_get_url(
            bucket_name,
            key
        )
        
        return Response(
            status_code=200,
            content_type="application/json",
            body=json.dumps({
                "downloadUrl": download_url,
                "key": key
            })
        )
    except Exception as e:
        logger.exception("Error creating download URL")
        return Response(
            status_code=500,
            content_type="application/json",
            body=json.dumps({
                "message": "Error creating download URL"
            })
        )

@tracer.capture_lambda_handler
def handler(event, context):
    return app.resolve(event, context) 