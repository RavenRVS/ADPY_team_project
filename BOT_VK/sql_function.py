def connection("файл из переменного окружения"):
    pass
    # 1)     Инициализируются параметры. полученные на вход метода
    # 2)     создается подключение
    # 3)     ??? через try/except отлавливается ошибка подключения


def create_tables(connection):
    pass
    # создаются таблицы:
    # 1)     users
    # -       Id (из VK)
    # -       Имя
    # -       Возраст
    # -       Пол
    # -       Город
    # 2)     challengers
    # -       Id (из VK)
    # -       Имя
    # -       Фамилия
    # -       Ссылка на профиль
    # 3)     relation_lists
    # -       id_user (ссылка на users)
    # -   	Id_challenger (ссылка на challengers)
    # -   	Дата внесения записи
    # -       Наличие в избранном (логический тип)


def select_date_from_table(connection, table_name):
    pass
    # 1)     Получить данные из таблицы


def insert_user():
    pass
    # 1)   Загрузить данные в таблицу user


def check_user(id_user):
    pass
    # 1)     Проверить наличие пользователя в таблице users
    # 2) 	Возвращает true/false


def check_and_update_param_user(id_user):
    pass
    # 1)     Проверяет соответствие полей таблицы user и обновляет при несоответсвии


def insert_challenger():
    pass
    # 1)     Загрузить кандидата в таблицу


def check_challenger():
    pass
    # 1)     Проверить наличие кандидата в таблице


def insert_relation():
    pass
    # 1)     Загрузить отношение в таблицу


def check_relation():
    pass
    # 1)     Проверить наличие отношения в таблице


def get_last_challenger(id_user):
    pass
    # 1)     Получить информацию о последнем кандидате добавленного пользователем (id_user) из таблиц relation_list и challengers
    # 2)     Возвращается список с параметрами кандидата и true/false о наличие в списке избранных


def insert_challenger_in_favorite_list(id_user, id_challenger):
    pass
    #  1) 	Установить True в таблицу relation_lists для id_user и Id_challenger


def select_favorite_list(id_user):
    pass
    # 1)     Получить выборку записей из таблицы relation_list где столбец id_user = id_user и наличие в избранном = true
    # 2)     Возвращает список с вложенным списком параметров кандидатов
