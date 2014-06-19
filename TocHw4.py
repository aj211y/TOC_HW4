# -*- coding: utf-8 -*- #告訴直譯器要用utf-8 宣告本文件應以UTF-8格式儲存
#!/usr/bin/python
#姓名:吳孟庭
#學號:F74006323
#系級:資訊104乙班

import urllib
import sys
import json

#如果沒有給網頁參數的話
if len(sys.argv)< 2:
	print "no input is given"
else:
	content = urllib.urlopen(sys.argv[1]).read() #parse網頁下來
	json_input = json.loads(content) #takes a JSON string and returns it as a Python data structure

	print content
	road_by_key = {} #記錄出現過的道路名字跟出現次數 建立dictionary(map) 有key值找value
	road_by_value = {} #有value值找key
	id_num = 0  #id總個數
	year = [] #根據id記錄每條路出現過的年月 建立2維陣列
	num = {}    #根據id記錄每條路交易過的年月總數
	max_num = 0 #最多個數
	max_id = [] #最多個數的id

	for element in json_input:
		#將路名parse到name變數中 只留存到XX大道XX路或XX街或XX巷
		name = u""
		i = 0 #第幾個字
		while (i < len(element[u"土地區段位置或建物區門牌"])-1 and element[u"土地區段位置或建物區門牌"][i]!=u"路" and element[u"土地區段位置或建物區門牌"][i]!=u"街" and element[u"土地區段位置或建物區門牌"][i]!=u"巷"):
			if (element[u"土地區段位置或建物區門牌"][i] == u"大" and i+1<len(element[u"土地區段位置或建物區門牌"])-1 and element[u"土地區段位置或建物區門牌"][i+1] == u"道"):#表示他為路名 XX大道
				name += element[u"土地區段位置或建物區門牌"][i] #把"大"加到name裡面
				i += 1
				break
			name += element[u"土地區段位置或建物區門牌"][i]
			i += 1
		if i!=len(element[u"土地區段位置或建物區門牌"])-1:
			name += element[u"土地區段位置或建物區門牌"][i]
		else : #i==len(element[u"土地區段位置或建物區門牌"])-1 表示這個路名中沒有包含任何的"大道""路" "街" "巷" 直接跳過
			continue
		#處理name
		#判斷有沒有出現過
		if road_by_key.has_key(name): #如果有存在 依據id 判斷交易年月是否為新的數值來更新year記錄表跟num記錄表
			id = road_by_key[name]
			if int(element[u"交易年月"]) not in year[id]:
				year[id].append(int(element[u"交易年月"]))
				num[id] += 1
				if num[id] == max_num:
					max_id.append(id)
				if num[id] > max_num:
					max_num = num[id]
					max_id = [] #清空
					max_id.append(id)
		else : #第一次出現 建立id 依據id更新year記錄表跟num記錄表
			#print "first", name, id_num
			road_by_key[name] = id_num
			road_by_value[id_num] = name
			year.append([]) #先將一般的陣列新增一個list物件
			year[id_num].append(int(element[u"交易年月"])) #再對新增的list做塞入元素的動作
			num[id_num] = 1
			id_num += 1
	max_id.sort() #使得多筆答案時，較先遇到的道路名稱較先被輸出
	i = 0 #計算個數 print需要
	for mid in max_id:
		highest = 0 #最高成交價
		lowest = 999999999 #最低成交價
		name = road_by_value[mid]
		for element in json_input:
			if name in element[u"土地區段位置或建物區門牌"]:
				if element[u"總價元"] > highest:
					highest = int(element[u"總價元"])
				if element[u"總價元"] < lowest:
					lowest = int(element[u"總價元"])
		#print 一定會在最後輸出空格
#		name += ","
#		if i == 0:
#			sys.stdout.write("\"")	#使用sys.stdout.write可以不輸出換行,不輸出空格
#		if i == len(max_id)-1:	#最後一筆答案的尾巴要有 " 符號
#			print name, "最高成交價:%d, 最低成交價:%d\"" % (highest,lowest)
#		else:
#			print name, "最高成交價:%d, 最低成交價:%d" % (highest,lowest)
#		i += 1