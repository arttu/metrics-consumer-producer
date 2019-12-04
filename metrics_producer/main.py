from settings import Settings
from producer.main import MetricsProducer

if __name__ == "__main__":
	print('Starting the producer')
	settings = None
	try:
		settings = Settings()
	except Exception as e:
		print(f'Encountered an error while reading settings: {e}')

	producer = MetricsProducer(settings)
	producer.start()
