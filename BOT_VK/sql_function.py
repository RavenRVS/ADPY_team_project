import sqlalchemy as sq
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Users:
    __tablename__ = "users"
    # объявление таблицы users
    # - Id (из VK)
    # - Имя
    # - Возраст
    # - Пол
    # - Город


class Сhallengers:
    __tablename__ = "challengers"
    # объявление таблицы challengers
    # - Id (из VK)
    # - Имя
    # -  Фамилия
    # - Ссылка на профиль


class RelationList:
    __tablename__ = "relation_lists"
    # объявление таблицы relation_lists
    # - id_user (ссылка на users)
    # - Id_challenger (ссылка на challengers)
    # - Дата внесения записи
    # - Наличие в избранном (логический тип)
    # - Наличие в черном списке


def create_tables(engine):
    pass
    # создаются все таблицы

    # return True/False


def connect(localhost, user, pwd):
    pass
    # Создет новое соединение

    # return экземпляр класса Session


def select_date_from_table(connect, table_name):
    pass
    # Получает данные из таблицы table_name

    # return список


def insert_user(id_user, name_user, sex_user, age_user, city_user):
    pass
    # Загружает данные в таблицу user

    # return True/False


def check_user(id_user):
    pass
    # Проверяет наличие пользователя в таблице users

    # return True/False


def check_and_update_param_user(id_user, name_user, sex_user, age_user, city_user):
    pass
    # Проверяет соответствие информации о пользователе в таблице users, полученным на вход. Обновляет данные в таблице
    # при несоответсвии

    # return [id_user, name_user, sex_user, age_user, city_user]


def insert_challenger(id_challenger, name_challenger, surname_challenger, link):
    pass
    # Загружает информацию о кандидате в таблицу challengers

    # return True/False


def check_challenger(id_challenger):
    pass
    # Проверяет наличие кандидата в таблице challenger

    # return True/False


def check_and_update_param_challenger(id_challenger, name_challenger, surname_challenger, link):
    pass
    # Проверяет соответствие информации о пользователе в таблице users, полученным на вход. Обновляет данные в таблице
    # при несоответсвии

    # return [id_challenger, name_challenger, surname_challenger, link]


def insert_relation(id_user, id_challenger, recording_date, favorite_list=False, black_list=False):
    pass
    # Загружает данные в таблицу relation_lists

    # return True/False


def check_relation(id_user, id_challenger):
    pass
    # По id_user, id_challenger проверяет наличие записи в таблице relation_lists

    # return True/False


def get_last_challenger(id_user):
    pass
    # Получает информацию о последнем кандидате добавленным пользователем(id_user) из таблиц relation_list и challengers

    # return [id_challenger, name_challenger, surname_challenger, link, favorite_list, black_list]


def insert_challenger_in_favorite_list(id_user, id_challenger):
    pass
    #  Устанавливает True в таблице relation_lists для строки с комибинацией id_user и id_challenger

    # return True/False


def select_favorite_list(id_user):
    pass
    # Получвет выборку записей из таблицы relation_list где столбец id_user = id_user и наличие  favorite_list = true

    # return список с вложенным списком [[id_challenger, name_challenger, surname_challenger, link],[...]] список
    # отсортирован по дате внесения пользователей в лист избранных
