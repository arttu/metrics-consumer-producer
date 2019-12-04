import json
import unittest

from kafka import (
	KafkaConsumer
)

from producer.main import MetricsProducer
from settings import Settings


class TestMetricsProducer(unittest.TestCase):

	def setUp(self):
		self.settings = Settings()
		self.test_consumer = KafkaConsumer(
			self.settings.metrics_topic,
			bootstrap_servers=self.settings.kafka_addr,
			client_id="test-metrics-consumer-1",
			group_id="test-metrics-group",
		)
		# make sure the consumer has partition assignments
		self.test_consumer.poll()
		# and all messages has been consumed
		self.test_consumer.poll()
		self.test_consumer.commit()

	def tearDown(self):
		self.test_consumer.commit()

	def test_initialization(self):
		try:
			producer = MetricsProducer(self.settings)
		except:
			self.assertFalse(True) # should never happen
		self.assertTrue(len(producer.metrics_topic) > 0)

	def test_writing_to_kafka(self):
		self.maxDiff = None
		assignment = self.test_consumer.assignment()
		partition = assignment.pop()

		# get the offset before publishing
		old_offset = self.test_consumer.position(partition)

		# produce a message
		producer = MetricsProducer(self.settings)
		msg = producer.collect_metrics()
		producer.publish_metrics(msg)

		raw_result = self.test_consumer.poll()
		for _, items in raw_result.items():
			self.assertEqual(len(items), 1)
			item = items.pop()
			# check that the consumed item is the same we published
			self.assertEqual(item.value.decode('utf-8'), json.dumps(msg))

		self.test_consumer.commit()

		# get the offset after consuming and check it's +1
		new_offset = self.test_consumer.position(partition)
		self.assertEqual(new_offset - old_offset, 1)

if __name__ == '__main__':
	unittest.main()
