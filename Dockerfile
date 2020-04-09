FROM python:3.7


RUN mkdir /app
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt

# Install the pip requirements file depending on
# the $ENV build arg passed in when starting build.
RUN pip install -Ur requirements.txt

# Copy the rest of our application.
COPY . /app/


# Run migration
CMD ["python", "manage.py", "migrate"]
# Run test server
CMD ["python", "manage.py", "runserver"]