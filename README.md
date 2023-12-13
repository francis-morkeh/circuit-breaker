# Circuit Breaker Script

## Description

This Python script utilizes a circuit breaker pattern to handle HTTP requests to a specific URL endpoint. It uses the `requests` library to make HTTP GET requests to `http://localhost:15000/status` with parameters for a password and SMS center. The script employs a circuit breaker mechanism from the `circuitbreaker` library to manage potential failures or overloads in the request.

## Requirements

- Python 3.x

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/francismorkehmensah/circuit-breaker.git
   cd circuit-breaker
   ```

2. Install Dependencies

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Execution

   ```bash
   ./circuit_breaker.py
   ```

   To make the script run continuously in the background on a Linux server
   ```bash
   nohup ./circuit_breaker.py > output.log 2>&1 &
   ```
   
2. Functionality

The script sends an HTTP GET request to http://localhost:15000/status with predefined parameters ('password': 'bar', 'smsc': 'ETISALAT_NG2'). It utilizes a circuit breaker pattern to manage potential failures or overloads when making the request.

Upon execution, it attempts to make the request. If successful (HTTP status code 200), it prints the response text. If it fails or encounters an error, it prints an error message along with the encountered exception.

## Note

Ensure the specified URL (http://localhost:15000/status) is reachable and the provided parameters are accurate.

Modify the URL, parameters, or circuit breaker settings (failure_threshold, recovery_timeout) within the script according to your requirements.
