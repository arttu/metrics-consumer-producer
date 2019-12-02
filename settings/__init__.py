import os

class ConfigurationException(Exception):
	"""Exception to be raised if there are configuration errors."""
	pass


class Settings:
	"""
	Common settings for producer and consumer.
	Reads from environment variables on initialization.
	"""

	def __init__(self):
		self.kafka_addr = self.read_mandatory('KAFKA_ADDR')
		self.metrics_topic = self.read_mandatory('METRICS_TOPIC')

	@classmethod
	def read_mandatory(self, name):
		value = os.environ.get(name, None)
		if value is None:
			raise ConfigurationException(f'Missing a mandatory environment variable {name}')
		return value
