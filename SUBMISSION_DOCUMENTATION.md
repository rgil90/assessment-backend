Submission Documentation
-------------------------

### Stack
* Database - Postgres 13 (Docker)
* Operating System - Ubuntu 20.04 (python 3.9.5 slim)
* Server - Django 3.2.5 (Docker)
* Python - 3.9.5
* Package Manager - pip3 with requirements.txt
* Testing - Django Test Runner
* Serialization - Django Rest Framework

### Setup
* run `docker-compose up` to start the database and server
* in a separate terminal, run `docker-compose run --rm app migrate` to run the database migrations (optional - there's already a docker-compose service that handles this for you)
* in a separate terminal, run `docker-compose run --rm app createsuperuser` to create a superuser (optional)
* in a separate terminal, run `docker-compose run --rm app shell` to open a django shell session (optional)
* in a separate terminal, run `docker-compose run --rm app makemigrations` to create new migrations (optional)

A few notes:
* The database is not seeded with any data
* I changed the source for pypi from a Pipfile to requirements.txt
* I also added a convenience `docker-entrypoint.sh` file to make it easier to run commands in the docker container.
* The Operating System for the docker container is not alpine! There are notes in the Dockerfile about that.
* I moved the `manage.py` file into the `assessment` directory. This makes it easier to work with for me and potentially other developers.
* I added an `apps` directory to the `assessment` directory. This is where I put all of the Django apps for the project. I did this because I like to keep my project structure clean and organized. I also like to keep my apps separate from the project root.

### API
* The API root is at `http://localhost:8000/api/v1/` - it will display a list of available endpoints

#### Objects
* The objects endpoint is at `http://localhost:8000/api/v1/objects/`
* The objects endpoint supports GET, POST, and DELETE
* The objects endpoint supports filtering by `data` key and value
* The objects endpoint supports pagination (default page size is 10) - the page size is configurable in `settings.py`
* To create an object, POST a JSON object with the following format:
```
{
    "batch_id": "<batch_id>",
    "object_id": "d6f983a8905e48f29ad480d3f5969b52",
    "data": [
            {
                    "key": "<key-name>",
                    "value": "<value-name>"
            },
    ]
}
```

**Note:** You must create a batch first using the POST request to `/api/v1/batches` before you can assign an object to a batch individually.
For a much more seamless experience, I would recommend using the `/api/v1/batches` API endpoint. See next bullet point below.

* As a test you can just grab the data from the `files` directory and POST it to the batches endpoint (e.g. `http://localhost:8000/api/v1/batches/)

* To retrieve an object, GET the object's `object_id` from the objects endpoint (e.g. `http://localhost:8000/api/v1/objects/1/`)
* To delete an object, DELETE the object's `object_id` from the objects endpoint (e.g. `http://localhost:8000/api/v1/objects/1/`)
* To filter objects by `data` key and/or value, add a query parameter to the objects endpoint (e.g. `http://localhost:8000/api/v1/objects/?data={"key": "value"}`)

#### Batches
* The batches endpoint is at `http://localhost:8000/api/v1/batches/`
* The batches endpoint supports GET, POST, and DELETE
* The batches endpoint supports pagination (default page size is 10) - the page size is configurable in `settings.py`
* The batches endpoint supports filtering by the related objects' `data` key and value
* To create a batch, POST a JSON object with the following format:
```
{
    "batch_id": "<batch-id>",
    "objects": [
        {
            "object_id": "<object-id>",
            "data": [
                {
                    "key": "<key-name>",
                    "value": "<value-name>"
                },
            ]
        }
    ]
}
```
* To retrieve a batch, GET the batch's `batch_id` from the batches endpoint (e.g. `http://localhost:8000/api/v1/batches/1/`)
* To delete a batch, DELETE the batch's `batch_id` from the batches endpoint (e.g. `http://localhost:8000/api/v1/batches/1/`)
  * Before deleting a batch, all related objects must be deleted first. This is enforced by the database. If you try to delete a batch that has related objects, you will get a 500 error.
* To filter batches by the related objects' `data` key and/or value, add a query parameter to the batches endpoint (e.g. `http://localhost:8000/api/v1/batches/?data={"key": "value"}`)

### Proposed Improvements
Given more time, I would have liked to improve the following areas:
* Testing
  * Add unit and integration tests to ensure that the API can handle non-happy path scenarios.
  * Add load testing to ensure that the API can handle a large number of requests. Or at least get an idea of how many requests it can handle.
* Security
  * I would have liked to enforce sending a valid API key with each request as a start.
  * I would have also liked to add rate limiting to the API. Especially with an API like this (which seems read-heavy), I would have liked to add rate limiting to prevent malicious users from overloading the API.
  * To detect malicious requests, I would even expose Canary keys that would be used to detect if a user is using a malicious API key.
* Logging
  * I would have liked to add logging to the API. This would allow us to track API usage and detect malicious activity.
  * I would also use logging to track errors and exceptions.
  * I would use logging to track performance at various parts of the stack (e.g. database, server, etc.)
* Monitoring
  * I would add an APM tool to the API like DataDog or New Relic. This would allow us to monitor the performance of the API and detect when it is slow.
  * As an alternative to a paid solution, I would use OpenTelemetry with the Jaeger collector to monitor the API and deploy it as a Container in the cloud.
* Health Checks
  * I would have liked to add health checks to the API.
    * This would allow us to monitor the health of the API and detect when it is down/unhealthy.
* Deployments
  * I would use Kubernetes to deploy the API. This would allow us to scale the API horizontally and vertically.
  * This would also allow us to deploy the API in multiple environments (e.g. dev, staging, prod) pretty easily.
  * I would also use a CI/CD pipeline to deploy the API. This would allow us to deploy the API automatically when code is merged into the main branch.
* Database
  * I might also be inclined to use a different database. I chose Postgres because I'm most familiar with it, and it was the one that came packaged with the
project. However, for an API like this, I would probably use a NoSQL database long-term.
  * I would probably use MongoDB because it would allow us to store the objects in a more flexible way. I'm aware however, that it doesn't
  come without its own set of tradeoffs. For example, what happens when we need to change the schema? Do we care about referential integrity?
  Those are some of the questions that would need to be answered before making a decision like that.
  But for this kind of API, that could warehouse billions of data points, I would be looking to move towards
  a NoSQL solution.
  * If we ever store sensitive data (such as passwords, or PII), I would also look into using a database that supports encryption at rest and in-transit.
* Language/Framework
  * Python is awesome for getting things up and running quickly. However, I would probably use a different language/framework for an API like this.
  * I would probably use Rust with a framework like Actix. Rust is a compiled language, which means it is fast.
    * It also has a lot of great features that make it a great choice for building APIs such as concurrency, memory safety, and type safety.
    * Using a compiled language would also allow us to take advantage of the performance benefits of using a compiled language and server efficiency, effectively reducing the cost of running the API because we'd need less resources to run the API.
    * One of the tradeoffs is that it is a compiled language, which means it is not as easy to iterate quickly on new features until the team gets familiar with the language.
    * However, I think the benefits of using a compiled language outweigh the cons. Especially for an API like this, that could be handling a lot of data.


There are definitely more improvements to make, but these are the ones that come to mind at the moment.
Based on the use cases of the API, we can prioritize which improvements to make first. I'm happy to discuss this
in further detail, perhaps do a little system design exercise to discuss the tradeoffs of each approach :)
