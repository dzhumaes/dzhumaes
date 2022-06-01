import requests
import sys

url = 'http://127.0.0.1:8080'  # Spider Project's API Server
filename = "C:\\py\\AD_Aksai_S.1054.sprj"  # Please prepend with the full path

r = requests.post(url, json={'command': 'openFile', 'fileName': filename, 'sessId': ''}) # return docHandle.key
print('\nProject opened.') if r.status_code == 200 else sys.exit(0)
docHandle = r.json()['docHandle']

r = requests.post(url, json={"command":"executeScript","docHandle": docHandle,"scriptLibName": "needDSMDays", 'sessId': ''})
print('\nСценарий выполнен успешно.') if r.status_code == 200 else sys.exit(0)