from sqlmodel import SQLModel, Session
from database import engine
from gem.model import *
from gem_properties.model import *

session = Session(bind=engine)

def create_db_and_tables():
    print ('creating database .....')
    SQLModel.metadata.create_all(engine)


def  main():
    create_db_and_tables()


if __name__ == "__main__":  # 
    main()