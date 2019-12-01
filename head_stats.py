import requests
from bs4 import BeautifulSoup
import lxml
import json
import calendar
import zipfile
import os
import csv
from io import TextIOWrapper

# lnk = 'https://hh.ru/oauth/authorize?response_type=code&client_id=31730620'
lnk  = 'https://www.avito.ru/sevastopol/vakansii?p={}'
r = requests.Session()

def get_last_page():
    lnk_pages = 'https://www.avito.ru/sevastopol/vakansii'
    counter = 0
    last_page = None
    while True:
        response_pages = requests.get(lnk_pages)
        soup_pages = BeautifulSoup(response_pages.content, 'lxml')
        pages_list = soup_pages.find('div', {'class': 'pagination'})
        counter += 1
        print(counter)
        if pages_list:
            last_page = int(pages_list.findAll('a', attrs = {'class': 'pagination-page'})[-1].get('href').split('?p=')[1])
            break
    return last_page


def get_vacancies():
    last_page = get_last_page() + 1
    all_data = []
    for page in range(1, last_page):
        print(f'page {page} of {last_page}')
        vacancy_list = []
        while not vacancy_list:
            response = requests.get(lnk.format(page))
            soup = BeautifulSoup(response.content, 'lxml')
            vacancy_list = soup.findAll('div', {'class': 'item__line'})
            for vacancy in vacancy_list:
                vacancy_title = vacancy.find('a', attrs = {'class': 'item-description-title-link'}).text.strip()
                data = vacancy.find('div', attrs = {'class':'data'})
                category = data.find('p').text.strip()
                price = vacancy.find('span', attrs={'itemprop':'price'}).text.split('₽')[0].strip()
                if price.lower() == u'зарплата не указана':
                    price = 0
                else:
                    price = int(price.replace(' ', ''))
                data_v = [vacancy_title, category, price]
                all_data.append(data_v)
            if vacancy_list:
                break
    return all_data

def write_vacancies():
    new_standard = open('_vacancies_sevastopol.csv', 'w', encoding='utf-8', newline='')
    standard_pen = csv.writer(new_standard)
    data_dump = get_vacancies()
    for vacancy in data_dump:
        standard_pen.writerow(vacancy)
        new_standard.flush()

write_vacancies()
