# this is an official Python runtime, used as the parent image
FROM python:3.6.5-slim

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD . /app

# execute everyone's favorite pip command, pip install -r
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
# RUN pip3 install flask_sqlalchemy flask_marshmallow
RUN pip3 install -U flask-sqlalchemy 
# RUN pip3 install psycopg2-binary
# unblock port 80 for the Flask app to run on
EXPOSE 80

# execute the Flask app
# CMD ["python", "app.py"]
CMD ["flask", "run", "--host=0.0.0.0"]