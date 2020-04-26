# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

import json
import logging
import re
import urllib.request as request

from os.path import isdir, isfile, join, basename, splitext
from json import dump as json_dump, load as json_load
from typing import Optional, List, Dict, Any, NamedTuple, Tuple
from datetime import datetime

# from defs import COVID19RU_PENDING

COVID19RU_PENDING = '.'

RE_HTML = re.compile(r'class="config-view">(.+?)<')
RE_TIME = re.compile(r', (.+?) \(')

PendingData=NamedTuple('PendingData', [('utcnow',datetime),('val',dict)])


TIME="%d-%m-%Y__%H:%M:%S:%f"

def timestring(dt:Optional[datetime]=None)->str:
  """ Return timestamp in UTC """
  dt2= datetime.utcnow() if dt is None else dt
  return dt2.strftime(TIME)


def fetch_yandex_text()->str:
  with request.urlopen('https://yandex.ru/web-maps/covid19') as response:
    return response.read().decode('utf-8')

def fetch_yandex(dump_folder:Optional[str]=COVID19RU_PENDING)->PendingData:
  """ Fetch COVID19 data from Yandex
  Based on https://github.com/AlexxIT/YandexCOVID/blob/master/custom_components/yandex_covid/sensor.py
  """
  text = fetch_yandex_text()

  m = RE_HTML.search(text)
  data = json.loads(m[1])

  attrs = {
      p['name']: {
          'cases': p['cases'],
          'cured': p['cured'],
          'deaths': p['deaths'],
          'coordinates':list(p['coordinates']), # [Lon,Lat] !!!
          'histogram':p.get('histogram',[])
      }
      for p in data['covidData']['items']
      if 'ru' in p and p['ru']==True
  }

  # items = data['covidData']['stat']['items']
  # attrs['Россия'] = {
  #     'cases': int(items[0]['value']),
  #     'new_cases': int(items[1]['value']),
  #     'cured': int(items[2]['value']),
  #     'deaths': int(items[3]['value'])
  # }
  # print(attrs)
  # m = re.search(r', (.+?) \(', data['covidData']['subtitle'])
  # state = m[1]
  data = PendingData(datetime.utcnow(), attrs)
  # print(state)
  #if dump_folder is not None:
  #  assert isdir(dump_folder)
  #  filepath = join(dump_folder,timestring(data.utcnow)+'.json')
  #  with open(filepath,'w') as f:
  #    json_dump(data.val, f, indent=4, ensure_ascii=False)
  #  print(f'Saved {filepath}')

  print ('Done')

  return data



def fetch_file(filepath:str, dump_folder:str=COVID19RU_PENDING)->PendingData:
  ts:datetime=datetime.strptime(splitext(basename(filepath))[0],TIME)
  with open(join(dump_folder,filepath),'r') as f:
    d=json_load(f)
  data=PendingData(ts,d)
  # print(data)
  # print(ts)
  return data



REGIONS=[('Moscow','Москва'),
        ('Saint Petersburg','Санкт-Петербург'),
        ('Moscow oblast','Московская область'),
        ('Samara oblast','Самарская область'),
        ("Saha republic","Республика Саха (Якутия)"),
        ("Sverdlov oblast","Свердловская область"),
        ("Kaliningrad oblast","Калининградская область"),
        ("Kirov oblast","Кировская область"),
        ("Novosibirsk oblast","Новосибирская область"),
        ("Krasnoyarskiy kray","Красноярский край"),
        ("Tambov oblast","Тамбовская область"),
        ("Lipetsk oblast","Липецкая область"),
        ("Tver oblast","Тверская область"),
        ("Habarovskiy kray","Хабаровский край"),
        ("Tumen oblast","Тюменская область"),
        ("Tula oblast","Тульская область"),
        ("Perm oblast","Пермский край"),
        ("Nizhegorodskaya oblast","Нижегородская область"),
        ("Krasnodarskiy kray","Краснодарский край"),
        ("Voronezh oblast","Воронежская область"),
        ("Kemerovo oblast","Кемеровская область"),
        ("Republic of Hakassia","Республика Хакасия"),
        ("Murmansk oblast","Мурманская область"),
        ("Komi republic","Республика Коми"),
        ("Kaluga oblast","Калужская область"),
        ("Ivanovo oblast","Ивановская область"),
        ("Zabaykalskiy kray","Забайкальский край"),
        ("Tomsk oblast","Томская область"),
        ("Arkhangelsk oblast","Архангельская область"),
        ("Ryazan oblast","Рязанская область"),
        ("Republic of Chuvashia","Чувашская Республика"),
        ("Ulianovsk oblast","Ульяновская область"),
        ("Yaroslavl oblast","Ярославская область"),
        ("Pensa oblast","Пензенская область"),
        ("Belgorod oblast","Белгородская область"),
        ("Hanty-Mansiyskiy AO","Ханты-Мансийский АО"),
        ("Leningradskaya oblast","Ленинградская область"),
        ("Orenburg oblast","Оренбургская область"),
        ("Saratov oblast","Саратовская область"),
        ("Republic of Tatarstan","Республика Татарстан"),
        ("Kurgan oblast","Курганская область"),
        ("Republic of Kabardino-Balkaria","Кабардино-Балкарская Республика"),
        ("Cheliabinsk oblast","Челябинская область"),
        ("Stavropolskiy kray","Ставропольский край"),
        ("Briansk oblast","Брянская область"),
        ("Republic of Udmurtia","Удмуртская Республика"),
        ("Novgorod oblast","Новгородская область"),
        ("Republic of Crimea","Республика Крым"),
        ("Republic of Bashkortostan","Республика Башкортостан"),
        ("Chechen republic","Чеченская Республика"),
        ("Primorskiy kray","Приморский край"),
        ("Volgograd oblast","Волгоградская область"),
        ("Orel oblast","Орловская область"),
        ("Pskov oblast","Псковская область"),
        ("Rostov oblast","Ростовская область"),
        ("Republic of Buriatia","Республика Бурятия"),
        ("Republic of Mordovia","Республика Мордовия"),
        ("Republic of Dagestan","Республика Дагестан"),
        ("Sakhalin oblast","Сахалинская область"),
        ("Kostroma oblast","Костромская область"),
        ("Smolensk oblast","Смоленская область"),
        ("Republic of Adygeia","Республика Адыгея"),
        ("Omsk oblast","Омская область"),
        ("Irkutsk oblast","Иркутская область"),
        ("Amursk oblast","Амурская область"),
        ("Altayskiy kray","Алтайский край"),
        ("Vladimir oblast","Владимирская область"),
        ("Vologda oblast","Вологодская область"),
        ("Republic of Kalmykia","Республика Калмыкия"),
        ("Republic of Mariy El","Республика Марий Эл"),
        ("Republic of Chuvashia","Республика Чувашия"),
        ("Astrahan oblast","Астраханская область"),
        ("Magadan oblast","Магаданская область"),
        ("Sevastopol","Севастополь"),
        ("Kursk oblast","Курская область"),
        ("Republic of North Osetia - Alania","Республика Северная Осетия — Алания"),
        ("Yamalo-Nenetskiy AO","Ямало-Ненецкий автономный округ"),
        ("Ingushetia republic","Республика Ингушетия"),
        ("Jewish Autonomous oblast","Еврейская автономная область"),
        ("Kamchatskiy kray","Камчатский край"),
        ("Republic of Karelia", "Республика Карелия"),
        ("Republic of Karachaevo-Cherkessia", "Карачаево-Черкесская Республика"),
        ("Republic of Tyva", "Республика Тыва"),
        ("Nenetskiy autonomous oblast", "Ненецкий автономный округ"),
        ("Chukotskiy autonomous oblast", "Чукотский автономный округ"),
        ("Altay republic", "Республика Алтай"),
        ]

REGIONS_RU_EN={r_ru:r_en for r_en,r_ru in REGIONS}
REGIONS_EN_RU={r_en:r_ru for r_en,r_ru in REGIONS}

Lat=float
Lon=float

LOCATION:Dict[str,Tuple[Lat,Lon]]={
	"Moscow":(55.75222, 37.61556),
	"Saint Petersburg":(59.93863, 30.31413),
	"Moscow oblast":(55.81363, 36.71631),
	"Samara oblast":(53.20007, 50.15),
	"Saha republic":(62.30161, 32.68536),
	"Sverdlov oblast":(43.25, 71.75),
	"Kaliningrad oblast":(54.70649, 20.51095),
	"Kirov oblast":(58.59665, 49.66007),
	"Novosibirsk oblast":(55.0415, 82.9346),
	"Krasnoyarskiy kray":(58.0, 93.0),
	"Tambov oblast":(52.73169, 41.44326),
	"Lipetsk oblast":(52.60311, 39.57076),
	"Tver oblast":(56.85836, 35.90057),
	"Habarovskiy kray":(48.48271,135.08379),
	"Tumen oblast":(57.15222, 65.52722),
	"Tula oblast":(54.19609, 37.61822),
	"Perm oblast":(58.01046, 56.25017),
	"Nizhegorodskaya oblast":(56.32867, 44.00205),
	"Krasnodarskiy kray":(44.98811, 38.97675),
	"Voronezh oblast":(51.67204, 39.1843),
	"Kemerovo oblast":(55.33333, 86.08333),
	"Republic of Hakassia":(53.71556, 91.42917),
	"Murmansk oblast":(68.97917, 33.09251),
	"Komi republic":(64.0, 54.0),
	"Kaluga oblast":(54.5293, 36.27542),
	"Ivanovo oblast":(56.99719, 40.97139),
	"Zabaykalskiy kray":(52.0, 117.0),
	"Tomsk oblast":(56.49771, 84.97437),
	"Arkhangelsk oblast":(64.0, 44.0),
	"Ryazan oblast":(54.6269, 39.6916),
	"Republic of Chuvashia":(56.13222, 47.25194),
	"Ulianovsk oblast":(54.32824, 48.38657),
	"Yaroslavl oblast":(57.62987, 39.87368),
	"Pensa oblast":(53.20066, 45.00464),
	"Belgorod oblast":(50.61074, 36.58015),
	"Hanty-Mansiyskiy AO":(61.00417, 69.00194),
	"Leningradskaya oblast":(60.0, 32.0),
	"Orenburg oblast":(51.7727, 55.0988),
	"Saratov oblast":(51.54056, 46.00861),
	"Republic of Tatarstan":(55.33333, 51.0),
	"Kurgan oblast":(55.45, 65.33333),
	"Republic of Kabardino-Balkaria":(43.355, 42.43917),
	"Cheliabinsk oblast":(55.15402, 61.42915),
	"Stavropolskiy kray":(45.0, 44.0),
	"Briansk oblast":(53.25209, 34.37167),
	"Republic of Udmurtia":(57.0, 53.0),
	"Novgorod oblast":(56.32867, 44.00205),
	"Republic of Crimea":(45.0, 34.0),
	"Republic of Bashkortostan":(54.0, 56.0),
	"Chechen republic":(43.2, 45.78889),
	"Primorskiy kray":(45.0, 135.0),
	"Volgograd oblast":(48.71939, 44.50183),
	"Orel oblast":(52.96508, 36.07849),
	"Pskov oblast":(57.8136, 28.3496),
	"Rostov oblast":(47.23135, 39.72328),
  "Republic of Buriatia":(54.54, 112.348699),
  "Republic of Mordovia":(54.20, 44.319669),
  "Republic of Dagestan":(42.26, 47.095742),
}

LOCATION_DEF=(61.52401,105.31875600000001)

CSSE2_HEADER=('FIPS,Admin2,Province_State,Country_Region,Last_Update,Lat,Long_,'
              'Confirmed,Deaths,Recovered,Active,Combined_Key')

def yandex_unpack_coordinates(dat:dict, default)->Tuple[float,float]:
  c=dat.get('coordinates')
  if c is not None:
    return (c[1],c[0])
  return default

def format_csse2(data:PendingData, dump_folder:Optional[str]=COVID19RU_PENDING, assert_unknown:bool=True)->List[str]:
  """ Format the data in the new CCSE format.

  Example output:
  ,,Moscow,Russia,3/22/20 00:00,55.75222,37.61556,191,1,0,"Moscow, Russia"
  ,,Moscow,Russia,2020-03-24 10:50:00,55.75222,37.61556,262,1,9,"Moscow, Russia"
  """
  res = []
  misses = []
  for c_ru,dat in data.val.items():
    if (not assert_unknown) and (not c_ru in {ru:en for en,ru in REGIONS}):
      misses.append(c_ru)
      continue
    c_en={ru:en for en,ru in REGIONS}[c_ru]

    update_time = data.utcnow.strftime("%Y-%m-%d %H:%M:%S")
    loc_lat,loc_lon = LOCATION.get(c_en, yandex_unpack_coordinates(dat,LOCATION_DEF))
    kw = f"{c_en},Russia"
    active=int(dat['cases'])-int(dat['deaths'])-int(dat['cured'])
    res.append((
      f",,\"{c_en}\",Russia,{update_time},{loc_lat},{loc_lon},"
      f"{dat['cases']},{dat['deaths']},{dat['cured']},{active},\"{kw}\""))

  if dump_folder is not None:
    filepath = join(dump_folder,timestring(data.utcnow)+'.csv')
    with open(filepath,'w') as f:
      f.write('\n'.join([CSSE2_HEADER]+res))
    print(f'Saved {filepath}')
  if len(misses)>0:
    print(f'Missed locations: {misses}')
  
  print (str(filepath))

  return res, str(filepath)

def dryrun():
  format_csse2(fetch_yandex(dump_folder=None), dump_folder=None, assert_unknown=True)


from time import sleep

def monitor()->None:
  while True:
    try:
      format_csse2(fetch_yandex(), assert_unknown=False)
    except KeyboardInterrupt:
      raise
    except Exception as e:
      print('Exception', e, 'ignoring')
    for i in range(60):
      print(f'{60-i}..',end='',flush=True)
      sleep(60)


