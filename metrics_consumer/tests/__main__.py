import json
import unittest

from kafka import (
	KafkaProducer
)

from consumer.main import MetricsConsumer
from consumer.postgres import SystemMetrics
from settings import Settings


class TestMetricsConsumer(unittest.TestCase):

	def setUp(self):
		self.settings = Settings()
		self.test_producer = KafkaProducer(
			bootstrap_servers=self.settings.kafka_addr,
		)

	def producer_message(self):
		return {
			'hostname': 'localhost',
			'timestamp': '2019-12-09T14:37:02.751902+00:00',
			'memory_total': 1043996672,
			'memory_available': 59838464,
			'memory_free': 66850816,
			'memory_percent': 94.3
		}

	def send_message(self, msg):
		json_msg = json.dumps(msg)

		self.test_producer.send(
			self.settings.metrics_topic,
			json_msg.encode('utf-8'),
		)

		self.test_producer.flush()


	def test_initialization(self):
		init_success = False
		try:
			consumer = MetricsConsumer(self.settings)
			init_success = True
		except:
			self.assertTrue(False) # should never happen

		self.assertTrue(init_success)

	def test_consume(self):
		consumer = MetricsConsumer(self.settings)
		# drain the possible existing messages
		consumer.consume()

		# count of records in Postgres
		count_before = consumer.pg_connection.session.query(SystemMetrics).count()

		# produce a message to Kafka
		msg = self.producer_message()
		self.send_message(msg)

		# consume one new message
		consumer.consume()

		count_after = consumer.pg_connection.session.query(SystemMetrics).count()
		self.assertEqual(count_after - count_before, 1)

		metrics = consumer.pg_connection.session.query(SystemMetrics).filter_by(
			timestamp=msg['timestamp'],
		).first()

		self.assertTrue(metrics.memory_total, msg['memory_total'])
		self.assertTrue(metrics.memory_available, msg['memory_available'])
		self.assertTrue(metrics.memory_free, msg['memory_free'])
		self.assertTrue(metrics.memory_percent, msg['memory_percent'])

if __name__ == '__main__':
	unittest.main()
