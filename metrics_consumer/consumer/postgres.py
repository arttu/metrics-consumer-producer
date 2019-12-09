from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *


Base = declarative_base()


class SystemMetrics(Base):
	__tablename__ = 'system_metrics'

	id = Column(Integer, Sequence('system_metrics_id_seq'), primary_key=True)
	hostname = Column(String(255), nullable=False)
	timestamp = Column(DateTime, nullable=False)
	memory_total = Column(Integer)
	memory_available = Column(Integer)
	memory_free = Column(Integer)
	memory_percent = Column(Float)


class Connection:

	def __init__(self, postgres_addr):
		self.pg_engine = create_engine(postgres_addr)
		Session = sessionmaker(bind=self.pg_engine)
		self.session = Session()

		# create table if it doesn't exist yet
		Base.metadata.create_all(bind=self.pg_engine, checkfirst=True)
