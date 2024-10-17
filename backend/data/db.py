import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://app_user:Password123!@127.0.0.1:3306/company")

Base = declarative_base()

#
# class AllCoins(Base):
#     # id,symbol,name,added
#     __tablename__ = 'all_coins'
#
#     id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
#     symbol = sqlalchemy.Column(sqlalchemy.String(length=100))
#     name = sqlalchemy.Column(sqlalchemy.String(length=100))
#     added = sqlalchemy.Column(sqlalchemy.Date, default=True)
#
#
# class NewCoins(AllCoins):
#     # id,symbol,name,added
#     __tablename__ = 'new_coins'
#
#     id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
#     symbol = sqlalchemy.Column(sqlalchemy.String(length=100))
#     name = sqlalchemy.Column(sqlalchemy.String(length=100))
#     added = sqlalchemy.Column(sqlalchemy.Date, default=True)
#
#
# class NewCoinsDetails(Base):
#     # id,Symbol,Name,Categories,Description,Homepage,White paper,Blockchain site,contract_address,added
#     __tablename__ = 'new_coins_details'
#     id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
#     symbol = sqlalchemy.Column(sqlalchemy.String(length=100))
#     name = sqlalchemy.Column(sqlalchemy.String(length=100))
#     added = sqlalchemy.Column(sqlalchemy.Date, default=True)
#     categories = sqlalchemy.Column(sqlalchemy.String(length=200))
#     description = sqlalchemy.Column(sqlalchemy.String(length=800))
#     Homepage = sqlalchemy.Column(sqlalchemy.String(length=200))
#     white_paper = sqlalchemy.Column(sqlalchemy.String(length=200))
#     blockchain = sqlalchemy.Column(sqlalchemy.String(length=100))
#     site = sqlalchemy.Column(sqlalchemy.String(length=200))
#     contract_address = sqlalchemy.Column(sqlalchemy.String(length=100))
#
#     parent_id = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('new_coins.id'))
#     new_coins = relationship(NewCoins, uselist=False)