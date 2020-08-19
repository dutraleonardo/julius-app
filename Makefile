all: build migrate clean

up:
	docker-compose up -d

stop:
	docker-compose stop

build:
	docker-compose build --no-cache

test:
	docker-compose run --rm web py.test

migrate:
	docker-compose run --rm web python manage.py migrate

collectstatic:
	docker-compose run --rm web python manage.py collectstatic

startapp:
	docker-compose run --rm web python manage.py startapp $(name)

install:
	docker-compose run --rm web pipenv install $(package)

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
