import timesched
import requests
import os
import logging
import hashlib
import json
from datetime import datetime, time

logging.basicConfig(format='%(message)s',level=logging.INFO)
log = logging.getLogger(__name__)
EXPERIMENTO_ID = os.environ["EXPERIMENTO_ID"]
output_file_path = f"./src/monitor/outputs/{EXPERIMENTO_ID}.csv"
checksum_enable = os.environ["CHECKSUM_ENABLE"] == "true"

def check_healty_services():
    print(f'user service called at {datetime.now()}')
    USERS_BASE_URL = os.environ["SERVICE_BASE_URL"]
    url = USERS_BASE_URL + '/health'
    response = requests.request("GET", url)
    is_healthy = response.status_code == 200

    if(checksum_enable):
        md5_response = response.json()
        checksum = md5_response['checksum']
        expected_response_body = {"status": "healthy"}
        data_md5 = hashlib.md5(json.dumps(expected_response_body, sort_keys=True).encode('utf-8')).hexdigest()
   
        write_to_output(f'{datetime.now()};{data_md5};{checksum};{"ok"if(checksum==data_md5) else "fail"}')
    else:
        write_to_output(f'{datetime.now()};{"healthy"if(is_healthy) else "unhealthy"}')


# Create a scheduler
s = timesched.Scheduler()
def start_job():
    log.info(f'Job called at {datetime.now()}')
    if(checksum_enable):
        write_to_output("time;response;expected;result") 
    else:
        write_to_output("time;result")  

    # Execute job() every t secs
    t = int(os.environ["TIME_SCHEDULER_SECS"])
    s.repeat(t, 0, check_healty_services)
    # Run scheduler
    s.run()

def write_to_output(message):
    print(message)
    output_file =  open(output_file_path, "a")
    output_file.write(f"{message}\n")
    #output_file.close()


