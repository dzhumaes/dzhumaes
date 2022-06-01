import requests
import sys

url = 'http://127.0.0.1:8080'  # Spider Project's API Server
path = input('Введите путь к файлу: ')
print('Путь к файлу:', path)
filename = input('Введите наименование файла с расширением: ')
print('Необходимо открыть файл: ', filename)
fullfn = path+filename
print('Полный путь к проекту: ', fullfn)

r = requests.post(url, json={'command': 'openFile', 'fileName': fullfn, 'sessId': ''}) # return docHandle.key
print('Project opened.') if r.status_code == 200 else sys.exit(0)