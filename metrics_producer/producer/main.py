from datetime import (
	datetime, timezone,
)
import json
import socket

from kafka import KafkaProducer
import psutil
from twisted.internet import (
	task, reactor,
)

class MetricsProducer:
	"""
	Produces system metrics to Kafka
	"""

	def __init__(self, settings):
		if settings.kafka_security_protocol == 'SSL':
			self.kafka_producer = KafkaProducer(
				bootstrap_servers=settings.kafka_addr,
				security_protocol = settings.kafka_security_protocol,
				ssl_cafile = settings.kafka_cafile,
				ssl_certfile = settings.kafka_certfile,
				ssl_keyfile = settings.kafka_keyfile,
			)
		else:
			self.kafka_producer = KafkaProducer(
				bootstrap_servers=settings.kafka_addr,
			)

		self.metrics_topic = settings.metrics_topic
		self.metrics_interval = settings.metrics_interval

	def start(self):
		self.loop = task.LoopingCall(self.collect_and_publish_metrics)
		self.loop.start(self.metrics_interval)
		reactor.run()

	def collect_and_publish_metrics(self):
		msg = self.collect_metrics()
		self.publish_metrics(msg)

	def collect_metrics(self):
		mem = psutil.virtual_memory()
		return {
			'hostname': socket.gethostname(),
			'timestamp': datetime.now(timezone.utc).isoformat(),
			'memory_total': mem.total,
			'memory_available': mem.available,
			'memory_free': mem.free,
			'memory_percent': mem.percent,
		}

	def publish_metrics(self, msg):
		json_msg = json.dumps(msg)

		self.kafka_producer.send(
			self.metrics_topic,
			json_msg.encode('utf-8'),
		)

		self.kafka_producer.flush()
		print(f'Sent to Kafka: {msg}')
