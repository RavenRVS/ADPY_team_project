import os
from time import sleep

import vk_api
from dotenv import load_dotenv, find_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from bot import BotVK
from db_for_bot import BaseForBot

load_dotenv(find_dotenv())

USER_TOKEN = os.environ.get("TOKEN")
TKN_GROUP = os.environ.get("TOKENGRP")
BASE_TYPE = os.environ.get("BASE_TYPE")
BASE_USER_NAME = os.environ.get("BASE_USER_NAME")
BASE_PWD = os.environ.get("BASE_PWD")
BASE_NAME = os.environ.get("BASE_NAME")

if __name__ == '__main__':

    vk = vk_api.VkApi(token=TKN_GROUP)
    longpoll = VkLongPoll(vk)

    base = BaseForBot(BASE_TYPE, BASE_USER_NAME, BASE_PWD, BASE_NAME)
    bot = BotVK(TKN_GROUP, USER_TOKEN, base, vk)

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                sleep(0.4)

                bot.action(event)
