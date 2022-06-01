import requests
import sys

url = 'http://127.0.0.1:8080'  # Spider Project's API Server
filename = 'C:\\py\\AD_Aksai_S.1054.sprj'  # Please prepend with the full path
reportName = 'C:\\Users\\DjumagalievE\\Documents\\Spider Project\\My report\\dsmDays.001.sdoc'

project = requests.post(url, json={'command': 'openFile', 'fileName': filename, 'sessId': ''}) # return docHandle.key
print('\nProject opened.') if project.status_code == 200 else sys.exit(0)
docHandleProject = project.json()['docHandle']

project = requests.post(url, json={"command":"executeScript","docHandle": docHandleProject,'scriptLibName': 'needDSMDays', 'sessId': ''})
print('\nScript executed.') if project.status_code == 200 else sys.exit(0)

report = requests.post(url, json={'command': 'openFile', 'fileName': reportName, 'sessId': ''})
print('\nReport opened.') if report.status_code == 200 else sys.exit(0)
docHandleReport = report.json()['docHandle']

report = requests.post(url, json={'command':'getTableHandle','docHandle': docHandleReport,'sessId':''})
print('\nTable handle obtained.') if report.status_code == 200 else sys.exit(0)
tableHandle = report.json()['tableHandle']

report = requests.post(url, json={'command':'getTable','tableHandle': str(tableHandle),'sessId':''})
print('\nTable obtained.') if report.status_code == 200 else sys.exit(0)
fieldsTableReport = report.json()['array']

print(fieldsTableReport)
#dsmtsm = []
#DSM = dsmtsm.append(float(x['WorkLoadPlan']) for x in dict if dict in fieldsTableReport)
#print(DSM)
#r = [float(x['WorkLoadPlan']) for x in dict if dict in fieldsTableReport]
#print(r)
#DSM = ['%s' % float(x['WorkLoadPlan']) for x in dict if dict in fieldsTableReport]
#print(DSM)