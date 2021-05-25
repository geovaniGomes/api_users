#pull official base image
FROM python:3.8



# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip setuptools


RUN mkdir /code

# set work directory
WORKDIR /code

# create and activate virtual environment
RUN python -m venv env


# copy and install pip requirements 
COPY src/requirements.txt  code/src/requirements.txt

RUN pip install -r code/src/requirements.txt

# copy Django project files

COPY . .