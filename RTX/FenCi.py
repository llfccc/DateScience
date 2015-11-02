#encoding=utf-8
import sys  
reload(sys)  
#sys.setdefaultencoding('utf-8')

import jieba
#jieba.load_userdict("userdict.txt")  #载入自定义用户词典

d=[['2','b','ooo'],['3','c','xoo'],['4','d','hello 最厉害的hero，超人T恤']]
for c in range(0,len(d),1):  #将聊天记录分词为一个列表，然后存放在原来的地方
    d[c][2] = jieba.lcut(d[c][2])  # 分词
print d    

##--统计词频--##
word_lst = []
word_dict = {}
with open("result.txt","r") as f1 ,open("jieguo.txt",'w') as f2:
   for line in f1:
       word_lst.append(line.split(','))
   for item in word_lst:
       for item2 in item:
           if item2.strip() not in "，！。“”" :
               if   item2 not in word_dict:
                   word_dict[item2] = 1
               else :
                   word_dict[item2] += 1
   for key in word_dict:
       print key,word_dict[key]
       f2.write(key+' '+str(word_dict[key]))
       f2.write('\r\n')
