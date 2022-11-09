import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    # - Id (из VK)
    user_id = sq.Column(sq.Integer, primary_key=True)
    # - Имя
    name = sq.Column(sq.String)
    # - Возраст
    age = sq.Column(sq.Integer)
    # - Пол
    sex = sq.Column(sq.Integer)
    # - Город
    city = sq.Column(sq.Integer)
    relationlist = relationship('RelationList', back_populates='user')


class Challengers(Base):
    # объявление таблицы challengers
    __tablename__ = "challengers"
    # - Id (из VK)
    challenger_id = sq.Column(sq.Integer, primary_key=True)
    # - Имя
    name = sq.Column(sq.String)
    # -  Фамилия
    surname = sq.Column(sq.String)
    # - Ссылка на профиль
    domain = sq.Column(sq.String)
    relationlist = relationship('RelationList', back_populates='challenger')


class RelationList(Base):
    __tablename__ = "relation_lists"  # объявление таблицы relation_lists
    # - id_user (ссылка на users)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('users.user_id'), nullable=False, primary_key=True)
    user = relationship('Users', back_populates='relationlist')
    # - Id_challenger (ссылка на challengers)
    challenger_id = sq.Column(sq.Integer, sq.ForeignKey('challengers.challenger_id'), nullable=False,
                               primary_key=True)
    challenger = relationship('Challengers', back_populates='relationlist')
    # - Дата внесения записи
    date_added = sq.Column(sq.DateTime, nullable=False)
    # - Наличие в избранном
    favorite_list = sq.Column(sq.Boolean, nullable=False)
    # - Наличие в черном списке
    black_list = sq.Column(sq.Boolean, nullable=False)


def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
