
tests:
	docker-compose run --rm producer python -m settings.tests.settings

.PHONY: tests
