from ..common.config_schemas.s3_config import S3ExportConfiguration
from .s3.s3_export_record import S3ExportRecord

location_key_map = {
	"s3": (S3ExportConfiguration.from_dict, S3ExportRecord)
}

def get_export_objs(location_key):
	return location_key_map[location_key]
