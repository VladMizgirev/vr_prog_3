import requests
import json
import time
from datetime import datetime as dt
import os

class VK:
    url_vk = 'https://api.vk.com/method/'
    url_yad = 'https://cloud-api.yandex.net/v1/disk/resources'
    def __init__(self, access_token, user_id, token_poligon, version= 5.199):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.token_poligon = token_poligon
        self.params = {'access_token': self.token, 'v': self.version}
        self.name_likes_list = []
        self.name_date_list = []
        self.name_id_list = []
    def users_info(self):
        params = {'user_ids': self.id}
        response = requests.get(self.url, params={**self.params, **params})
        return response.json()
    def get_common_params(self):
        return {'access_token': self.token, 'v': 5.199, 'owner_id': self.id, 'extended': 1}
    def get_photos(self):
        response = requests.get(f'{self.url_vk}photos.getAll', params = self.get_common_params())
        return response.json()
    def load_foto(self):
        data = vk.get_photos()
        print(data)
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self.token_poligon}'}
        for i in data['response']['items']:
            file_url = i['sizes'][-1]['url']
            sizes_file = i['sizes'][-1]['type']
            name_likes = i['likes']['count']
            name_date = dt.fromtimestamp(i['date']).strftime('%Y_%m_%d_%H_%M_%S')
            self.name_date_list.append(dt.fromtimestamp(i['date']).strftime('%Y_%m_%d_%H_%M_%S'))
            self.name_likes_list.append(i['likes']['count'])
            name_id = i['id']
            self.name_id_list.append(i['id'])    
            time.sleep(0.1)
            api = requests.get(file_url)
            count_likes = self.name_likes_list.count(name_likes)
            count_date = self.name_date_list.count(name_date)
            save_file_likes = f'/test/{name_likes}.jpg'
            save_file_likes_json = f'/test/{name_likes}.json'
            save_file_date = f'/test/{name_date}.jpg'
            save_file_date_json = f'/test/{name_date}.json'
            save_file_id = f'/test/{name_id}.jpg'
            save_file_id_json = f'/test/{name_id}.json'
            if count_likes <= 1:
                with open('images/%s.jpg' % name_likes, 'wb') as f:
                      f.write(api.content)
                res_likes = requests.get(f'{self.url_yad}/upload?path={save_file_likes}', headers=headers).json()
                res_likes_json = requests.get(f'{self.url_yad}/upload?path={save_file_likes_json}', headers=headers).json()
                with open(f'images/{name_likes}.jpg', 'rb') as f:
                    try:
                        requests.put(res_likes['href'], files={'file':f})
                    except KeyError:
                        print(res_likes)
                file_json = [{'name': name_likes, 'sizes': sizes_file}]
                with open('images/%s.json' % name_likes, 'w') as f:
                      json.dump(file_json, f)
                with open(f'images/{name_likes}.json', 'rb') as f:
                    try:
                        requests.put(res_likes_json['href'], files={'file':f})
                    except KeyError:
                        print(res_likes_json)
            else:
                if count_date <= 1:
                    with open('images/%s.jpg' % name_date, 'wb') as f:
                      f.write(api.content)
                    res_date = requests.get(f'{self.url_yad}/upload?path={save_file_date}', headers=headers).json()
                    res_date_json = requests.get(f'{self.url_yad}/upload?path={save_file_date_json}', headers=headers).json()
                    with open(f'images/{name_date}.jpg', 'rb') as f:
                        try:
                            requests.put(res_date['href'], files={'file':f})
                        except KeyError:
                            print(res_date)
                    file_json = [{'name': name_date, 'sizes': sizes_file}]
                    with open('images/%s.json' % name_date, 'w') as f:
                        json.dump(file_json, f)
                    with open(f'images/{name_date}.json', 'rb') as f:
                        try:
                            requests.put(res_date_json['href'], files={'file':f})
                        except KeyError:
                            print(res_date_json)
                else:
                    with open('images/%s.jpg' % name_id, 'wb') as f:
                      f.write(api.content)
                    res_id = requests.get(f'{self.url_yad}/upload?path={save_file_id}', headers=headers).json()
                    res_id_json = requests.get(f'{self.url_yad}/upload?path={save_file_id_json}', headers=headers).json()
                    with open(f'images/{name_id}.jpg', 'rb') as f:
                        try:
                            requests.put(res_id['href'], files={'file':f})
                        except KeyError:
                            print(res_id)
                    file_json = [{'name': name_id, 'sizes': sizes_file}]
                    with open('images/%s.json' % name_id, 'w') as f:
                      json.dump(file_json, f)
                    with open(f'images/{name_id}.json', 'rb') as f:
                        try:
                            requests.put(res_id_json['href'], files={'file':f})
                        except KeyError:
                            print(res_id_json)

file_name = "token.txt"

if os.path.isfile(file_name):
    with open(file_name, "r") as file:
        access_token = str(file.read().strip())
        print(access_token)
        print(f"Файл token.txt найден. Токен из файла: {access_token}")
else:
    with open(file_name, "w") as file:
        file.write('')
        print("Файл не найден, создан новый файл token.txt. Введите токен и сохраните его в этом файле.")
    with open(file_name, "r") as file:
        access_token = str(file.read().strip())
        print(access_token)
        print(f"Файл token.txt найден. Токен из файла: {access_token}")

token_poligon = str(input())
user_id = int(input())
vk = VK(access_token, user_id, token_poligon)

vk.load_foto()
