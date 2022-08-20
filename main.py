from pprint import pprint
import requests
import json
from loguru import logger
import os

logger.add('log.log', format="{time} {level} {message}", level="INFO")
logger.add('log.log', format="{time} {level} {message}", level="DEBUG")

class Superhero():
    def routes(self):
        self.url = 'https://akabab.github.io/superhero-api/api/all.json'
        respons = requests.get(self.url)
        logger.info(f'Выгрузка списка героев API, {respons}')
        return respons.json()

    def dict_hero(self):
        self_hero_list = []
        name_hero = ''
        while name_hero != 'end':
            name_hero = input('Укажите именя героя. Для окончания ввода укажите "end": ')
            if name_hero != 'end':
                self_hero_list.append(name_hero)
            else:
                break
        logger.info(f'Получаем список от пользователя, {self_hero_list}')
        # self_hero_list = ['Hulk', 'Captain America', 'Thanos']
        hero_dict = {}
        hero_all = self.routes()
        for name_hero_one in self_hero_list:
            for one in hero_all:
                if name_hero_one == one['name']:
                    hero_id = one['name']
                    hero_dict[hero_id] =  one['powerstats']['intelligence']
        logger.info(f'Записываем характеристику по героям пользователя, {hero_dict}')
        return hero_dict

# Список всех героев, В консоле ответ не помещается - для проверки записываес json (по потребности)
# with open('m.json', 'w') as f:
#     json.dump(name.routes(), f, sort_keys=True, indent=2)

def work_1():
    logger.info('Запуск программы №1')
    name = Superhero()
    dict_heros = name.dict_hero()
    for name_hero_k, intelligence_hero_v in dict_heros.items():
        if intelligence_hero_v == max(dict_heros.values()):
            print(f'Из списка героев самый умный: {name_hero_k}, "intelligence" - {intelligence_hero_v}')
    return



class Yandex:
    def __init__(self, yandex_token):
        logger.info(f"Yandex: Создан объект Yandex - {self}")
        self.url_api = 'https://cloud-api.yandex.net/v1/disk/'
        self.headers = {'Authorization': f'OAuth {yandex_token}', 'Content-Type': 'application/json', 'Accept': 'application/json'}

    def check_floder(self): # Проверка наличии папки "Шоб бардака не было" 
        url = f'{self.url_api}resources'
        params = {'path': '/Шоб бардака не было'}
        response = requests.get(url, params = params, headers= self.headers)
        logger.info(f"Yandex: Проверка наличии папки: {url, params}")
        logger.debug(f"{response}")
        return response.status_code

    def creat_folder_link(self):  # Получить ссылку на создание папки 
        url = f'{self.url_api}resources'
        params = {'path': 'Шоб бардака не было'}
        response = requests.put(url, params = params, headers = self.headers)
        logger.info(f"Yandex: Получить ссылку на создание папки: {url, params}")
        logger.debug(f"{response}")
        return response.json()

    def creat_folder(self, href_folder): # Создать папку
        self.href_folder = href_folder
        response = requests.put(self.href_folder)
        logger.info(f"Yandex: Создание папки - {self}: {self.href_folder}")
        logger.debug(f"{response}")

    def get_linc_upload(self, file_path): # Получить ссылку на загрузку файлов
        url = f'{self.url_api}resources/upload'
        params = {'path': file_path, 'overwrite': 'true'}
        response = requests.get(url, params = params, headers = self.headers)
        logger.info(f"Yandex: Получить ссылку загрузку файлов: {url, params}")
        logger.debug(f"{response}")
        return response.json()

    def put_upload(self, href, filename): # Загрузить файлы по полученной ссылке
        self.href = href
        response = requests.put(self.href, data = open(filename, 'rb'))
        logger.info(f"Yandex: Отправить файл {filename} на загрузку: {self.href}")
        logger.debug(f"{response}")

def floder(): # Функция проверки на наличие папки, в случае ее отсутствии создает папку (избежание 403)
    if ya.check_floder() == 404:
        logger.info("System: Запуск создания папки")
        link = ya.creat_folder_link()
        href_folder = link['href']
        ya.creat_folder(href_folder)
    elif ya.check_floder() == 200:
        logger.info("System: Папка 'Шоб бардака не было' присутствует на Диске. Запись в существующую папку.")

def work_2(): # Функция, которая загружает файлы в папку на Диске
    logger.info("System: Запуск загрузки файлов")
    floder()
    # path = input('Укажите путь до файла: ')
    path_coder = '/Users/dmitriykonnov/request/main.py'
    path = path_coder.replace('/', '%2F')
    # '%2F'
    # pprint(ya.get_linc_upload(f'{path}'))
    link_dir = ya.get_linc_upload(f'Шоб бардака не было/{path}')
    href = link_dir['href']
    ya.put_upload(href, path_coder)
    logger.info(f"System: Загрузка {path_coder} на диск")


if __name__ == '__main__':
    # Задание №1
    # work_1() 
    # Вопрос: рационально ли в одном методе доставать лист героев по API каждый раз, при проверке по имени, или рационально одним методом создать один общий список и втором методом достать нужных героев с характеристиками?

    yandex_token = 'AQAAAAATf-PhAADLW50Lxq76NkyFhElSEL_l-oo'
    ya = Yandex(yandex_token)
    work_2()

    path = '/course_project/'
    # pprint(ya.get_linc_upload(path))