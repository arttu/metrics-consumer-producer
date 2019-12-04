
tests:
	docker-compose run --rm producer python -m settings.tests.settings
	docker-compose run --rm producer python -m tests

.PHONY: tests
