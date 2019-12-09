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
		self.kafka_security_protocol = os.environ.get('KAFKA_SECURITY_PROTOCOL', 'None')
		self.kafka_cafile = os.environ.get('KAFKA_CAFILE')
		self.kafka_certfile = os.environ.get('KAFKA_CERTFILE')
		self.kafka_keyfile = os.environ.get('KAFKA_KEYFILE')
		self.metrics_topic = self.read_mandatory('METRICS_TOPIC')

		interval = os.environ.get('METRICS_INTERVAL_MS', None)
		if interval is not None:
			self.metrics_interval = float(interval) / 1000 # convert to seconds

		self.consumer_client_id = os.environ.get('METRICS_CLIENT_ID')
		self.consumer_group_id = os.environ.get('METRICS_GROUP_ID')

		self.postgres_addr = os.environ.get('POSTGRES_ADDR')

	@classmethod
	def read_mandatory(self, name):
		value = os.environ.get(name, None)
		if value is None:
			raise ConfigurationException(f'Missing a mandatory environment variable {name}')
		return value
