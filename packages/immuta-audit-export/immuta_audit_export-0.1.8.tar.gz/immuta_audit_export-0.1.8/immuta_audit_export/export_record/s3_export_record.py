from .s3_transform_record import transform_record
from datetime import datetime
import boto3	
import json

class S3ExportRecord:

	def __init__(self, config):
		self.config = config
		self._bucket = None

	def _make_bucket(self):
		session_kwargs = {
			"aws_access_key_id":self.config.aws_access_key_id,
			"aws_secret_access_key":self.config.aws_secret_access_key,
			"aws_session_token":self.config.aws_session_token
		}

		session = boto3.Session(**session_kwargs)

		self._bucket = session.resource('s3').Bucket(self.config.bucket_name)

	import json

	def _transform_record(self, input_record):
		# make input into an s3_export_schema
		timestamp = str(datetime.now())
		key_suffix = "test_record.json"
		key_name = f"{timestamp}{key_suffix}"
		return (key_name, input_record)

	@property
	def _s3_bucket(self):
		if self._bucket is None:
			self._make_bucket()
		return self._bucket
		
	def export_record(self, input_record):
		key_name, json_body = self._transform_record(input_record)

		bucket = self._s3_bucket

		bucket.put_object(Key=key_name, Body=bytes(json.dumps(json_body).encode('UTF-8')))

