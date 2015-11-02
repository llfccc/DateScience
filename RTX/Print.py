#encoding:utf-8       #设置编码方式  

import xlwt

d=[['1','a','XXX'],['2','b','ooo'],['3','c','xoo'],['4','d','oox']]
##---将结果写入excel文件，保存为results.xls的sheet1表   ---##
w = xlwt.Workbook()     #创建一个工作簿
ws = w.add_sheet('Sheet1')     #创建一个工作表
for i in range(0,len(d),1):     #外循环，d[i]代表每一条完整的记录，包括主题、参与者、对话内容等
    print i
    for j in range(0,len(d[0]),1):  #内循环，d[i][j]代表每一条完整记录中某一列的内容
        print j
        ws.write(i,j,d[i][j])    #在i行j列写入d[i][j]
 
w.save('results.xls')     #保存