class S3ExportConfiguration:

	def __init__(self, bucket_name, pub_key, priv_key, session_key):
		self.bucket_name = bucket_name
		self.pub_key = pub_key
		self.priv_key = priv_key
		self.session_key = session_key

	class Builder:

		def bucket_name(self, bucket_name):
			self.bucket_name = bucket_name
			return self

		def pub_key(self, pub_key):
			self.pub_key = pub_key
			return self

		def priv_key(self, priv_key):
			self.priv_key = priv_key
			return self

		def session_key(self, session_key):
			self.session_key = session_key
			return self

		def build(self):
			return S3ExportConfiguration(self.bucket_name, self.pub_key, self.priv_key, self.session_key)

		


