from ..tenant_config.get_tenant_config import *
from .config_exporter_registry import *
from ..common.call_export_record import call_export_record

def export_all(tenant, record):
	configs = get_tenant_configs(tenant)
	for key, config in configs:
		call_export_record(key, config, record)


		



