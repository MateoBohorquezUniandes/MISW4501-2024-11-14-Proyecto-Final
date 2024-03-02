import timesched
import requests
import os
import logging
from datetime import datetime, time

logging.basicConfig(format='%(message)s',level=logging.INFO)
log = logging.getLogger(__name__)
EXPERIMENTO_ID = os.environ.get("EXPERIMENTO_ID")
output_file_path = f"./src/monitor/outputs/{EXPERIMENTO_ID}.csv"

def check_healty_services():
    print(f'user service called at {datetime.now()}')
    USERS_BASE_URL = os.environ["USERS_BASE_URL"]
    url = USERS_BASE_URL + '/health'
    response = requests.request("GET", url)
    is_healthy = response.status_code == 200
    write_to_output(f'{datetime.now()};users;{"healthy"if(is_healthy) else "unhealthy"}','a')


# Create a scheduler
s = timesched.Scheduler()
def start_job():
    log.info(f'Job called at {datetime.now()}')  
    #write_to_output("time;service name;result","w")  
    # Execute job() every t secs
    t = int(os.environ["TIME_SCHEDULER_SECS"])
    s.repeat(t, 0, check_healty_services)
    # Run scheduler
    s.run()

def write_to_output(message, mode):
    print(message)
    output_file =  open(output_file_path, mode)
    output_file.write(f"{message}\n")
    #output_file.close()


