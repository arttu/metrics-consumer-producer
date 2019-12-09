## Usage

Start consumer and producer in separate shell sessions

	docker-compose run --rm consumer

	docker-compose run --rm producer

Inspect the records in Postgres

	# find out the Postgres container ID and replace below
	docker exec -it "Pg container ID" psql postgres://test:test@postgres:5432/metrics

## Using with aiven.io services

- Signup at https://console.aiven.io/signup.html
- Setup new Kafka and create topic "SystemMetrics"
  - Download save the following SSL files:
    - "Access Key" -> "./ssl_files/aiven.key"
    - "Access Certificate" -> "./ssl_files/aiven.crt"
    - "CA Certificate" -> "./ssl_files/aiven_ca.pem"
- Setup new Postgres and create database "metrics"
- Change the two occurrences of `KAFKA_SECURITY_PROTOCOL=None` in `docker-compose.yml` to `KAFKA_SECURITY_PROTOCOL=SSL`
- Change Kafka and Postgres connection URLs to ones you have in aiven.io console
