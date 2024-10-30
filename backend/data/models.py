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
    is_shit = Column(Boolean)
    new_coins = relationship("NewCoins", back_populates="all_coin")


class NewCoins(db.Model):
    __tablename__ = 'new_coins'

    id = Column(String, primary_key=True)
    symbol = Column(String(length=100))
    name = Column(String(length=100))
    added = Column(DateTime(timezone=True), server_default=func.now())
    is_shit = Column(Boolean)
    parent_id = Column(Integer, ForeignKey('all_coins.id'))
    all_coin = relationship(AllCoins, back_populates="new_coins")
    details = relationship("CoinsDetails", back_populates="new_coin")


class CoinsDetails(db.Model):
    __tablename__ = 'new_coins_details'

    id = Column(String, primary_key=True)
    symbol = Column(String(length=100))
    name = Column(String(length=100))
    added = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String(length=800))
    homepage = Column(String(length=200))
    parent_id = Column(Integer, ForeignKey('new_coins.id'))
    new_coin = relationship(NewCoins, back_populates="details")
