import timesched
import requests
import os
import logging
from datetime import datetime, time

logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)

def check_healty_services():
    print(f'user service called at {datetime.now()}')
    USERS_BASE_URL = os.environ["USERS_BASE_URL"]
    url = USERS_BASE_URL + '/health'
    response = requests.request("GET", url)
    if(response.status_code != 200):
        log.info(f'todo bien')
    else:
        log.info(f'todo mal')


# Create a scheduler
s = timesched.Scheduler()
def start_job():
    log.info(f'Job called at {datetime.now()}')    
    # Execute job() every t secs
    t = os.environ["TIME_SCHEDULER_SECS"]
    s.repeat(t, 0, check_healty_services)
    # Run scheduler
    s.run()




