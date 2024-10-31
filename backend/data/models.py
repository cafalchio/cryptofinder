from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.app import db


class AllCoins(db.Model):
    __tablename__ = 'all_coins'

    id = Column(String, primary_key=True)
    symbol = Column(String(length=100))
    name = Column(String(length=100))
    added = Column(DateTime(timezone=True), server_default=func.now())
    source = Column(String(length=100))
    is_shit = Column(Boolean)


class CoinsDetails(db.Model):
    __tablename__ = 'coins_details'

    id = Column(String, primary_key=True)
    symbol = Column(String(length=100))
    name = Column(String(length=100))
    added = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String(length=800))
    homepage = Column(String(length=200))
    parent_id = Column(Integer, ForeignKey('new_coins.id'))
