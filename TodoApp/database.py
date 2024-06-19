from sqlalchemy import create_engine

# sqlalchemy can only create new table for us, instead of enhancing tables. So sometimes we need to delete and recreate tables. 
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'    # create a location of databsae on fastAPI application
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:111111@localhost/TodoAppDatabase'

# In fastAPI, it's common database interact with different thread at the same time; it's telling sqlite that
# do not check different thread bc there could be multiple thread happening at sql database
from sqlalchemy.orm import sessionmaker
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) # "connect_args={'check_same_thread': False}" this part is for sqlite only
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# not let database do something automatically; bind it to our current engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a database object to interact later on
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


