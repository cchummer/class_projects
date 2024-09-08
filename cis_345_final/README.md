# Final Project CIS 345
Business Information Systems Development II (AKA my Python class):

'At the end of this course students will have the ability to 1) demonstrate a comprehensive understanding of object-oriented programming techniques, 2) utilize APIs, 3) apply the Systems Development Life Cycle (SDLC) tools, techniques, and methodologies, and 4) develop applications making use of micro-services.'

This final project involved creating a GUI based python application which called a public API of our choice. I chose to create an app which would provide delay information based on a customer's flight. See my FAA repo for more code playing with FAA endpoinds.


## Install required libraries
Ensure that you are in the main directory and 
run the following:

_This must be done before you can run the application
if you are not using the included venv._

```shell
$ pip install json
$ pip install requests
$ pip install bs4
$ pip install lxml
$ pip install PIL
$ pip install tkinter
$ pip install pytest
```

## To run the program
Click the green triangle run icon in the 
top-right corner of the PyCharm window.
or
```shell
$ python3 app.py
```

## Functionality
### Search for an airport
An FAA endpoint will be queried, and results filtered for the respective airport. A list of relevant closures and delays will be output to the GUI, including their types and start/end times.

### Exit
The application will be closed when the Exit
button is clicked.

## Data files
### queries.json
The file contains the transaction data in the 
following format:
```json
{"query_time": "2024-04-25 22:43:47", "airport": "LGA", "is_departing": true, "events_list": [[{"type": "airport_closure", "reason": "!LGA 04/094 LGA AD AP CLSD EXC 4HR \rPPR 718-533-3700 DLY 0401-1000 2404150401-2411021000", "start": "Apr 15 at 04:01 UTC.", "reopen": "Nov 02 at 10:00 UTC."}]]}{"query_time": "2024-04-25 22:43:53", "airport": "BOS", "is_departing": true, "events_list": [[{"type": "airport_closure", "reason": "!BOS 04/191 BOS AD AP CLSD TO NON SKED TRANSIENT GA ACFT PPR 617-561-2500 2404110900-2406152359", "start": "Apr 11 at 09:00 UTC.", "reopen": "Jun 15 at 23:59 UTC."}]]}{"query_time": "2024-04-25 22:44:23", "airport": "SFO", "is_departing": true, "events_list": [[{"type": "ground_delay", "reason": "runway construction", "avg": "1 hour and 41 minutes", "max": "2 hours and 53 minutes"}]]}
```

## Class

### AirportQuery Class

#### Variables
Each AirportQuery instance has the following instance
variables:
1. airport_name: private, string data type
2. query_time: private, string data type
3. departing: private, boolean data type
4. delay_list: private, list data type

Each Account instance has the following properties:
- airport_name getter
- airport_name setter
- query_time getter
- query_time setter
- departing getter
- departing setter
- delay_list getter
- delay_list setter

#### Methods
The AirportQuery class has the following methods:
* The dunder__init__ method
* The dunder__str__ method

## Auto Testing
Run the following command to test the 
test_airportevents.py file.  There are 3 test cases.

```shell
$ pytest -v test_airportevents.py
```

