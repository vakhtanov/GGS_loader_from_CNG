# -*- coding: utf-8 -*- 
# @wahha  @HomeD
# скрипт для скачки ГГС с сайта http://213.79.66.203:7777/, скачка по областям
#import fetch_data
import requests
import base64
import json


levels=[0,1,2,3,4,5,6,7,8,9,10]
levels_dict={0:'GFGS',1:'GGS-1',2:'GVO 1 klass',3:'GVO 2 klass',4:'GGS 4 klass',5:'GGS 3 klass',6:'GGS 1 klass',7:'GGS 2 klass',8:'FAGS',9:'SGS-1',10:'VGS',}

def countGGS(level):
	link1='http://213.79.66.203:7777/proxy.ashx?http://cniigaik/ArcGIS/rest/services/GGS/MapServer/'
	link2=str(level)+'/query'
	link3='?text=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&where=OBJECTID%3E0&time=&returnCountOnly=true&returnIdsOnly=false&returnGeometry=true&maxAllowableOffset=&outSR=&outFields=*&f=pjson'
	CountLink=link1+link2+link3
	CountReq=requests.get(CountLink)
	response=CountReq.text
	json_dict=json.loads(response)
	#print(response.encode('utf8'))
	#print(json_dict['count']) 
	return int(json_dict['count']) #ЭТО ПАРСИНГ JSON ЮГУУ! После парсинга получаем словарь
	
def downloadGGS(level, StartObjectID, EndObjectID):
	link1='http://213.79.66.203:7777/proxy.ashx?http://cniigaik/ArcGIS/rest/services/GGS/MapServer/'
	link2=str(level)+'/query'
	link3='?text=&geometry=&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&'
	#link4='where=OBJECTID%3E%3D'0'+and+OBJECTID%3C'1001
	link4='where=OBJECTID%3E%3D'+str(StartObjectID)+'+and+OBJECTID%3C'+str(EndObjectID)
	link5='&time=&returnCountOnly=false&returnIdsOnly=false&returnGeometry=true&maxAllowableOffset=&outSR=&'
	link6='outFields=*'
	link7='&f=pjson'
	DownloadLink=link1+link2+link3+link4+link5+link6+link7
	GGSReq=requests.get(DownloadLink)
	response=GGSReq.text
	return response
	
for level in levels:
	count=countGGS(level)
	out='in level '+str(level)+' is : '+str(count)+' objects'
	print(out)
	
	startID=0
	
	while startID<count:
		endID=startID+1000
		filename=str(levels_dict[level])+'_objects_'+str(startID)+'-'+str(endID)+'.json'
		with open(filename,'w') as fd:
			outdata=downloadGGS(level, startID, endID)
			try:
				fd.write(outdata.encode('utf8'))
				print('In level '+str(levels_dict[level])+' objects:'+str(startID)+'-'+str(endID)+' RECODED')
			except Exception as e:
				print(e)
		##здесь мой код
		startID=endID #Конец цикла по слою


"""
#rayon_count=50
#filename='yanao.txt'

link='http://pbprog.ru/webservices/oms/ajax_oms.php?type=fs&cn='+region_code+'%3A'
#link_full='http://pbprog.ru/webservices/oms/ajax_oms.php?type=fs&cn=66%3A01' 

headers = {'X-Requested-With':'XMLHttpRequest','Cookie':'_ym_uid=1508829202456486828; BX_USER_ID=345f53efb749c88b92c3744f1042df14; BITRIX_SM_LOGIN=wahha; BITRIX_SM_SOUND_LOGIN_PLAYED=Y; last_visit=1508902955787::1508913755787; __utma=16333431.2118996432.1508829202.1508846067.1508913757.5; __utmc=16333431; __utmz=16333431.1508832650.2.2.utmcsr=yandex|utmccn=(organic)|utmcmd=organic; _ym_isad=2; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A1%2C%22EXPIRE%22%3A1508965140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; tmr_detect=0%7C1508913765891; PHPSESSID=5cc9cbedfac835b4bc9ae15acecc368e; BITRIX_SM_UIDH=c4c748dc20c1a16b16209a430e30a080; BITRIX_SM_UIDL=wahha; BITRIX_SM_SALE_UID=1937074'}
# построение списка текстов из 2х символов на всякий случай
# i=[str(i).rjust(2,'0') for i in range(1,16)]


kvartal_spisok=[str(i).rjust(2,'0') for i in range(1,rayon_count+1)]
#i=1
# цикл по кварталам
with open(filename,'w') as fd:
#	while i<rayon_count:
#_______________________________
#старый вариант добавления нуля в начало цифры
#		if i<10:
#			kvartal='0'+str(i)
#		else:
#			kvartal=str(i)
	for kvartal in kvartal_spisok:
		print('kvartal: '+kvartal)
		req_link=link+kvartal
		print('link:',req_link)
		print('ZAPROS!!!')
			#req = requests.Request('GET',req_link, auth=('user', 'pass'))
		#Запрос к сайту с пунктами
		req=requests.get(req_link,headers=headers)
		#Декодировка из бейза64
		try:
			req_out=base64.b64decode(req.text)
		except:
			req_out='____________\n'
		req_out=req_out.replace('"omss": [','"omss": [\n')
		req_out=req_out.replace('}, {','},\n{')
		req_out=req_out.replace('"}]}','"}\n')
		req_out=req_out.replace('", "','*')
		req_out=req_out.replace('": "','*')
		print('ZAMENA')
#    for chunk in r.iter_content(chunk_size=128):
# запись в файл
		fd.write(req_out)
		print('ZAPISAN')
#		i=i+1
"""