import datetime

import requests


class ReqVkApi:
    def __init__(self, user_token, version=5.131):
        self.token = user_token
        self.version = version
        self.param = {'access_token': self.token, 'v': self.version}
        self.path = 'http://api.vk.com/method/'

    def get_info_about_user(self, id_user):
        # получает через API инофрмацию о пользователе

        # Возвращает словарь с ключами {Имя, Фамилия, пол, возраст, город, короткий адрес}

        method = 'users.get'
        url = self.path + method
        params = {'user_ids': id_user, 'fields': 'bdate,sex,city,domain',
                  'v': self.version}

        res = requests.get(url, params={**self.param, **params})

        name_user = res.json()['response'][0]['first_name']
        surname_user = res.json()['response'][0]['last_name']
        sex_user = res.json()['response'][0]['sex']
        if len(str(res.json()['response'][0]['bdate'])) < 7 or None:
            age_user = 0
        else:
            age_user = int(datetime.datetime.now().year) - int(res.json()['response'][0]['bdate'][-4:])
        if 'city' in res.json()['response'][0]:
            city_user = res.json()['response'][0]['city']['id']
        else:
            city_user = 1
        domain = res.json()['response'][0]['domain']
        dict_param = {'name': name_user, 'surname': surname_user, 'sex': sex_user, 'age': age_user,
                      'city': city_user, 'domain': domain}
        return dict_param

    def search_people(self, dict_param_for_searching):
        # На вход получает список [age_from, age_up_to, sex, city]. По заданным параметрам ищет 100 подходящих
        # пользователей ВК
        # возвращает [список ID подходящих пользователей]

        method = 'users.search'
        url = self.path + method
        count = 100
        city = dict_param_for_searching['city']
        sex = dict_param_for_searching['sex']
        age_up_to = dict_param_for_searching['age_up_to']
        age_from = dict_param_for_searching['age_from']
        params = {'v': self.version,
                  'fields': 'bdate,sex,city,domain,country',
                  'city': city,
                  'count': count,
                  'sex': sex,
                  'age_to': age_up_to,
                  'age_from': age_from
                  }
        res = requests.get(url, params={**self.param, **params})
        if 'response' in res.json():
            inf_user = res.json()['response']['items']

            list_id = [users_id['id'] for users_id in inf_user]
            return list_id

    def get_photo(self, id_challenger):
        # получает на вход ID пользователя и через API запрашивает до 3 фото из профиля этого пользователя
        # возвращает список строк в формате "photo<id_challenger>_<id_photo>", если фото нет None

        dict_photo = {}
        method = 'photos.get'
        url = self.path + method

        params = {'album_id': 'profile',
                  'extended': 1,
                  'rev': 0,
                  'owner_id': id_challenger,
                  'v': self.version, 'count': 20}
        res = requests.get(url, params={**self.param, **params})

        if 'response' in res.json().keys() and \
                len(res.json()['response']['items']) > 0 and \
                'error' not in res.json().keys():

            for photos in res.json()['response']['items']:
                dict_photo[photos['likes']['count'], photos['id']] = f"photo{photos['owner_id']}_{photos['id']}"

            list_send_photo = []
            i = 0
            while i < 3 and i < len(dict_photo):
                list_send_photo.append(dict_photo[sorted(dict_photo, reverse=True)[i]])
                i += 1

            return ','.join(list_send_photo)

        elif 'response' in res.json().keys() and \
                len(res.json()['response']['items']) == 0:
            return None

        elif 'error' in res.json().keys():
            return None
