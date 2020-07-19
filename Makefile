setup:
	@docker-compose build

run:
	@docker-compose up web

test:
	@docker-compose run test

