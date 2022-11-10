import random
from datetime import datetime
from random import randrange

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from db_for_bot import BaseForBot
from requests_to_vk import ReqVkApi


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

    @staticmethod
    def get_param_for_searching(user_param):
        # Из параметров пользователя рассчитывает параметры для поиска кандидатов. Если какой-либо из
        # параметров не получен на вход (отсутствуют в профиле), то устанавливает значения по умолчанию
        # Принимает на вход список либо список [name_user, surname_user, sex_user, age_user, city_user, domain],
        # либо список [user_id, name, age, sex, city]
        # возвращает список [возраст от, возраст до, пол противоположный пользователю, город]
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
        # Отправляет текстовое сообщение пользователю
        vk_authoriz.method('messages.send',
                           {'user_id': self.id_user,
                            'message': text_message,
                            'random_id': randrange(10 ** 7),
                            'keyboard': keyboard})

    def send_message_with_attachments(self, vk_authoriz, text_message, attachments):
        # Отправляет пользователю текстовое сообщение c вложением

        vk_authoriz.method(
            'messages.send', {
                'user_id': self.id_user,
                'message': text_message,
                'random_id': randrange(10 ** 7),
                'attachment': attachments
            }
        )

    def hi_command(self):
        # 1)     через метод get_info_about_user модуля requests_to_vk получает парамтеры пользователя
        # 2)     методом check_user модуля db_for_bot проверяет есть ли пользователь в БД,
        # если есть – проверяет актуальность имеющихся в базе данных (метод update_param_user модуля db_for_bot
        # если нет, то добавляет данные в базу через метод insert_user модуля db_for_bot
        # 3)     активирует клавиатуру с кнопкой «найти пару»
        # 4)     отправляет приветственное сообщение пользователю (метод send_message)

        user_params = self.req.get_info_about_user(self.id_user)
        if self.session.check_user(self.id_user):
            self.session.update_param_user(self.id_user, user_params)
        else:
            self.session.insert_user(self.id_user, user_params)

        begin = VkKeyboard(one_time=True)
        begin.add_button('Найти пару', VkKeyboardColor.PRIMARY)

        self.send_message(self.vk_api, f'Привет, {user_params[0]}!', begin.get_keyboard())

    def next_challenger_command(self):
        # 1)     методом get_user_from_base получает из базы информацию о пользователе. Если нет в базе, то методом
        # get_info_about_user получает данные о пользователе и записывает их в базу (insert_user)
        # 2)     методом get_param_for_searching определяет параметры для поиска подходящих пользователей (возраст от,
        # возраст до, противоположный пол, город)
        # 3)     методом search_people модуля request_to_vk получает список ID подходящих пользователей
        # 4)     через random выбирает из списка любого кандидата
        # 5)     методам check_relation проверяет, есть ли пользователь в таблице просмотренных кандидатов, если нет,
        # то методами insert_challenger и insert_relation модуля записываем данные в БД
        # 6)     методом get_info_about_challenger получает информацию о выбранном пользователе
        # 7)     методом get_photo получает до трех фото найденного кандидата
        # 8)     если фото нет, то методом send_message отправляет информацию о найденном пользователе без фото
        # 9)     если фото есть, то методом send_message_with_attachments отправляет сообщение пользователю с
        # информацией о найденном кандидате и фото

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
        # 1)     Переключает клавиатуру на четыре кнопки («Завершить», «Ищем дальше», «В избранное», «Избранное»)
        # 2)     Методом send_message отправляет сообщение о начале поиска
        # 3)     Выполняет метод next_challenger

        self.keyboards.add_button('Завершить', VkKeyboardColor.SECONDARY)
        self.keyboards.add_button('Ищем дальше', VkKeyboardColor.POSITIVE)
        self.keyboards.add_line()
        self.keyboards.add_button('Избранное', VkKeyboardColor.SECONDARY)
        self.keyboards.add_button('В избранное', VkKeyboardColor.PRIMARY)

        self.send_message(self.vk_api, 'Запускаем поиск...', self.keyboards.get_keyboard())

        self.next_challenger_command()

    def set_in_favorite_list_command(self):
        # 1)     Методом get_last_challenger получает последнего выведенного на просмотр кандидата
        # 2)     Если кандидат уже в списке избранных, то методом send_massage отправляет пользователю сообщение
        # «кандидат уже в списке избранных»
        # 3)     Иначе, методом insert_challenger_in_favorite_list записывает пользователя в таблицу в БД
        # 4)     Методом send_message отправляет сообщение пользователю об успешной записи кандидата в список избранных

        id_challenger = self.session.get_last_challenger(self.id_user)
        if self.session.check_challenger_in_favorite_list(self.id_user, id_challenger[0]):
            self.send_message(self.vk_api, 'Последний найденный кандидат уже в списке избранных')
        else:
            self.session.insert_challenger_in_favorite_list(self.id_user, id_challenger[0])
            self.send_message(self.vk_api, f'Пользователь {id_challenger[1]} '
                                           f'{id_challenger[2]} добавлен в список избранных')

    def get_favorite_list_command(self):
        # 1) 	Методом select_favorite_list получает список избранных
        # 2)    Если список пуст, то методом send_message отправляет пользователю сообщение «Ваш список избранных пуст»
        # 3)    Иначе через цикл for:
        #       a)    Через метод get_photo получает до трех фото кандидата
        #       b)    Методом send_message_with_attachments отправляет сообщение пользователю с информацией о кандидате
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
        # 1) Переключает клавиатуру на кнопку "Натйти пару"
        # 2) Методом send_message отправляет прощальное сообщение пользователю
        self.keyboards.add_button('Найти пару', VkKeyboardColor.PRIMARY)
        self.send_message(self.vk_api, f'Пока, пока :)', self.keyboards.get_keyboard())

    def action(self):
        # 1)     Через условный оператор производит сверку текста сообщения с командами из списка команд
        # 2)     При найденном соответствии запускает соответствующий метод
        # 3)     При отсутствии соответствия методом send_message пользователю отправляет сообщение о нераспознанной
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
