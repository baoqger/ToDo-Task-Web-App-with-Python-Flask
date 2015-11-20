from sqlalchemy import Column, ForeignKey, Integer, String, DateTime,func
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship 
from sqlalchemy import create_engine

Base = declarative_base()

class ToDoTask(Base):
	__tablename__ = 'todotask'
	content = Column(String(250), nullable = False)
	id = Column(Integer, primary_key = True)
	priority = Column(Integer)
	#create_time = Column(DateTime, default=func.now())
	status = Column(String(8))
	
engine = create_engine('sqlite:///todotask.db')
Base.metadata.create_all(engine)
