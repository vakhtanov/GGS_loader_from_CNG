# -*- coding: utf-8 -*- 
# @wahha  @HomeD
# скрипт для скачки ГГС с сайта http://213.79.66.203:7777/, скачка по областям
#import fetch_data
import requests
import base64
import json


levels=[0,1,2,3,]
levels_dict={0:'CORRECTIONS_CLASS_1',1:'CORRECTIONS_CLASS_2',2:'CORRECTIONS_CLASS_3',3:'CORRECTIONS',}
MasterLink='http://213.79.66.203:7777/proxy.ashx?http://cniigaik/ArcGIS/rest/services/'
link1='MONBAZ'+'/MapServer/'


def countGGS(level):
	link2=str(level)+'/query'
	link3='?text=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&where=OBJECTID%3E0&time=&returnCountOnly=true&returnIdsOnly=false&returnGeometry=true&maxAllowableOffset=&outSR=&outFields=*&f=pjson'
	CountLink=MasterLink+link1+link2+link3
	CountReq=requests.get(CountLink)
	response=CountReq.text
	json_dict=json.loads(response)
	#print(response.encode('utf8'))
	#print(json_dict['count']) 
	return int(json_dict['count']) #ЭТО ПАРСИНГ JSON ЮГУУ! После парсинга получаем словарь
	
def downloadGGS(level, StartObjectID, EndObjectID):
	link2=str(level)+'/query'
	link3='?text=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&objectIds=&'
	#link4='where=OBJECTID%3E%3D'0'+and+OBJECTID%3C'1001
	link4='where=OBJECTID%3E%3D'+str(StartObjectID)+'+and+OBJECTID%3C'+str(EndObjectID)
	link5='&time=&returnCountOnly=false&returnIdsOnly=false&returnGeometry=true&maxAllowableOffset=&outSR=&'
	link6='outFields=*'
	link7='&f=pjson'
	DownloadLink=MasterLink+link1+link2+link3+link4+link5+link6+link7
	GGSReq=requests.get(DownloadLink)
	response=GGSReq.text
	return response
	
for level in levels:
	count=countGGS(level)
	out='in level '+str(level)+' is : '+str(count)+' objects'
	print(out)
	
	startID=0
	#continue # for comment
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
