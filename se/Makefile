# Работа через Docker

build:
	docker compose pull --ignore-buildable
	docker compose build

run:
	docker compose up -d

stop:
	docker compose down -v

lint:
	docker compose run -T --rm linters flake8 /src/

lint_file:
	cat $1 | docker compose run -T --rm linters flake8 -

pytest:
	docker compose run --rm django pytest ./ .contrib-candidates/

makemigrations:
	docker compose run --rm django ./manage.py makemigrations

migrate:
	docker compose run --rm django ./manage.py migrate

first_start:
	make build migrate
	docker compose run --rm django ./manage.py createsuperuser --no-input
