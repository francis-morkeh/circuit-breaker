#!/usr/bin/env python3

"""
Circuit Breaker Script

Author:
Francis Morkeh Mensah

Date: 
14TH December 2023

Description:
Monitors a URL using a circuit breaker pattern, handling failures and sending email alerts.
Uses 'requests' for HTTP, 'circuitbreaker' for circuit state, and a command-line tool for emails.

Tutor:
- 'requests' for HTTP.
- 'circuitbreaker' for state management.
- Email alerts via command-line tool.

Purpose:
Ensure resilient monitoring, prevent cascading failures, and notify through email in case of issues.
"""

import requests
import time
import subprocess
from circuitbreaker import CircuitBreaker

# Define the URL and parameters
url = "http://localhost:15000/status"
params = {
    'password': 'bar',
    'smsc': 'ETISALAT_NG2'
}

# Define the circuit breaker
circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)

@circuit_breaker
def make_request():
    response = requests.get(url, params=params)
    return response

# Function to trigger the request and send alert if needed
def trigger_request():
    try:
        result = make_request()

        # Check if the circuit is open
        if circuit_breaker.state == 'open':
            print("Circuit is open. Sending alert...")
            email_content = f"<h3>The circuit for ETISALAT_NG2 is open. Please check.</h3>"
            send_email(email_content)

        # Check if the request is not successful
        elif result.status_code != 200:
            print("Request failed with status code:", result.status_code)
            email_content = f"<h3>Request failed, The request failed with status code: {result.status_code}</h3>"
            send_email(email_content)

        else:
            print("Request successful:", result.text)

    except Exception as e:
        print("Error making request:", str(e))
        email_content = f"<h3>Error making request, An error occurred: {str(e)}</h3>"
        send_email(email_content)

# Function to send email using command line tool
def send_email(content):
    email_command = f'echo "{content}" | /usr/local/bin/email -s "Circuit Breaker Notification: ETISALAT_NG2 Open" -html francis.mensah@rancard.com -cc derick.asamani@rancard.com,godwin.adade@rancard.com'
    
    try:
        subprocess.run(email_command, shell=True, check=True)
        print("Email sent successfully")

    except subprocess.CalledProcessError as e:
        print(f"Error sending email: {e}")
        print(f"Command output: {e.output.decode('utf-8')}")

# Run continuously in a loop
while True:
    trigger_request()

    # Sleep during the open state of the circuit breaker
    if circuit_breaker.state == 'open':
        time.sleep(circuit_breaker.next_attempt)  # sleep until the next attempt time

    # Add a delay to avoid constant requests and reduce load on the server
    time.sleep(60)  # sleep for 60 seconds
