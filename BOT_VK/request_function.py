class ReqVkApi:
    def __init__(self, user_token, version=5.131):
        self.token = user_token
        self.version = version  # Версия API VK
        self.param = {'access_token': self.token, 'v': self.version}
        self.path = 'http://api.vk.com/method'

    def get_info_about_user(self, id_user):
        pass
        # получаем через API инофрмацию о пользователе

        # return [Имя, Фамилия, пол, возраст, город]

    def search_people(self, пол, возраст_от, возраст_до, город):
        pass
        # по заданным параметрам ищем подходящих пользователей ВК

        # return [список ID подходящих пользователей]

    def get_link_challenger(self, id_challenger):
        pass
        # получаем ссылку на страницу кандидата

        # return link(ссылка тип str)

    def get_photo(self, id_challenger):
        pass
        # получаем до трех фото найденного кандидата

        # return список строк в формате "photo<id_challenger>_<id_photo>", если фото нет None