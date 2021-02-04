#	Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START docker]

# The Google App Engine python runtime is Debian Jessie with Python installed
# and various os-level packages to allow installation of popular Python
# libraries. The source is on github at:
# https://github.com/GoogleCloudPlatform/python-docker

# START Production Docker
# FROM gcr.io/google_appengine/python

# # Create a virtualenv for the application dependencies.
# RUN virtualenv -p python3 /env
# ENV PATH /env/bin:$PATH

# ADD requirements.txt /app/requirements.txt
# RUN /env/bin/pip install --upgrade pip && /env/bin/pip install -r /app/requirements.txt
# ADD . /app

# CMD gunicorn -b :$PORT mysite.wsgi
# END Production Docker

# START Development Docker
FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

EXPOSE 8080

# COPY . /code/
# END Development Docker

# [END docker]
