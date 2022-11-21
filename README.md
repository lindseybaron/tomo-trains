## Notes
App can be run and tested as described [here](#Template)

Schedule times are accepted as an int in HHMM format, without leading 0's.

Currently, there's no way to update an existing train's schedule, because I included validation to prevent duplicate trains from being created, and the directions say to use only the existing methods in the Database class. I would have liked to add an update method that would allow for this, which would also leverage Database().set(), but with modified validation (assert the train exists, don't error if it does).

For scalability purposes, I would probably use a sqlite instance and leverage sqlalchemy to easily manage train and schedule objects in separate tables, so additional information could be added, i.e. details about the train such as size, details about each train 'time', i.e. arrival, departure, bay, etc.

Schemas would be nice to more cleanly handle request validation and response formatting.

As a user, I would have found it helpful to have the API return the train id along with the schedules/times, but the acceptance requirements specifically says to return the schedule. That's what it's currently doing, but should product decide to make that change, it would be pretty easy to do.

I have some thoughts/questions about the thread safety bit of the directions, but I'd prefer to discuss that during the interview.

## Context
Tomo is building a service for the local transit authority.

Initially the service will support a single train station with an arbitrary number of train lines running through it, like the Fulton Street station, which hosts the 2, 3, 4, 5, A, C, J, and Z lines.
  
We would like the service to manage the schedules of the trains in this station, recording when they arrive as well as reporting when multiple trains are in the station at the same time.

## Objective & Requirements

Write a small API web service that provides endpoints to track and manage the train schedules for the station and the data storage mechanism for it.

### Service Capability  

The web service should provide a means for clients to post a schedule for a new train line that runs through this station and verify its correctness:

- A request to `/trains` should accept a train identifier (a string that contains up to four alphanumeric characters, e.g. ‘EWR0’, ‘ALP5’, ‘TOMO’, etc.) and a list of times when the train arrives in the station
- A request to `/trains/<train_id>` should provide the schedule for the specified train identifier
- A request to `/trains/next` should return the time two or more trains will be in the station.    
     
### Data Storage Capability

This web service uses a key-value store for keeping state, with the following functions:  

- A *db.set(key, value)* method to set the value associated with a key.    
    
- A *db.get(key)* method to retrieve the object set at a key.  
    
- A *db.keys()* method to return the list of all defined keys in the database. This function returns an empty list if none have been defined.  
      
The service should be threadsafe and use this hypothetical key-value store (with only these three methods available).
      
## Template

We've provided a template Python project using [Flask](https://flask.palletsprojects.com/en/2.0.x/]).  We recommend using it, though a submission in any language of your choice is acceptable, provided it meets the requirements provided above and includes documented tests demonstrating the service contract.

Following the steps below will provide you with a running Flask instance capable of receiving requests, template unit tests, and implementation hints.

1. Download the latest major version of Python (3.9.8+)
2. Start virtualenv, install the requirements and start flask, as below:
```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ flask run
```

To verify that Flask is running the template service, issue a CURL (or browser request) to http://127.0.0.1:5000/, e.g.
```bash
% curl -I http://127.0.0.1:5000/ 
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 2
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Fri, 12 Nov 2021 01:42:25 GMT                       
```

To run the test suite, simply execute pytest; you should expect to see some fail until you have implemented them.
```bash
$ pytest
```

We will assume that your submission retains these characteristics and can be started using ```$ flask run``` and tested using ``` $ pytest ```, with the provided tests passing, as well as any additional ones you add. You are free to vary from this template, but include notes for the reviewer, if so.

### Assumptions

- All trains have the same schedule each day (i.e. no special schedules for weekends and holidays).  
    
- If there are no times after the specified time value when multiple trains will be in the station simultaneously, the service should "wrap around" and return the first time of the day when multiple trains arrive at the station simultaneously (tomorrow, perhaps)        
    
- If there are no instances when multiple trains are in the station at the same time, this method should return no time.

You may define the API contract for this service however you wish, including the format used for accepting and returning time arguments. The endpoint should return a 2XX response for valid requests, and a 4xx request for invalid requests (with actual HTTP code at your discretion).



## Expectations and Assumptions

- You can use whatever language, framework, and tools you feel most comfortable with.
    
- You can use whatever dependencies are useful to solve the problem.

- You do not need to worry about user authentication or authorization; all endpoints can be public to anonymous users.
    
- It’s OK (and encouraged) to make additional assumptions that aren’t encoded in this prompt.      
    
- You may ask any questions you need to pursue this prompt, including questions to clarify assumptions around performance requirements, scale, etc.




## Submission

You may submit in one of two ways:

- ZIP the source code (and any supplemental documentation) and return it as an email attachment.  
- Commit and push the code to an accessible GitHub/GitLab/etc. repository
