from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import random

from datetime import datetime


class BotVK:
    def __init__(self, group_token, sql_connect, user_id):
        self.token = group_token
        self.command = ['привет', 'найти пару', 'ищем дальше', 'в избранное', 'избранное', 'пока']
        self.connect = sql_connect
        self.user_id = user_id

        keyboards = VkKeyboard(one_time=False)
        begin = VkKeyboard(one_time=True)
        begin.add_button('найти пару', VkKeyboardColor.PRIMARY)

    def get_param_for_searching(self, age_user, sex_user, city_user):
        if sex_user > 3:
            age_up_to = age_user + 3
            age_from = age_user - 3
        else:
            age_up_to = 50
            age_from = 19
        if sex_user == 1:
            sex = 2
        else:
            sex = 1
        city = city_user
        param_for_search = [age_from, age_up_to, sex, city]
        return param_for_search
        # 1)     Из параметров пользователя рассчитывает параметры для поиска кандидатов
        # 2)     # Если какой-либо из параметров не получен на вход (отсутствуют в профиле), то устанавливает значения
        #        # по умолчанию

        # return (возраст от, возраст до, пол противоположный пользователю, город).

    def send_massage(self, id_пользователя, токен_сообщества, текст, параметр_клавиатуры):
        pass
        # 1)     Отправляет текстовое сообщение пользователю

    def send_message_with_attachments(self, id_пользователя, токен_сообщества, текст, параметр_клавиатуры, вложение):
        pass
        # 1)     Отправляет пользователю текстовое сообщение c вложением

    def hi_command(self):
        pass
        # 1)     через метод get_info_about_user модуля request_function получаем имя, возраст, город,
        # пол пользователя
        # 2)     методом check_user проверяем модуля sql_function есть ли пользователь в БД,
        # если нет, то добавляем в базу (через метод insert_user модуля sql_function записываем данные в БД),
        # если есть – проверяем актуальность имеющихся в базе данных (метод check_and_update_param_user модуля
        # SQL_function)
        # 3)     активируем клавиатуру с кнопкой «найти пару»
        # 4)     Отправляем приветственное сообщение пользователю (метод send_message)

    def next_challenger(self):
        pass
        # 1)     Методом get_param_for_searching определяем параметры для поиска подходящих пользователей (возраст от,
        # возраст до, противоположный пол, город)
        # 2)     Методом search_people модуля request_function получаем список ID подходящих пользователей
        # 3)     Через random выбираем из списка любого кандидата
        # 4)     Методом get_info_about_challenger модуля request_function получаем информацию о выбранном пользователе
        # 5)     Методом get_link_challenger модуля request_function получаем ссылку на страницу кандидата
        # 6)     Методами check_challenger и check_relation модуля SQL_function проверяем есть ли пользователь в
        # таблице просмотренных кандидатов, если нет, то методами insert_challenger и insert_relation модуля
        # SQL_function записываем данные в БД
        # 7)     Методом get_photo модуля request_function получаем до трех фото найденного кандидата
        # 8)     Методом send_message_with_attachments отправляем сообщение пользователю с информацией о
        # найденном кандидате

    def begin_command(self):
        pass
        # 1)     Переключаем клавиатуру на три кнопки («ищем дальше», «В избранное», «Избранное»)
        # 2)     Выполняем метод next_challenger

    def set_in_favorite_list_command(self):
        pass
        # 1)     Методом get_last_challenger модуля SQL_function получаем последнего выведенного на просмотр кандидата
        # 2)     Если кандидат уже в списке избранных, то методом send_massege отправляем пользователю сообщение
        # «кандидат уже в списке избранных»
        # 3)     Иначе, методом insert_challenger_in_favorite_list модуля SQL_function записываем пользователя в
        # таблицу в БД
        # 4)     Методом send_message отправляем сообщение пользователю об успешной записи кандидата в список избранных

    def get_favorite_list_command(self):
        pass
        # 1) 	Методом select_favorite_list в модуле SQL_function получаем список избранных
        # 2)     Если список пуст, то методом send_message отправляем «Ваш список избранных пуст»
        # 3)     Иначе через цикл for:
        # a)      Получаем id, имя и ссылку на профиль
        # b)     Через метод get_photo модуля request_function получаем до трех фото кандидата
        # c)      Методом send_message_with_attachments отправляем сообщение пользователю с информацией о кандидате
        # из списка избранных

    def bye_command(self):
        pass
        # 1)     Методом send_message отправляем прощальное сообщение пользователю

    def action(self, текст_сообщения):
        pass
        # 1)     Через условный оператор производим сверку текста сообщения с командами из списка команд
        # 2)     При найденном соответствии запускается соответствующий метод
        # 3)     При отсутствии соответствия методом send_massege пользователю отправляется сообщение о нераспознанной
        # команде, с рекомендациями воспользоваться кнопками или прочитать инструкцию
