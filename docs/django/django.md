## How to create Django projects

We use docker-compose for doing so. we have to mention the name of the service in the command and actual command to use

`docker-compose run app sh -c "django-admin.py startproject app ."`

## Creating core app

It's good idea to create a core application which holds common aspect of our application like database and it's models.

`docker-compose run app sh -c "python manage.py startapp core"`

We deleted `tests.py` for sake of having clreat structure of our project we put tests in it's folder in case we have multiple tests files
we need to create following structure: `core/tests/__init__.py`
