# -*- coding: utf-8 -*-
import re
import sys
import xlwt
reload(sys)
sys.setdefaultencoding('utf8')
import datetime
starttime = datetime.datetime.now()  #用来计算程序耗时
#long running

text=open('a.txt','r').read()   #读取源文件

##------正则表达式匹配部分 ------####
p =re.compile(r'/\*[\s\S]*?\*/')  ##找到所有/* 开头 ，*/结尾的内容
p0 =re.compile(r'\*/([\s\S]*?)/\*') ##找到所有*/ 开头 ，/*结尾的内容 ，并只取
p1=re.compile(r'([\x80-\xff]+\d*?) \([\x80-\xff]+\d*?\) 20\w\w-\w\w-\w\w \w\w:\w\w:\w\w') ##匹配名字和时间，取其中的名字
p2=re.compile(r'[\x80-\xff]+\d*? \([\x80-\xff]+\d*?\) (20\w\w-\w\w-\w\w \w\w:\w\w:\w\w)') ##匹配名字和时间，取其中的时间
p3=re.compile(r'[\x80-\xff]+\d*? \([\x80-\xff]+\d*?\) 20\w\w-\w\w-\w\w \w\w:\w\w:\w\w\n') ##匹配名字和时间，分割出剩余部分即对话内容

##------将文本内容拆成/*   */ 与下面的对话2部分 并存放成2个字符串组FirstPart（备注部分），LastPart（对话内容）###
FirstPart=re.findall(p,text) #找到符合/* */的所有内容,保存为提示部分FirstPart列表
LastPart=re.findall(p0,text) #查找/* */来分割开来，保存剩下的对话部分为LastPart列表
#本来用LastPart=re.split(p,text,re.MULTILINE)，发现re.split只能分隔成9部分，故放弃

while '' in LastPart:    #删掉split出来的所有空字符，不知道哟见没有用
    LastPart.remove('')

if len(FirstPart)!=len(LastPart):
    print "Len is not equal"

listL=[]
d=[]   #将a,b,c数组合成一个d数组
#result=[['' for x in range(12)] for y in range(1000)] #将所有结果存入result数组
##------处理主题提示部分 ------####
for n in range(0,len(LastPart),1):   # for n in range(0,len(LastPart),1):

    for i in ('/*','主 题','创建时间','创建者','参与者','*/'):
        FirstPart[n] = FirstPart[n].replace(i,'ox2o')  #通过统一替换不同的分隔符来一次性分割开语句
        FirstPart[n] = FirstPart[n].replace("：",'')   #删除“主 题：”
    listL.append(FirstPart[n].split('ox2o'))

    ##------处理对话部分 ------####
    temp=LastPart[n]
    a=re.findall(p1,temp) #取名字
    b=re.findall(p2,temp) #取其中的时间
    c=re.sub(p3,'ox3o',temp) #取对话内容
    c=c.strip()   #忘了有啥用了，但是有用
    c=c.split("ox3o",)

    while '' in c:    #删掉split出来的所有空字符
        c.remove('')
    ##---因为备注部分只出现一次，故用循环将每一句对话都配合上备注部分，组成一条完整的对话内容，包括所有部分--##
    if len(a)==len(b) and len(b)==(len(c)):
        for i in range(0,len(a),1):
            d.append(listL[n]  +[a[i],b[i],c[i]])
    elif len(a)==len(b) and len(b)==(len(c))-1:
        for i in range(0,len(a),1):
            d.append(listL[n]  +[a[i],b[i],c[i+1]])

 ##---sortlist函数使用迭代删除重复的列表,不影响排序，网上抄来的---##
def sortlist(list0):
    listTemp=[]
    for i in list0:
        if not i in listTemp:
            listTemp.append(i)
    return listTemp

#d=sortlist(d)  #删除d列表中的重复项

##---将结果写入excel文件，保存为results.xls的sheet1表   ---##
w = xlwt.Workbook()     #创建一个工作簿
ws = w.add_sheet('Sheet1')     #创建一个工作表
for i in range(0,len(d),1):     #外循环，d[i]代表每一条完整的记录，包括主题、参与者、对话内容等
    for j in range(0,len(d[0]),1):  #内循环，d[i][j]代表每一条完整记录中某一列的内容
       ws.write(i+1,j,d[i][j].decode())    #在i行j列写入d[i][j]，用decode（）来变成中文

w.save('results.xls')     #保存

endtime = datetime.datetime.now()
print "It has taken",(endtime - starttime).seconds,"s"

##导出中间文件，测试用的，不需要了
#fl=open('list.txt', 'w')
#for i in LastPart:
#    fl.write(i)
#    fl.write("\n")
#fl.close()
#
#f2=open('list2.txt', 'w')
#
#for i in FirstPart:
#    f2.write(i)
#    f2.write("\n")
#f2.close()
