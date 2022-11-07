import datetime

import requests
from time import sleep


class ReqVkApi:
    def __init__(self, id_user, user_token, version=5.131):
        self.token = user_token
        self.id_user = id_user
        self.version = version
        self.param = {'access_token': self.token, 'v': self.version}
        self.path = 'http://api.vk.com/method/'

    def get_info_about_user(self, id_user):
        # получаем через API инофрмацию о пользователе

        # return [Имя, Фамилия, пол, возраст, город, короткий адрес]

        sleep(0.4)
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
        city_user = res.json()['response'][0]['city']['id']
        domain = res.json()['response'][0]['domain']
        list_param = [name_user, surname_user, sex_user, age_user, city_user, domain]
        return list_param

    def search_people(self, list_param_for_searching):
        # На вход получаем список [age_from, age_up_to, sex, city]. По заданным параметрам ищет 100 подходящих
        # пользователей ВК

        # return [список ID подходящих пользователей]
        sleep(0.4)
        method = 'users.search'
        url = self.path + method
        count = 100
        city = list_param_for_searching[3]
        sex = list_param_for_searching[2]
        age_up_to = list_param_for_searching[1]
        age_from = list_param_for_searching[0]
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
        # получаем до трех фото найденного кандидата

        # return список строк в формате "photo<id_challenger>_<id_photo>", если фото нет None

        sleep(0.4)
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
            if len(dict_photo) >= 3:
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 2]])
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 3]])

            elif 1 < len(dict_photo) <= 2:
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 2]])

            elif 0 < len(dict_photo) <= 1:
                list_send_photo.append(dict_photo[sorted(dict_photo)[len(dict_photo) - 1]])

            print(','.join(list_send_photo))
            return ','.join(list_send_photo)

        elif 'response' in res.json().keys() and \
                len(res.json()['response']['items']) == 0:
            return None

        elif 'error' in res.json().keys():
            return None
