# What is Travis-CI config file

This is a file tells travis what to do when we push something to the project repo.


## How to create config file

We need to create a **YML** file in the root of our project file. file should called `.travis.yml`


## What does it contain

we include language of our application which is python, version of the python we are using, services need to use,
all sub-services are contained in docker file and compose file.

- before_script: group of scripts it runs before it execute any automation command

every time we push something to repo travis will spin up new server with python, install docker and compose and run our script

```
anguage: python
python:
  - "3.6"

services:
  - docker

before_script: pip install docker-compose

script:
  - docker-compose run app sh -c "python manage.py test && flake8"
```
