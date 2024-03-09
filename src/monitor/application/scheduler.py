import timesched
import requests
import os
import logging
import hashlib
import json
from datetime import datetime, time

logging.basicConfig(format="%(message)s", level=logging.INFO)
log = logging.getLogger(__name__)
EXPERIMENTO_ID = os.environ["EXPERIMENTO_ID"]
output_file_path = f"./src/monitor/outputs/{EXPERIMENTO_ID}.csv"
checksum_enable = os.environ["CHECKSUM_ENABLE"] == "true"


def check_healty_services():
    print(f"user service called at {datetime.now()}")
    url = os.environ["SERVICE_BASE_URL"]
    response = requests.request("GET", url)
    status_code = response.status_code
    is_healthy = status_code == 200

    if checksum_enable:
        md5_response = response.json()
        checksum = md5_response["checksum"]
        expected_response_body = {"status": "healthy"}
        data_md5 = hashlib.md5(
            json.dumps(expected_response_body, sort_keys=True).encode("utf-8")
        ).hexdigest()

        write_to_output(
            f'{datetime.now()};{data_md5};{checksum};{"ok"if(checksum==data_md5) else "fail"}',
            "a",
        )
    else:
        write_to_output(
            f'{datetime.now()};200;{status_code};{"ok"if(is_healthy) else "fail"}', "a"
        )


# Create a scheduler
s = timesched.Scheduler()


def start_job():
    log.info(f"Job called at {datetime.now()}")
    write_to_output("time;response;expected;result", "w")
    # Execute job() every t secs
    t = int(os.environ["TIME_SCHEDULER_SECS"])
    s.repeat(t, 0, check_healty_services)
    # Run scheduler
    s.run()


def write_to_output(message, mode):
    print(message)
    output_file = open(output_file_path, mode)
    output_file.write(f"{message}\n")
    # output_file.close()
