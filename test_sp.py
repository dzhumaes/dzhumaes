import requests
import sys

url = 'http://127.0.0.1:8080'  # Spider Project's API Server
filename = "C:\\py\\AD_Aksai_S.1054.sprj"  # Please prepend with the full path


r = requests.post(url, json={'command': 'openFile', 'fileName': filename, 'sessId': ''}) # return docHandle.key
print('Project opened.') if r.status_code == 200 else sys.exit(0) #
docHandle = r.json()['docHandle']
print(r)
print(docHandle)

r = requests.post(url, json={'command': 'getTableHandle', 'docHandle': str(docHandle), 'table': 'GanttAct', 'sessId': ''}) # return tableHandle.key
print('Table handle obtained.') if r.status_code == 200 else sys.exit(0)
tableHandle = r.json()['tableHandle']
print(r)
print(tableHandle)

r = requests.post(url, json={'command': 'getTable', 'tableHandle': str(tableHandle), 'sessId': ''}) # return arrayTable.key
print('Table content obtained.') if r.status_code == 200 else sys.exit(0)
r = r.json()
print(r)

print(docHandle)
print(tableHandle)