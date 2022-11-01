import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

import random
import os
from dotenv import load_dotenv, find_dotenv
from time import sleep
from datetime import datetime

from sql_function import connection, create_tables, select_date_from_table
from bot import Bot_VK
from

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    try:
        vk = vk_api.VkApi(token=os.getenv('GROUP_TOKEN'))
        longpoll = VkLongPoll(vk)
    except:
        print('Не удалось подключиться к API VK. Проверьте наличие интернет соединение и актуальность введенного '
              'ключа доступа.')

    connection_bd = connection(*os.getenv('файл с параметрами подключения к БД').split(','))
    create_tables(connection)
    user_bd = select_date_from_table(connection, 'users')
    challengers_bd = select_date_from_table(connection, 'challengers')
    relation_bd = select_date_from_table(connection, 'relation_lists')

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                sleep(0.4)

                text_msg = event.text.lower()
                Bot_VK(os.getenv('GROUP_TOKEN'),
                       event.user_id).action(connection_bd, user_bd, challengers_bd, relation_bd, text_msg)
