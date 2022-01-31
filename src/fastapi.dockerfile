# pull from official base image (switch to alpine to dec image size)
FROM python:3.8.10

# create /app folder
RUN mkdir /app

# set work directory
WORKDIR /app

# set environment variables (can also set in docker-compose)
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY app/requirements.txt /app/requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# open up webserver port
EXPOSE 8000

# remove folder since we mount with docker compose
RUN rm -rf /app