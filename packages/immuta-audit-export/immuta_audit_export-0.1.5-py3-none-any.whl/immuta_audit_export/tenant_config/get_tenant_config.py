from ..common.config_schemas import s3_config
import json

def get_tenant_config(tenant_id):
	# todo set the aws values
	# todo document this
	aws_secret_access_key = "test"
	aws_access_key_id = "test"
	aws_session_token = "test"
	config_builder = S3ExportConfiguration.Builder()
	config = config_builder.bucket_name("luke-boyer-audit-test").priv_key(aws_secret_access_key).session_key(aws_session_token).pub_key(aws_access_key_id).build()
	return json.dumps(config.to_dict())