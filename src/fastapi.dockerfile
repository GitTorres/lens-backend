# pull from official base image (switch to alpine to dec image size)
FROM python:3.8.10-alpine as dev

# create /app folder
RUN mkdir /app

# set work directory
WORKDIR /app

RUN echo $MONGODB_USER

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY app/requirements.txt /app/requirements.txt

# install dependencies
RUN pip install --no-cache-dir --upgrade  -r requirements.txt

# open up webserver port
EXPOSE 8000

# remove folder. the compose file will set it up as a volume for hot reloading
RUN rm -rf /app

# production image
FROM dev as prod

# copy app files, except for what is excluded via .dockerignore
COPY . .