#RTX聊天记录数据规整
##目的
对腾讯通聊天记录内容整理成表格形式以便后期作分析
## 使用说明
1. 主程序  main.py
2. 数据 a.ini (在文本最后手动加入了/*,为了findall能找到文件）
3. 使用分词器
## 测试问题
1. 异常处理薄弱，如果出现意外字符串可能崩溃
2. 效能不高，处理一个5M的纯文本，如果不去重需要11秒，去重后需要33秒，故可对去重算法进行优化，或者整体结果进行变更，考虑采取readline()一行行来读取，对每一行做逻辑判断不知道会不会快一些
## 学习目标
* 学习如何用python写入Excel表格指定位置
* 学习如何用JieBa分词和统计词频
* 学习数据分析
* 学习使用GitHub的使用，包括分支管理等

##学到的内容
1. 正则表达式的使用（正则中括号代表取匹配的括号部分）
2. 

主要通过此项目练习正则表达式，学习python字符串和数组的使用方式
##碰到的问题
1. re.split()只支持分割为9个部分，后采用re.findall()替代
2. 编码问题：ascii utf-8 gkb交织，导致输出不对或者运行不过去，需采用decode()和encode()。并且把a.ini的格式转换为utf-8无bom格式
3. 待补充
