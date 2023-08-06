from ..tenant_config.get_tenant_config import *
from .config_exporter_registry import *

def export_all(tenant, record):
	configs = get_tenant_configs(tenant)

	for key, config in configs:
		# call the other function over da wire




