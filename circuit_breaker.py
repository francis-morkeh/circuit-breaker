#!/usr/bin/env python3

import requests
import time

FAILURE_THRESHOLD = 3
RECOVERY_TIMEOUT = 10

url = "http://localhost:15000/status"
params = {
    'password': 'bar',
    'smsc': 'ETISALAT_NG2'
}

consecutive_failures = 0
circuit_opened = False
last_failure_time = 0

def make_request():
    global consecutive_failures, circuit_opened, last_failure_time
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            print("Request successful:", response.text)
            consecutive_failures = 0
            circuit_opened = False
        else:
            handle_failure()
    except Exception as e:
        handle_failure()

def handle_failure():
    global consecutive_failures, circuit_opened, last_failure_time
    consecutive_failures += 1
    if consecutive_failures >= FAILURE_THRESHOLD:
        circuit_opened = True
        last_failure_time = time.time()
        print("Circuit opened. Waiting for recovery...")
    else:
        print("Failure occurred. Count:", consecutive_failures)

def trigger_request():
    global circuit_opened, last_failure_time
    if circuit_opened:
        if time.time() - last_failure_time >= RECOVERY_TIMEOUT:
            print("Circuit recovered. Trying request again.")
            circuit_opened = False
            make_request()
        else:
            print("Circuit still open. Waiting for recovery...")
    else:
        make_request()

# Trigger the request
trigger_request()