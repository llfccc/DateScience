# -*- coding: utf-8 -*-
import re
import sys
import datetime
import xlwt
reload(sys)
sys.setdefaultencoding('utf8')   #使用utf-8处理字符
starttime = datetime.datetime.now()  #用来计算程序耗时

#读取源文件a.ini和载入用户字典

text=open('a.ini','r').read()
#jieba.load_userdict("userdict.txt")
##------正则表达式匹配部分 ------####

p =re.compile(r'/\*[\s\S]*?\*/')  ##找到所有/* 开头 ，*/结尾的内容（即主题提示部分）
p0 =re.compile(r'\*/([\s\S]*?)/\*') ##找到所有*/ 开头 ，/*结尾的内容 ，并只取部分内容，（即对话内容部分）
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

listL=[] #储存主题提示部分
d=[]   #将a,b,c数组合成一个d数组，d[]代表对话内容部分
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

d=sortlist(d)  #删除d列表中的重复项

##---分词统计---###
import jieba
#jieba.load_userdict("userdict.txt")  #载入自定义用户词典

#因对话内容处于d[][9]处，故对其用jieba的lcut分为列表
#测试用的数据d=[['','','zhuti','faqiren','canyuzhe','shijian','','llf','2015-3-1 19:00:00','中文狗在此报道/tx~/tx~ \/ll'],['','','zhuti','faqiren','canyuzhe','shijian','','llf','2015-3-1 19:00:00','bu dong le ba,na jiu kan ba s\ll \cy']]
for c in range(0,len(d),1):  #将聊天记录分词为一个列表，然后存放在原来的地方
    try:
        seg_list = list(jieba.cut(d[c][9])) #默认是精确模式,用list（）来转换迭代器为列表
        seg_list2= " ".join(seg_list)
        d[c].append(seg_list2)  #储存分词后的内容为字符串
        d[c].append(seg_list)  # 储存分词后的分词为一个列表，成为3维列表
    except:
        print d[c][8].encode('gbk')


##--统计词频并写入到jieguo.ini--##
word_lst = []
word_dict = {}
with open("jieguo.ini",'w') as f2:
    for line in d:    #取d的每一行
        for j in line[11]: #取d数组每一行的第12个元素，即分词后的列表seg_list，j为每一个分词后的词组
            word_lst.append(j)

    for item in word_lst:   #对每一个词组进行计数
        if item.strip() not in "，, \ / ！。“”" :   #不计特殊符号的数量
            if item not in word_dict:
                word_dict[item] = 1
            else :
                word_dict[item] += 1
    for key in word_dict:  #写入jieguo.ini文件
       f2.write(key+'  '+str(word_dict[key]))
       f2.write('\r\n')

#---将结果写入excel文件，保存为results2.xls的sheet1表   ---##
w = xlwt.Workbook()     #创建一个工作簿
ws = w.add_sheet('Sheet1')     #创建一个工作表
for i in range(0,len(d),1):     #外循环，d[i]代表每一条完整的记录，包括主题、参与者、对话内容等
    for j in range(0,len(d[0])-1,1):  #内循环，d[i][j]代表每一条完整记录中某一列的内容
        ws.write(i+1,j,d[i][j].decode())    #在i行j列写入d[i][j]，用decode（）来变成中文

w.save('results.xls')     #保存

##--程序结束，计算程序耗时--##
endtime = datetime.datetime.now()
print "\nThe End.It has taken",(endtime - starttime).seconds,"s"
