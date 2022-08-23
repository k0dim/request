from pprint import pprint
import requests
from loguru import logger
from Modules.APIYandex import Yandex
import datetime

logger.add('log.log', format="{time} {level} {message}", level="INFO")
logger.add('log.log', format="{time} {level} {message}", level="DEBUG")

class Superhero():
    def routes(self):
        self.url = 'https://akabab.github.io/superhero-api/api/all.json'
        respons = requests.get(self.url)
        logger.info(f'Выгрузка списка героев API, {respons}')
        return respons.json()

    def dict_hero(self):
        # self_hero_list = []
        # name_hero = ''
        # while name_hero != 'end':
        #     name_hero = input('Укажите именя героя. Для окончания ввода укажите "end": ')
        #     if name_hero != 'end':
        #         self_hero_list.append(name_hero)
        #     else:
        #         break
        # logger.info(f'Получаем список от пользователя, {self_hero_list}')
        self_hero_list = ['Hulk', 'Captain America', 'Thanos']
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


def work_2(): # Функция, которая загружает файлы в папку на Диске
    logger.info('Запуск программы №2')
    yandex_token = input('Укажите токен API Yandex.Disk: ')
    ya = Yandex(yandex_token)
    logger.info("System: Запуск загрузки файлов")
    ya.floder()
    path_coder = input('Укажите путь к файлу файла: ')
    filename = input('Укажите название файла: ')
    # path_coder = '/Users/dmitriykonnov/request/main.py'
    for element_url in path_coder:
        if element_url == '/':
            path = path_coder.replace('/', '%2F')
        elif element_url == '\\':
            path = path_coder.replace('\\', '%2F')
    logger.info("System: Загрузка файла (ссылка)")
    link_dir = ya.get_linc_upload(f'Шоб бардака не было/{filename}')
    href = link_dir['href']
    logger.info("System: Загрузка файла")
    ya.put_upload(href, path_coder)
    logger.info(f"System: Загрузка {path_coder} на диск")

def work_3():
    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    url = 'https://api.stackexchange.com/2.3/questions'
    params = {'order': 'desc', 'min': f'{yesterday}', 'max': f'{today}', 'sort': 'activity', 'tagged': 'python', 'site': 'stackoverflow' }
    response = requests.get(url, params= params)
    return pprint(response.json())

if __name__ == '__main__':
    num_work = input('Выберите номер задания: ')
    if num_work == '1':
        work_1()
    elif num_work == '2':
        work_2()
    elif num_work == '3':
        work_3()