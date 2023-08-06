class S3ExportConfiguration:

	def __init__(self, bucket_name, aws_access_key_id, aws_secret_access_key, aws_session_token):
		self.bucket_name = bucket_name
		self.aws_access_key_id = aws_access_key_id
		self.aws_secret_access_key = aws_secret_access_key
		self.aws_session_token = aws_session_token

	class Builder:

		def bucket_name(self, bucket_name):
			self.bucket_name = bucket_name
			return self

		def aws_access_key_id(self, aws_access_key_id):
			self.aws_access_key_id = aws_access_key_id
			return self

		def aws_secret_access_key(self, aws_secret_access_key):
			self.aws_secret_access_key = aws_secret_access_key
			return self

		def aws_session_token(self, aws_session_token):
			self.aws_session_token = aws_session_token
			return self

		def build(self):
			return S3ExportConfiguration(self.bucket_name, self.aws_access_key_id, self.aws_secret_access_key, self.aws_session_token)

# need to serialize/de- 

	def to_dict(self):
		return self.__dict__

	@staticmethod
	def from_dict(d):
		return S3ExportConfiguration(**d)



