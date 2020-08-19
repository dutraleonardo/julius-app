FROM python:3.8.2
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy --dev
COPY . /code/
