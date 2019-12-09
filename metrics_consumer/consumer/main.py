import json
from datetime import (
	datetime, timezone,
)

from kafka import KafkaConsumer

from .postgres import (
	Connection,
	SystemMetrics,
)

class MetricsConsumer:
	def __init__(self, settings):
		self.settings = settings
		self.kafka_consumer = KafkaConsumer(
			self.settings.metrics_topic,
			bootstrap_servers=self.settings.kafka_addr,
			client_id=self.settings.consumer_client_id,
			group_id=self.settings.consumer_group_id,
		)
		self.pg_connection = Connection(self.settings.postgres_addr)

	def start(self):
		self.kafka_consumer.poll()
		self.kafka_consumer.commit()
		while True:
			self.consume()

	def consume(self):
		raw_items = self.kafka_consumer.poll()
		for topic, raw_messages in raw_items.items():
			for raw_msg in raw_messages:
				metrics = json.loads(raw_msg.value.decode('utf-8'))
				self.save_to_postgres(metrics)
				print(f'Saved to Postgres: {metrics}')
		self.kafka_consumer.commit()

	def save_to_postgres(self, metrics):
		metrics = SystemMetrics(
			hostname=metrics.get('hostname'),
			timestamp=datetime.fromisoformat(metrics.get('timestamp')),
			memory_total=metrics.get('memory_total'),
			memory_available=metrics.get('memory_available'),
			memory_free=metrics.get('memory_free'),
			memory_percent=metrics.get('memory_percent'),
		)
		self.pg_connection.session.add(metrics)
		self.pg_connection.session.commit()
