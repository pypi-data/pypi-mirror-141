import requests
import os
# call the export record function over http from another function

def call_export_record(location_key, config, record):
	export_record_url = os.getenv("export_record_url")
	data = {
		"location_key": location_key,
		"config": config,
		"record": record,
	}

	requests.post(export_record_url, data=data)



	