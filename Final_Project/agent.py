import psutil
import time
import json
import boto3
import math
from datetime import datetime
from config import Config

MACHINEID = 2

# lambda client
lambda_client = boto3.client('lambda',
            aws_access_key_id = Config.ACCESS_KEY_ID,
            aws_secret_access_key = Config.SECRET_KEY,
            region_name = Config.REGION)

# data collection
# cpu_util, mem_util, disk_util, all in percentage
while True:
	time_stamp = math.floor(time.time() / 60)
	data = {}
	cpu_util = psutil.cpu_percent(interval=None)
	mem_util = psutil.virtual_memory()
	mem_util = mem_util.percent
	disk_util = psutil.disk_usage('/')
	disk_util = disk_util.percent
	data['timestamp'] = time_stamp
	data['metric_names'] = ['cpu_util', 'mem_util', 'disk_util']
	data['metric_values'] = [cpu_util, mem_util, disk_util]
	data['machineid'] = MACHINEID
	json_data = json.dumps(data, sort_keys=True, default=str)

	print(json_data)

	# invoke lambda
	response = lambda_client.invoke(FunctionName='testFunction', Payload= json_data)

	print(response)
	time.sleep(60)
