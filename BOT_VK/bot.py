import random
from datetime import datetime
from random import randrange
from time import sleep

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from db_for_bot import BaseForBot
from requests_to_vk import ReqVkApi


class Command:
    START = "начать"
    HELLO = "привет"
    FIND = "найти пару"
    NEXT = "ищем дальше"
    IN_FAVORITE = "в избранное"
    FAVORITE = "избранное"
    BYE = "пока"
    END = "завершить"


class KeyboardForBot:

    begin = VkKeyboard(one_time=True)
    begin.add_button('Найти пару', VkKeyboardColor.PRIMARY)
    main = VkKeyboard(one_time=False)
    main.add_button('Завершить', VkKeyboardColor.SECONDARY)
    main.add_button('Ищем дальше', VkKeyboardColor.POSITIVE)
    main.add_line()
    main.add_button('Избранное', VkKeyboardColor.SECONDARY)
    main.add_button('В избранное', VkKeyboardColor.PRIMARY)

    def begin_keyboard(self):
        return self.begin

    def main_keyboard(self):
        return self.main



class BotVK:

    def __init__(self, token_group, token_user, db_session, vk_api) -> [str, str, BaseForBot,
                                                                        vk_api]:
        self.tkn_gr = token_group
        self.tkn_user = token_user
        self.session = db_session
        self.req = ReqVkApi(token_user)
        self.vk_api = vk_api
        self.keyboard = KeyboardForBot()


    @staticmethod
    def get_param_for_searching(user_param):
        # Из параметров пользователя рассчитывает параметры для поиска кандидатов. Если какой-либо из
        # параметров не получен на вход (отсутствуют в профиле), то устанавливает значения по умолчанию
        # Принимает на вход список либо список [name_user, surname_user, sex_user, age_user, city_user, domain],
        # либо список [user_id, name, age, sex, city]
        # возвращает список [возраст от, возраст до, пол противоположный пользователю, город]
        if user_param['age'] == 0:
            age_up_to = 40
            age_from = 20
        else:
            age_up_to = user_param['age']
            age_from = user_param['age'] - 3

        if user_param['sex'] == 1:
            sex = 2
        elif user_param['sex'] == 2:
            sex = 1
        else:
            sex = 0

        if user_param['city'] == 0 or None:
            city = 1
        else:
            city = user_param['city']

        dict_param = {'age_from': age_from, 'age_up_to': age_up_to, 'sex': sex, 'city': city}

        return dict_param

    def send_message(self, id_user, text_message, keyboard=None):
        # Отправляет текстовое сообщение пользователю
        self.vk_api.method('messages.send',
                           {'user_id': id_user,
                            'message': text_message,
                            'random_id': randrange(10 ** 7),
                            'keyboard': keyboard})

    def send_message_with_attachments(self, id_user, text_message, attachments):
        # Отправляет пользователю текстовое сообщение c вложением

        self.vk_api.method(
            'messages.send', {
                'user_id': id_user,
                'message': text_message,
                'random_id': randrange(10 ** 7),
                'attachment': attachments
            }
        )

    def hi_command(self, id_user):
        # 1)     через метод get_info_about_user модуля requests_to_vk получает парамтеры пользователя
        # 2)     методом check_user модуля db_for_bot проверяет есть ли пользователь в БД,
        # если есть – проверяет актуальность имеющихся в базе данных (метод update_param_user модуля db_for_bot
        # если нет, то добавляет данные в базу через метод insert_user модуля db_for_bot
        # 3)     активирует клавиатуру с кнопкой «найти пару»
        # 4)     отправляет приветственное сообщение пользователю (метод send_message)

        user_params = self.req.get_info_about_user(id_user)
        if self.session.check_user(id_user):
            self.session.update_param_user(id_user, user_params)
        else:
            self.session.insert_user(id_user, user_params)

        self.send_message(id_user, f'Привет, {user_params["name"]}!', self.keyboard.begin_keyboard().get_keyboard())

    def next_challenger_command(self, id_user):
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
        user_param = self.session.get_user(id_user)
        if not user_param:
            user_param = self.req.get_info_about_user(id_user)
            self.session.insert_user(id_user, user_param)
        param_for_search = self.get_param_for_searching(user_param)
        people = self.req.search_people(param_for_search)
        challenger_in_base = True
        while challenger_in_base:
            id_challenger = random.choice(people)
            if self.session.check_relation(id_user, id_challenger):
                continue
            else:
                challenger_in_base = False
        info_about_challenger = self.req.get_info_about_user(id_challenger)
        if self.session.check_challenger(id_challenger):
            self.session.update_param_challenger(id_challenger, info_about_challenger)
        else:
            self.session.insert_challenger(id_challenger, info_about_challenger)
        self.session.insert_relation(id_user, id_challenger, datetime.now())
        photo = self.req.get_photo(id_challenger)
        if photo is None:
            self.send_message(id_user, f'{info_about_challenger["name"]} {info_about_challenger["surname"]}\n'
                                       f'https://vk.com/{info_about_challenger["domain"]}\n'
                                       f'Фото отсутствуют, либо закрыт доступ')
        else:
            self.send_message_with_attachments(id_user,
                                               f'{info_about_challenger["name"]} {info_about_challenger["surname"]}\n'
                                               f'https://vk.com/{info_about_challenger["domain"]}',
                                               photo)

    def begin_command(self, id_user):
        # 1)     Переключает клавиатуру на четыре кнопки («Завершить», «Ищем дальше», «В избранное», «Избранное»)
        # 2)     Методом send_message отправляет сообщение о начале поиска
        # 3)     Выполняет метод next_challenger
        self.send_message(id_user, 'Запускаем поиск...', self.keyboard.main_keyboard().get_keyboard())

        self.next_challenger_command(id_user)

    def set_in_favorite_list_command(self, id_user):
        # 1)     Методом get_last_challenger получает последнего выведенного на просмотр кандидата
        # 2)     Если кандидат уже в списке избранных, то методом send_massage отправляет пользователю сообщение
        # «кандидат уже в списке избранных»
        # 3)     Иначе, методом insert_challenger_in_favorite_list записывает пользователя в таблицу в БД
        # 4)     Методом send_message отправляет сообщение пользователю об успешной записи кандидата в список избранных

        id_challenger = self.session.get_last_challenger(id_user)
        if self.session.check_challenger_in_favorite_list(id_user, id_challenger["id"]):
            self.send_message(id_user, 'Последний найденный кандидат уже в списке избранных')
        else:
            self.session.insert_challenger_in_favorite_list(id_user, id_challenger["id"])
            self.send_message(id_user, f'Пользователь {id_challenger["name"]} '
                                       f'{id_challenger["surname"]} добавлен в список избранных')

    def get_favorite_list_command(self, id_user):
        # 1) 	Методом select_favorite_list получает список избранных
        # 2)    Если список пуст, то методом send_message отправляет пользователю сообщение «Ваш список избранных пуст»
        # 3)    Иначе через цикл for:
        #       a)    Через метод get_photo получает до трех фото кандидата
        #       b)    Методом send_message_with_attachments отправляет сообщение пользователю с информацией о кандидате
        # из списка избранных

        favorite_list = self.session.get_favorite_list(id_user)
        if not favorite_list:
            self.send_message(id_user, f'Ваш список избранных пуст')
        else:
            for challenger in favorite_list:
                photo = self.req.get_photo(challenger["id"])

                self.send_message_with_attachments(id_user,
                                                   f'{challenger["name"]} {challenger["surname"]}\n'
                                                   f'https://vk.com/{challenger["domain"]}',
                                                   photo)
                sleep(0.2)

    def bye_command(self, id_user):
        # 1) Переключает клавиатуру на кнопку "Натйти пару"
        # 2) Методом send_message отправляет прощальное сообщение пользователю
        self.send_message(id_user, f'Пока, пока :)', self.keyboard.begin_keyboard().get_keyboard())

    def action(self, event):
        # 1)     Через условный оператор производит сверку текста сообщения с командами из списка команд
        # 2)     При найденном соответствии запускает соответствующий метод
        # 3)     При отсутствии соответствия методом send_message пользователю отправляет сообщение о нераспознанной
        # команде, с рекомендациями воспользоваться кнопками или прочитать инструкцию

        id_user = event.user_id
        text_message = event.text.lower()

        if text_message == Command.HELLO or text_message == Command.START:
            self.hi_command(id_user)
        elif text_message == Command.FIND:
            self.begin_command(id_user)
        elif text_message == Command.NEXT:
            self.next_challenger_command(id_user)
        elif text_message == Command.IN_FAVORITE:
            self.set_in_favorite_list_command(id_user)
        elif text_message == Command.FAVORITE:
            self.get_favorite_list_command(id_user)
        elif text_message == Command.BYE or text_message == Command.END:
            self.bye_command(id_user)
        else:
            self.send_message(id_user, f'Неизвестная команда!\nВоспользуйтей кнопками ниже или '
                                       f'отправьте команду "Найти пару"')
