from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select
from sqlmodel.pool import StaticPool
from organ.config import ENVIRONMENT, DB_URL
from organ.models import User


def get_engine(env=ENVIRONMENT):
  return create_engine(DB_URL, echo=True)

def get_user(username):
  with Session(engine) as session:
    return session.exec( select(User).where(User.username == username) ).first()

  """Return a SQLAlchemy engine for the given environment"""
  # if env == 'test':
  #   return create_engine(
  #     DB_URL,
      
  #   )
  # if env == 'development':
    # return create_engine(DB_URL, echo=True)

  # if env == 'production':
  #   return create_engine(
  #     DB_URL, connect_args={'check_same_thread': True}, echo=False
  #   )
  # raise Exception(f'Unknown environment: {env}')




# # Create database from SQLModel schema
# SQLModel.metadata.create_all(engine)


# TODO: implement async engine
# def create_async_engine():
#     from sqlmodel.ext.asyncio.session import AsyncEngine

#     return AsyncEngine(engine)

engine = get_engine()
