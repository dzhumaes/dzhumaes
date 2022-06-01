import requests
import sys

url = 'http://127.0.0.1:8080'  # Spider Project's API Server
filename = 'C:\\py\\AD_Aksai_S.1054.sprj'  # Please prepend with the full path
reportName = 'C:\\Users\\DjumagalievE\\Documents\\Spider Project\\My report\\dsmDays.001.sdoc'

project = requests.post(url, json={'command': 'openFile', 'fileName': filename, 'sessId': ''}) # return docHandle.key
print('\nProject opened.') if r.status_code == 200 else sys.exit(0)
docHandle = project.json()['docHandle']
print(docHandle)

project = requests.post(url, json={"command":"executeScript","docHandle": docHandle,"scriptLibName": "needDSMDays", 'sessId': ''})
print('\nScript executed.') if r.status_code == 200 else sys.exit(0)

rep = requests.post(url, json={'command': 'openFile', 'fileName': reportName, 'sessId': ''})
print('\nReport opened.') if r.status_code == 200 else sys.exit(0)
docHandleReport = rep.json()['docHandle']
print(docHandleReport)
print(docHandle)