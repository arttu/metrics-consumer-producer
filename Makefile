
tests:
	docker-compose run --rm producer python -m settings.tests.settings
	docker-compose run --rm producer python -m tests
	docker-compose run --rm consumer python -m tests

.PHONY: tests
