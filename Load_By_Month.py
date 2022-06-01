#import calendar
import sys
from datetime import datetime as dt

import numpy as np
import pandas as pd
import requests

# Spider Project's API Server
url = 'http://172.16.201.42:62449//'
# Please prepend with the full path
filename = 'C:\\Users\\djumagalieve\\Documents\\Spider Project\\Demo Projects\\AD_Aksai_S.1054.sprj'
reportName = 'C:\\Users\\djumagalieve\\Documents\\Spider Project\\My report\\dsmYears.001.sdoc'

r = requests.post(url, json={'command': 'login', 'user': 'Dzhumaes', 'password': 'ElS173tsm'})
print('Login request done.') if r.status_code == 200 else sys.exit(0)
r = r.json()
if r['errcode'] != 0:
    print('Invalid login or password!')
    sys.exit(0)

# return docHandle.key
project = requests.post(url, json={'command': 'openFile', 'fileName': filename, 'sessId': r['sessId']})
print('\nProject opened.') if project.status_code == 200 else sys.exit(0)
docHandleProject = project.json()['docHandle']

# execute Script
project = requests.post(url,json={'command': 'executeScript', 'docHandle': docHandleProject, 'scriptLibName': 'needDSMYears', 'sessId': r['sessId']})
print('\nScript executed.') if project.status_code == 200 else sys.exit(0)

# return docHandle.key
report = requests.post(url, json={'command': 'openFile', 'fileName': reportName, 'sessId': r['sessId']})
print('\nReport opened.') if report.status_code == 200 else sys.exit(0)
docHandleReport = report.json()['docHandle']

# return tableHandle.key
report = requests.post(url, json={'command': 'getTableHandle', 'docHandle': docHandleReport, 'sessId': r['sessId']})
print('\nTable handle obtained.') if report.status_code == 200 else sys.exit(0)
tableHandle = report.json()['tableHandle']

# return table
report = requests.post(url, json={'command': 'getTable', 'tableHandle': str(tableHandle), 'sessId': r['sessId']})
print('\nTable obtained.') if report.status_code == 200 else sys.exit(0)
df = report.json()['array']

# форматирование имен столбцов из str в datetime ('_01_01_22' ---> 2022-01-01 00:00:00)
for index, item in enumerate(df.columns.values):
  df.columns.values[index] = pd.to_datetime(df.columns.values[index], format='_%d_%m_%y', errors='ignore')
  # форматирование имен столбцов из datetime в date (2022-01-01 00:00:00 ---> 2022-01-01)
  if type(df.columns.values[index]) is pd._libs.tslibs.timestamps.Timestamp:
    df.columns.values[index] = dt.date(df.columns.values[index])

# сортировка дней
df_Days = df.select_dtypes(exclude='object')
df_Info = df.select_dtypes(include='object')
df_Days.sort_index(axis=1, inplace=True)
df = df_Info.join(df_Days)

# разбиение массива на 2 отдельных (количество техники и трудоёмкость)
df_Amount = pd.DataFrame(columns=df.columns)
df_WorkLoadPlan = pd.DataFrame(columns=df.columns)
for index, item in enumerate(df.values[:, 2]): # ??? change '2' to 'ParName' in enumerate(df.values[:, 2])
  if 'Количество' in item:
    df_Amount.loc[df_Amount.shape[0]] =  df.values[index]
  elif 'Трудоёмкость' in item:
    df_WorkLoadPlan.loc[df_WorkLoadPlan.shape[0]] = df.values[index]
  else:
    continue

# РАСЧЕТ СРЕДНИХ ЗНАЧЕНИЙ ТЕХНИКИ ПО МЕСЯЦАМ
# форматирование фрейма для последующих операций
df_Amount.set_index('Name', inplace=True)
df_Amount = df_Amount.T

# получение списка значений "год-месяц" для последующего разделения фрейма по месяцам
year_month_list = []
for i in df_Amount.index[3:]:
  year_month = str(i)[:7]
  if (year_month not in year_month_list):
    year_month_list.append(year_month)

# создание пустого фрейма для средних значений техники по месяцам
df_Amount_Mean = pd.DataFrame(columns=df_Amount.columns)

for i in range(len(year_month_list)):
  df = pd.DataFrame(columns=df_Amount.columns)
  for index, item in enumerate(df_Amount.index):
    if year_month_list[i] in str(item):
      df = df.append(df_Amount.iloc[index])
  year = int(year_month_list[i][:4])
  month = int(year_month_list[i][5:7])
  last_day = calendar.monthrange(year, month)[1]

  # переменные с промежуточными датами
  d_01 = dt.strptime((year_month_list[i]+'-01'), '%Y-%m-%d').date()
  d_20 = dt.strptime((year_month_list[i]+'-20'), '%Y-%m-%d').date()
  d_10 = dt.strptime((year_month_list[i]+'-'+str(last_day-20)), '%Y-%m-%d').date()
  d_30 = dt.strptime((year_month_list[i]+'-'+str(last_day)), '%Y-%m-%d').date()

  # переменные с индексами элементов, соответствующих условиям
  idx_1 = df.index[(d_01 <= df.index) & (df.index <= d_20)].copy()
  idx_2 = df.index[(d_10 < df.index) & (df.index <= d_30)].copy()

  # фреймы с рассчитанными средними за первые и последние 20 дней
  df_1 = df.loc[idx_1].mean(axis=0)
  df_2 = df.loc[idx_2].mean(axis=0)

  # слияние с выбором максимального среднего в одну строку
  row_max_mean = pd.concat([df_1, df_2], axis=1).max(axis=1)
  row_max_mean.name = calendar.month_name[month]

  # добавление строки со рассчитанными средними значениями в итоговый фрейм
  df_Amount_Mean = df_Amount_Mean.append(row_max_mean)

# настройка отображения и округление значений фрейма
df_Amount_Mean = df_Amount_Mean.T
df_Amount_Mean = df_Amount_Mean.apply(np.ceil)
df_Amount_Mean = df_Amount_Mean.iloc[:].astype(int)

# форматирование значений месяцев
months = df_Amount_Mean.columns.values.tolist()
df_Amount_Mean.columns = pd.CategoricalIndex(df_Amount_Mean.columns, categories=months, ordered=True)

# РАСЧЕТ ТРУДОЁМКОСТИ ПО МЕСЯЦАМ
# форматирование фрейма для последующих операций
df_WorkLoadPlan.set_index('Name', inplace=True)
df_WorkLoadPlan = df_WorkLoadPlan.T

df_T = pd.DataFrame(columns=df_WorkLoadPlan.columns)

for i in range(len(year_month_list)):
  df = pd.DataFrame(columns=df_WorkLoadPlan.columns)
  for index, item in enumerate(df_WorkLoadPlan.index):
    if year_month_list[i] in str(item):
      df = df.append(df_WorkLoadPlan.iloc[index])
  year = int(year_month_list[i][:4])
  month = int(year_month_list[i][5:7])
  last_day = calendar.monthrange(year, month)[1]

  # переменные с датами первого и последнего дня месяца
  d_01 = dt.strptime((year_month_list[i]+'-01'), '%Y-%m-%d').date()
  d_30 = dt.strptime((year_month_list[i]+'-'+str(last_day)), '%Y-%m-%d').date()

  # переменные с индексами элементов (дат), входящих в месяц
  idx = df.index[(d_01 <= df.index) & (df.index <= d_30)].copy()

  # строка с рассчитанными суммами трудоёмкости за месяц
  row_sum_workloadplan = df.loc[idx].sum(axis=0)
  row_sum_workloadplan.name = calendar.month_name[month]

  # добавление строки со рассчитанными суммами трудоёмкости в итоговый фрейм
  df_T = df_T.append(row_sum_workloadplan)

# настройка отображения и форматирования значений фрейма
df_T = df_T.T
df_T = df_T.iloc[:].astype(int)

# форматирование названий месяцев
months = df_T.columns.values.tolist()
df_T.columns = pd.CategoricalIndex(df_T.columns, categories=months, ordered=True)

# РАСЧЕТ ЗАГРУЗКИ
df_Load = df_T / (30 * 20 * df_Amount_Mean)
df_Load = df_Load.fillna(0)

# форматирование отображения числовых значений с плавающей точкой (1.000 ---> 100%)
for i in df_Load.columns:
  df_Load[i] = df_Load[i].map('{:.1%}'.format)

# СЛИЯНИЕ РЕЗУЛЬТАТОВ
# добавление подназваний столбцов
df_Load.columns = pd.MultiIndex.from_product([["Загрузка"], df_Load.columns])
df_T.columns = pd.MultiIndex.from_product([["Трудоёмкость"], df_T.columns])
df_Amount_Mean.columns = pd.MultiIndex.from_product([["Количество"], df_Amount_Mean.columns])

df_Load = df_Load.swaplevel(axis=1)
df_T = df_T.swaplevel(axis=1)
df_Amount_Mean = df_Amount_Mean.swaplevel(axis=1)

# слияние фреймов загрузки и трудоёмкости
df_T_Load = pd.merge(df_T, df_Load, left_index=True, right_index=True)
df_T_Load.sort_index(axis=1, level=0, inplace=True)

# слияние фреймов загрузки и количества
df_Amount_Load = pd.merge(df_Amount_Mean, df_Load, left_index=True, right_index=True)
df_Amount_Load.sort_index(axis=1, level=0, inplace=True)

# СОХРАНЕНИЕ ФАЙЛОВ
# сохранение результатов "Загрузка/Трудоёмкость" в csv-файл
df_T_Load.to_csv('T_Load_Data.csv')
# сохранение результатов "Загрузка/Трудоёмкость" в xls-файл
df_T_Load.to_excel('T_Load_Data.xlsx')
# сохранение результатов "Загрузка/Количество" в csv-файл
df_Amount_Load.to_csv('Amount_Load_Data.csv')
# сохранение результатов "Загрузка/Количество" в xls-файл
df_Amount_Load.to_excel('Amount_Load_Data.xlsx')