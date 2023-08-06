import json
from datetime import datetime
from .s3_export_schema import S3ExportSchema

def transform_record(input_record):
	# make input into an s3_export_schema
	timestamp = str(datetime.now())
	key_suffix = "test_record.json"
	key_name = f"{timestamp}{key_suffix}"
	return S3ExportSchema(key_name, input_record.data)