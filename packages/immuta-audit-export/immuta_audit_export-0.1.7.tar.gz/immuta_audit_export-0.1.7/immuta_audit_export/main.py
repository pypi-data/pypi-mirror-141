from immuta_audit_export.common.config_schemas.s3_config import S3ExportConfiguration
import json
from immuta_audit_export.export_record.export_record_registry import *

test_load = {
	"location_key": "s3",
	"config": {
		"aws_access_key_id":"ASIAQFZE4EV56ABVDCLL",
		"aws_secret_access_key":"FVhM60nKBWfu6OGZkWsN/gnKZJthRBXvM3tePUyF",
		"aws_session_token":"IQoJb3JpZ2luX2VjEDIaCXVzLWVhc3QtMSJIMEYCIQDTLaRzCSnuhlSgFwAh3ugm4OfB3ELemdu75qvttR+aewIhAJ/SR/oQqtn0UN8OWFxN3HyiGB62cv8U/+KeQV4w1gepKpwDCJr//////////wEQAxoMMDEyNDI1MzczMDUxIgx9X9SWI0nvElDCcp8q8AJGpzYiauxwnQ0vgS4vtimhzZD4DwHoWMwfAGAdgq1Vz6TypkRTYFF1HHAM+QX1O7UH2f+at9k8WfbemnSLz3z+JLiiOAJtLf6ao2bXITTD0rlfbqptCSCMSZw2cbJA8bzkmP48utO4KCYSxD5K+fDtUYOTuvHDfZ9bPIw1fUsR03KXvWHwwQU8LRyLuzlLEq9r6odagdygcYQzYp5QB2LZEK+tNlxJBNN3FvosyU3d3cZLPyRsk0eCZHnTmIa/8Da7AlYK37KMLQ6PSMdqLH9mE7q4dTbtGa3VhWgOPCOdaX866XLgox150zGJXdWiLwo7mBhiS6dXta5RCp7EYQW+3XSrLbcAnLZPqrvhHEPQ1lwkiC6mWO2lqpBTpM+NEhkZk+ExQjZSvOAGJ3gupv17rY4Xi+md6fxsxcmHs/LTFPgYWpGcb6U/8+kKueKVARI9HcyrUR1tGeEHI/ajPP6WRevxsh3xDi2fGjIpHvgUfTC+tZWRBjqlAQmJQ9hDqJE/4YpZxUH8R2Yyqwg/ujlINbhF4nEKQbHnGwbOqHhkm6lrRQ3qEWvj49of5XL67iDN5FZrtyMHF2RfYhH/LYaXnsr37Y2KCrFTMLiPjJiggq9EHuTfDn+QGlbyOkE19UqY+1VtCUramkBoddJ/wqSJXPeTjBsC+2cdXbWFZVzBuhJaanlTKYBBBReyRVBnkD1e3fI4ZZRQNl1kP/dmMQ==",
		"bucket_name":"luke-boyer-audit-test"
	},
	"record": {
		"somestuff": "test audit data"
	}
}
if __name__ == "__main__":
	json_req = test_load
	location_key = json_req["location_key"]
	config_data = json_req["config"]
	record_data = json_req["record"]

	config_obj, exporter_obj = get_export_objs(location_key)

	exporter = exporter_obj(config_obj(config_data))
	exporter.export_record(record_data)
	print("it works")