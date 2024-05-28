from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)
    size_field = Column(Integer, default=10)
    in_game = Column(Boolean, default=False)
    user_game_field = Column(LargeBinary)
    bot_game_field = Column(LargeBinary)
    # ship = relationship("Ship", back_populates="owner")


# class Ship(Base):
#     __tablename__ = 'ship'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     x = Column(Integer)
#     y = Column(Integer)
#     length = Column(Integer)
#     is_move = Column(Boolean, default=True)
#     cells = Column(String)
#     turn = Column(Boolean)
#     ship_cells = Column(String)
#     around_ship = Column(String)
#     size_field = Column(Integer)
#
#     owner_id = Column(Integer, ForeignKey('users.user_id'))
#     owner = relationship("User", back_populates="ship")
