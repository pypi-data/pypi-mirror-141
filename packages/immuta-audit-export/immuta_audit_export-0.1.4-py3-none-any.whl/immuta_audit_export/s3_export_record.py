from s3_transform_record import transform_record
import boto3	
import json

class S3ExportRecord:

	def __init__(self, config):
		self.config = config
		self.transform_record = transform_record
		self._bucket = None

	def _make_bucket(self):
		session_kwargs = {
			"aws_access_key_id":self.config.pub_key,
			"aws_secret_access_key":self.config.priv_key,
			"aws_session_token":self.config.session_key
		}

		session = boto3.Session(**session_kwargs)

		self._bucket = session.resource('s3').Bucket(self.config.bucket_name)


	@property
	def _s3_bucket(self):
		if self._bucket is None:
			self._make_bucket()
		return self._bucket
		
	def export_record(self, input_record):
		s3_export_record = self.transform_record(input_record)
		key_name = s3_export_record.key_name
		json_body = s3_export_record.json_body

		bucket = self._s3_bucket

		bucket.put_object(Key=key_name, Body=bytes(json.dumps(json_body).encode('UTF-8')))

