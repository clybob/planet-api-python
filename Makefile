setup:
	@docker-compose build

run:
	@docker-compose run -e SERVER_NAME=localhost:5000 -e FLASK_ENV=development --service-ports web bash -c "flask create-db && flask run --host 0.0.0.0"

test:
	@docker-compose run -e SERVER_NAME=localhost:5000 -e FLASK_ENV=development web bash -c "flask create-db && python -m unittest discover -s api"

