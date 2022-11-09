import sqlalchemy as sq
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from BOT_VK.db_models import create_tables, Users, Challengers, RelationList


class BaseForBot:
    def __init__(self, base_type, user_name, password, base_name, host='localhost', port=5432):
        self.base_type = base_type
        self.user_name = user_name
        self.pwd = password
        self.host = host
        self.port = port
        self.base_name = base_name

        self.dsn = f"{self.base_type}://{self.user_name}:{self.pwd}@{self.host}:{self.port}/{self.base_name}"
        self.engine = sq.create_engine(self.dsn)
        create_tables(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def insert_user(self, id_user, user_params):
        # Загружает данные в таблицу user
        # возвращает True/False
        # user_params = [name_user, surname_user, sex_user, age_user, city_user, domain]
        try:
            str = Users(user_id=id_user, name=user_params[0], age=user_params[3], sex=user_params[2],
                        city=user_params[4])
            print(str)
            self.session.add(str)
            self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            return {'error': 'error'}
        return True

    def get_user(self, id_user):
        # возвращает информацию о пользователе по id
        query = self.session.query(Users).filter(Users.user_id == id_user).limit(1)
        result_list = []
        for i in query:
            result_list = [i.user_id, i.name, i.age, i.sex, i.city]
        return result_list

    def check_user(self, id_user):
        # Проверяет наличие пользователя в таблице users
        # возвращает True/False
        query = self.session.query(Users).filter(Users.user_id == id_user).all()
        result = []
        for i in query:
            result.append(i.user_id)
        if len(result) > 0:
            return True
        else:
            return False

    def update_param_user(self, id_user, user_params):
        # user_params = [name_user, surname_user, sex_user, age_user, city_user, domain]
        # Проверяет соответствие информации о пользователе в таблице users, полученным на вход.
        # Обновляет данные в таблице при несоответсвии
        # Возвращает True/False

        try:
            self.session.query(Users).filter(Users.user_id == id_user).update({Users.name: user_params[0],
                                                                               Users.age: user_params[3],
                                                                               Users.sex: user_params[2],
                                                                               Users.city: user_params[4]},
                                                                              synchronize_session=False)

            self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            return {'error': 'error'}
        return True

    def insert_challenger(self, id_challenger, challenger_params):
        # challenger_params = [name_user, surname_user, sex_user, age_user, city_user, domain]
        # Загружает информацию о кандидате в таблицу challengers
        # возвращет True/False
        try:
            str = Challengers(challenger_id=id_challenger, name=challenger_params[0], surname=challenger_params[1],
                              domain=challenger_params[5])
            self.session.add(str)
            self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            return {'error': 'error'}
        return True

    def check_challenger(self, id_challenger):

        # Проверяет наличие кандидата в таблице challenger
        # возвращает True/False

        query = self.session.query(Challengers).filter(Challengers.challenger_id == id_challenger).all()

        result = []
        for i in query:
            result.append(i.challenger_id)
        if len(result) > 0:
            return True
        else:
            return False

    def update_param_challenger(self, id_challenger, challenger_params):

        # challenger_params = [name_user, surname_user, sex_user, age_user, city_user, domain]
        # Обновляет данные в таблице Challengers для строки с id_challenger

        # возвращет True или код ошибки

        try:
            self.session.query(Challengers).filter(Challengers.challenger_id == id_challenger).update({
                Challengers.name: challenger_params[0],
                Challengers.surname: challenger_params[1],
                Challengers.domain: challenger_params[5]},
                synchronize_session=False)
            self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            return {'error': 'error'}
        return True

    def insert_relation(self, id_user, id_challenger, recording_date, favorite_list=False, black_list=False):

        # Загружает данные в таблицу relation_lists
        # Возвращает True/False

        try:
            str = RelationList(user_id=id_user,
                               challenger_id=id_challenger,
                               date_added=recording_date,
                               favorite_list=favorite_list,
                               black_list=black_list
                               )
            self.session.add(str)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            return {'error': 'error'}
        return True

    def check_relation(self, id_user, id_challenger):
        pass
        # По id_user, id_challenger проверяет наличие записи в таблице relation_lists
        # возвращает True/False

        query = self.session.query(RelationList).filter((RelationList.user_id == id_user) &
                                                        (RelationList.challenger_id == id_challenger))
        result = []
        for i in query:
            result.append(i.user_id)
        if len(result) > 0:
            return True
        else:
            return False

    def check_challenger_in_favorite_list(self, id_user, id_challenger):

        query = self.session.query(RelationList).filter((RelationList.user_id == id_user) &
                                                        (RelationList.challenger_id == id_challenger) &
                                                        (RelationList.favorite_list == True)).all()
        result = []
        for i in query:
            result.append(i.challenger_id)
        if len(result) > 0:
            return True
        else:
            return False

    def get_last_challenger(self, id_user):

        # Получает информацию о последнем кандидате добавленным пользователем(id_user) из таблиц relation_list
        # и challengers
        # Возвращает список [id_challenger, name_challenger, surname_challenger, domain, favorite_list, black_list]

        subquery = self.session.query(RelationList).filter(RelationList.user_id == id_user).order_by(
            RelationList.date_added.desc()).limit(1).subquery()
        query = self.session.query(Challengers).join(subquery, Challengers.challenger_id == subquery.c.challenger_id)
        result_list = []
        for i in query:
            result_list = [i.challenger_id, i.name, i.surname, i.domain]
        return result_list

    def insert_challenger_in_favorite_list(self, id_user, id_challenger):

        #  Устанавливает True в таблице relation_lists для строки с комибинацией id_user и id_challenger
        #  возвращает True/False

        try:
            self.session.query(RelationList).filter((RelationList.user_id == id_user) &
                                                    (RelationList.challenger_id == id_challenger)).update({
                RelationList.favorite_list: True}, synchronize_session=False)
            self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            return {'error': 'error'}
        return True

    def get_favorite_list(self, id_user):
        pass
        # Получвет выборку записей из таблицы relation_list где столбец id_user = id_user и
        # наличие  favorite_list = true
        # return список с вложенным списком [[id_challenger, name_challenger, surname_challenger, link],[...]]

        subquery = self.session.query(RelationList).filter((RelationList.user_id == id_user) &
                                                        (RelationList.favorite_list == True)).order_by(
            RelationList.date_added.desc()).subquery()
        query = self.session.query(Challengers).join(subquery,
                                                     Challengers.challenger_id == subquery.c.challenger_id).all()

        result_list = []
        for i in query:
            subresult_list = [i.challenger_id, i.name, i.surname, i.domain]
            result_list.append(subresult_list)
        return result_list
