import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    user_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String)
    age = sq.Column(sq.Integer)
    sex = sq.Column(sq.Integer)
    city = sq.Column(sq.Integer)
    relationlist = relationship('RelationList', back_populates='user')


class Challengers(Base):
    __tablename__ = "challengers"
    challenger_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String)
    surname = sq.Column(sq.String)
    domain = sq.Column(sq.String)
    relationlist = relationship('RelationList', back_populates='challenger')


class RelationList(Base):
    __tablename__ = "relation_lists"
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'), nullable=False, primary_key=True)
    user = relationship('Users', back_populates='relationlist')
    challenger_id = sq.Column(sq.Integer, sq.ForeignKey('challengers.challenger_id'), nullable=False,
                               primary_key=True)
    challenger = relationship('Challengers', back_populates='relationlist')
    date_added = sq.Column(sq.DateTime, nullable=False)
    favorite_list = sq.Column(sq.Boolean, nullable=False)
    black_list = sq.Column(sq.Boolean, nullable=False)


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
