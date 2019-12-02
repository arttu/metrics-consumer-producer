import os
import unittest

from .. import (
	ConfigurationException,
	Settings,
)

class TestSettings(unittest.TestCase):

	def test_success(self):
		settings = Settings()
		self.assertEqual(settings.kafka_addr, 'kafka:9092')
		self.assertEqual(settings.metrics_topic, 'SystemMetrics')

	def test_missing_environment_variable(self):
		orig_value = os.environ['KAFKA_ADDR']
		os.environ.pop('KAFKA_ADDR')

		with self.assertRaises(ConfigurationException):
			Settings()

		os.environ['KAFKA_ADDR'] = orig_value


if __name__ == '__main__':
	unittest.main()
