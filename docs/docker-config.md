# How docker file is made

## Where is docker file ?

In root of project create a file called **Dockerfile**.

## What does each line of file do ?

First line is image we are going to inherit for our docker file. this project is built on python 3.7 we can go to https://hub.docker.com/ and look for python 3.7 alpine image. (alpine if for lightweight version of docker)


```
FROM python:3.7-alpine
```
***

Second line is maintainer line which means who is going to maintain this image.

```
MAINTAINER Seyedamir Tadrisi
```
***


Third line is setting env variable for python unbuffered. what this variable does it makes python to run in unbuffered mode which is recommended for python running in docker.

```
ENV PYTHONUNBUFFERED 1
```
***


4th and 5th line is for Installing dependencies, copying project `requirements.txt` to docker `/requirements.txt`

```
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
```
***

Next is to Make directory to store our app there

```
RUN mkdir /app
WORKDIR /app
COPY ./app /app
```
***

And Create a user that run our application, `-D` means user for running app only

```
RUN adduser -D user
USER user
```

## How to run it ?

Navigate to root of the project where docker file exist and run `docker build .`


# Troubleshooting

if during the `docker build .` you get ` unauthorized: incorrect username or password` make sure in CLI you `docker logout` and `docker login` using your docker id not your email.
