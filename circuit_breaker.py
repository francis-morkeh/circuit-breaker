#!/usr/bin/env python3

import requests
from circuitbreaker import CircuitBreaker, circuit

# Define the URL and parameters
url = "http://localhost:15000/status"
params = {
    'password': 'bar',
    'smsc': 'ETISALAT_NG2'
}

# Define the circuit breaker
@CircuitBreaker(failure_threshold=3, recovery_timeout=10)
def make_request():
    response = requests.get(url, params=params)
    return response

# Function to trigger the request
def trigger_request():
    try:
        result = make_request()
        if result.status_code == 200:
            print("Request successful:", result.text)
        else:
            print("Request failed with status code:", result.status_code)
    except Exception as e:
        print("Error making request:", str(e))

# Trigger the request
trigger_request()
