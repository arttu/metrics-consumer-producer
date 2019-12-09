from settings import Settings
from consumer.main import MetricsConsumer

if __name__ == "__main__":
	print('Starting the consumer')
	settings = None
	try:
		settings = Settings()
	except Exception as e:
		print(f'Encountered an error while reading settings: {e}')

	consumer = MetricsConsumer(settings)
	consumer.start()
