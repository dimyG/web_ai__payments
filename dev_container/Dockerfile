FROM python:3.10.10-bullseye

# the WORKDIR within the container
WORKDIR /usr/src/payments_src

# the COPY from path is relative to the build context, not to the Dockerfile
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y
RUN apt-get install -y binutils libproj-dev vim

# These are non essential libraries
# RUN apt-get install -y net-tools

COPY ./ ./

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8001"]