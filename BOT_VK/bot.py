import random

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from random import randrange

from datetime import datetime

from request_function import ReqVkApi
from db_for_bot import BaseForBot


class BotVK:
    def __init__(self, token_group, token_user, db_session, vk_api, id_user, text_message) -> [str, str, BaseForBot,
                                                                                               vk_api, int]:
        self.tkn_gr = token_group
        self.tkn_user = token_user
        self.session = db_session
        self.id_user = id_user
        self.text_message = text_message
        self.req = ReqVkApi(id_user, token_user)
        self.vk_api = vk_api
        self.keyboards = VkKeyboard(one_time=False)
        self.command = ['привет', 'найти пару', 'ищем дальше', 'в избранное', 'избранное', 'пока', 'завершить']
        # 1) 	 Токен сообщества
        # 2)     Команды (привет, найти пару, ищем дальше, в избранное, избранное, пока)
        # 3)     Подключение к БД
        # 4)     Стартовые параметры клавиатуры

    @staticmethod
    def get_param_for_searching(user_param):
        # 1)     Из параметров пользователя рассчитывает параметры для поиска кандидатов
        # 2)     # Если какой-либо из параметров не получен на вход (отсутствуют в профиле), то устанавливает значения
        #        # по умолчанию

        # return (возраст от, возраст до, пол противоположный пользователю, город).
        if len(user_param) > 5:
            if user_param[3] == 0:
                age_up_to = 40
                age_from = 20
            else:
                age_up_to = user_param[3]
                age_from = user_param[3] - 3

            if user_param[2] == 1:
                sex = 2
            elif user_param[2] == 2:
                sex = 1
            else:
                sex = 0

            if user_param[4] == 0 or None:
                city = 1
            else:
                city = user_param[4]

            list_param = [age_from, age_up_to, sex, city]

            return list_param
        else:
            # result_list = [i.user_id, i.name, i.age, i.sex, i.city]
            if user_param[2] == 0:
                age_up_to = 40
                age_from = 20
            else:
                age_up_to = user_param[2]
                age_from = user_param[2] - 3

            if user_param[3] == 1:
                sex = 2
            elif user_param[3] == 2:
                sex = 1
            else:
                sex = 0

            if user_param[4] == 0 or None:
                city = 1
            else:
                city = user_param[4]

            list_param = [age_from, age_up_to, sex, city]

            return list_param

    def send_message(self, vk_authoriz, text_message, keyboard=None):

        # 1)     Отправляет текстовое сообщение пользователю
        vk_authoriz.method('messages.send',
                           {'user_id': self.id_user,
                            'message': text_message,
                            'random_id': randrange(10 ** 7),
                            'keyboard': keyboard})

    def send_message_with_attachments(self, vk_authoriz, text_message, attachments):
        pass
        # 1)     Отправляет пользователю текстовое сообщение c вложением

        vk_authoriz.method(
            'messages.send', {
                'user_id': self.id_user,
                'message': text_message,
                'random_id': randrange(10 ** 7),
                'attachment': attachments
            }
        )

    def hi_command(self):
        # 1)     через метод get_info_about_user модуля request_function получаем имя, возраст, город,
        # пол пользователя
        # 2)     методом check_user модуля sql_function проверяем есть ли пользователь в БД,
        # если есть – проверяем актуальность имеющихся в базе данных (метод check_and_update_param_user модуля
        # SQL_function, если нет, то добавляем в базу через метод insert_user модуля sql_function данные в БД
        # 3)     активируем клавиатуру с кнопкой «найти пару»
        # 4)     Отправляем приветственное сообщение пользователю (метод send_message)

        user_params = self.req.get_info_about_user(self.id_user)
        if self.session.check_user(self.id_user):
            self.session.update_param_user(self.id_user, user_params)
        else:
            self.session.insert_user(self.id_user, user_params)

        begin = VkKeyboard(one_time=True)
        begin.add_button('Найти пару', VkKeyboardColor.PRIMARY)

        self.send_message(self.vk_api, f'Привет, {user_params[0]}!', begin.get_keyboard())

    def next_challenger_command(self):
        # 1)     методом get_user_from_base получаем из базы информацию о пользователе. Если нет в базе, то методом
        # get_info_about_user получаем данные о пользователе и записываем их в базу (insert_user)
        # 2)     методом get_param_for_searching определяем параметры для поиска подходящих пользователей (возраст от,
        # возраст до, противоположный пол, город)
        # 3)     Методом search_people модуля request_function получаем список ID подходящих пользователей
        # 4)     Через random выбираем из списка любого кандидата
        # 5)     Методом get_info_about_challenger модуля request_function получаем информацию о выбранном пользователе
        # 6)     Методом get_link_challenger модуля request_function получаем ссылку на страницу кандидата
        # 7)     Методами check_challenger и check_relation модуля SQL_function проверяем есть ли пользователь в
        # таблице просмотренных кандидатов, если нет, то методами insert_challenger и insert_relation модуля
        # SQL_function записываем данные в БД
        # 8)     Методом get_photo модуля request_function получаем до трех фото найденного кандидата
        # 9)     Методом send_message_with_attachments отправляем сообщение пользователю с информацией о
        # найденном кандидате

        global id_challenger
        user_param = self.session.get_user(self.id_user)
        if not user_param:
            user_param = self.req.get_info_about_user(self.id_user)
            self.session.insert_user(self.id_user, user_param)
        param_for_search = self.get_param_for_searching(user_param)
        people = self.req.search_people(param_for_search)
        challenger_in_base = True
        while challenger_in_base:
            id_challenger = random.choice(people)
            if self.session.check_relation(self.id_user, id_challenger):
                continue
            else:
                challenger_in_base = False
        info_about_challenger = self.req.get_info_about_user(id_challenger)
        if self.session.check_challenger(id_challenger):
            self.session.update_param_challenger(id_challenger, info_about_challenger)
        else:
            self.session.insert_challenger(id_challenger, info_about_challenger)
        self.session.insert_relation(self.id_user, id_challenger, datetime.now())
        photo = self.req.get_photo(id_challenger)
        if photo is None:
            self.send_message(self.vk_api, f'{info_about_challenger[0]} {info_about_challenger[1]}\n'
                                           f'https://vk.com/{info_about_challenger[5]}\n'
                                           f'Фото отсутствуют, либо закрыт доступ')
        else:
            self.send_message_with_attachments(self.vk_api,
                                               f'{info_about_challenger[0]} {info_about_challenger[1]}\n'
                                               f'https://vk.com/{info_about_challenger[5]}',
                                               photo)

    def begin_command(self):

        # 1)     Переключаем клавиатуру на три кнопки («ищем дальше», «В избранное», «Избранное»)
        # 2)     Выполняем метод next_challenger

        self.keyboards.add_button('Завершить', VkKeyboardColor.SECONDARY)
        self.keyboards.add_button('Ищем дальше', VkKeyboardColor.POSITIVE)
        self.keyboards.add_line()
        self.keyboards.add_button('Избранное', VkKeyboardColor.SECONDARY)
        self.keyboards.add_button('В избранное', VkKeyboardColor.PRIMARY)

        self.send_message(self.vk_api, 'Запускаем поиск...', self.keyboards.get_keyboard())

        self.next_challenger_command()

    def set_in_favorite_list_command(self):

        # 1)     Методом get_last_challenger модуля SQL_function получаем последнего выведенного на просмотр кандидата
        # 2)     Если кандидат уже в списке избранных, то методом send_massege отправляем пользователю сообщение
        # «кандидат уже в списке избранных»
        # 3)     Иначе, методом insert_challenger_in_favorite_list модуля SQL_function записываем пользователя в
        # таблицу в БД
        # 4)     Получаем информацию о кандидате
        # 5)     Методом send_message отправляем сообщение пользователю об успешной записи кандидата в список избранных

        id_challenger = self.session.get_last_challenger(self.id_user)
        if self.session.check_challenger_in_favorite_list(self.id_user, id_challenger[0]):
            self.send_message(self.vk_api, 'Последний найденный кандидат уже в списке избранных')
        else:
            self.session.insert_challenger_in_favorite_list(self.id_user, id_challenger[0])
            # info_about_challenger = self.req.get_info_about_user(id_challenger[0])
            self.send_message(self.vk_api, f'Пользователь {id_challenger[1]} '
                                           f'{id_challenger[2]} добавлен в список избранных')

    def get_favorite_list_command(self):

        # 1) 	Методом select_favorite_list в модуле SQL_function получаем список избранных
        # 2)     Если список пуст, то методом send_message отправляем «Ваш список избранных пуст»
        # 3)     Иначе через цикл for:
        # a)      Получаем id, имя и ссылку на профиль
        # b)     Через метод get_photo модуля request_function получаем до трех фото кандидата
        # c)      Методом send_message_with_attachments отправляем сообщение пользователю с информацией о кандидате
        # из списка избранных

        favorite_list = self.session.get_favorite_list(self.id_user)
        if favorite_list is None:
            self.send_message(self.vk_api, f'Ваш список избранных пуст')
        else:
            for challenger in favorite_list:
                photo = self.req.get_photo(challenger[0])

                self.send_message_with_attachments(self.vk_api,
                                                   f'{challenger[1]} {challenger[2]}\n'
                                                   f'https://vk.com/{challenger[3]}',
                                                   photo)

    def bye_command(self):

        # 1)     Методом send_message отправляем прощальное сообщение пользователю
        self.keyboards.add_button('Найти пару', VkKeyboardColor.PRIMARY)
        self.send_message(self.vk_api, f'Пока, пока :)', self.keyboards.get_keyboard())

    def action(self):

        # 1)     Через условный оператор производим сверку текста сообщения с командами из списка команд
        # 2)     При найденном соответствии запускается соответствующий метод
        # 3)     При отсутствии соответствия методом send_message пользователю отправляется сообщение о нераспознанной
        # команде, с рекомендациями воспользоваться кнопками или прочитать инструкцию

        if self.text_message == self.command[0]:
            self.hi_command()
        elif self.text_message == self.command[1]:
            self.begin_command()
        elif self.text_message == self.command[2]:
            self.next_challenger_command()
        elif self.text_message == self.command[3]:
            self.set_in_favorite_list_command()
        elif self.text_message == self.command[4]:
            self.get_favorite_list_command()
        elif self.text_message == self.command[5] or self.text_message == self.command[6]:
            self.bye_command()
        else:
            self.send_message(self.vk_api, f'Неизвестная команда!\nВоспользуйтей кнопками ниже или '
                                           f'отправьте команду "Найти пару"')
