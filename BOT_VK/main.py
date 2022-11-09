import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import os
from dotenv import load_dotenv, find_dotenv
from time import sleep

from db_for_bot import BaseForBot
from bot import BotVK

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

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                sleep(0.4)

                text_msg = event.text.lower()
                BotVK(TKN_GROUP, USER_TOKEN, base, vk, event.user_id, text_msg).action()
