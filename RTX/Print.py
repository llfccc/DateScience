#encoding:utf-8       #设置编码方式  

import xlwt

#a=[1,2,3]
#b=[4,5,6]
#c=[[a,b] for a,b in zip(a,b)]
#print c



d=[['1','a','XXX'],['2','b','ooo'],['3','c','xoo'],['4','d','oox']]


w = xlwt.Workbook()     #创建一个工作簿
ws = w.add_sheet('Sheet1')     #创建一个工作表
for i in range(0,len(d),1):
    print i
    for j in range(0,len(d[0]),1):
        print j
        ws.write(i,j,d[i][j])    #在1行1列写入bit
       
        
w.save('mini.xls')     #保存
