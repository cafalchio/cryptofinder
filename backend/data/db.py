import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.app import Base

# engine = sqlalchemy.create_engine("mariadb+mariadbconnector://app_user:Password123!@127.0.0.1:3306/company")


class AllCoins(Base):
    # id,symbol,name,added
    __tablename__ = 'all_coins'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    symbol = sqlalchemy.Column(sqlalchemy.String(length=100))
    name = sqlalchemy.Column(sqlalchemy.String(length=100))
    added = sqlalchemy.Column(sqlalchemy.Date, default=True)
    is_shit = sqlalchemy.Column(sqlalchemy.Boolean(default=False))


class NewCoins(AllCoins):
    # id,symbol,name,added
    __tablename__ = 'new_coins'


class CoinsDetails(Base):
    __tablename__ = 'new_coins_details'
    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    symbol = sqlalchemy.Column(sqlalchemy.String(length=100))
    name = sqlalchemy.Column(sqlalchemy.String(length=100))
    added = sqlalchemy.Column(sqlalchemy.Date, default=True)
    description = sqlalchemy.Column(sqlalchemy.String(length=800))
    Homepage = sqlalchemy.Column(sqlalchemy.String(length=200))

    parent_id = sqlalchemy.Column(
        sqlalchemy.Integer, ForeignKey('new_coins.id'))
    new_coins = relationship(NewCoins, uselist=False)
