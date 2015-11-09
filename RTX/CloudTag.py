# -*- coding: utf-8 -*-

import sys
import random

import pytagcloud
from operator import itemgetter
from pytagcloud import create_tag_image, make_tags
reload(sys)
sys.setdefaultencoding('utf8')   #使用utf-8处理字符

import re
k = {}
#tag.txt，每一行为词语、‘\t’、数字，这种格式
def openFile():
    return {k.strip().decode("gbk"):int(v.strip()) for k, v in (l.split('\t') for l in open("tag.txt"))}
k=openFile()
from operator import itemgetter
swd = sorted(k.iteritems(), key=itemgetter(1), reverse=True)
swd = swd[1:60]
print swd
tags = make_tags(swd,10,80)
create_tag_image(tags,'tag_cloud.png',background=(255, 255, 255, 255), size=(860, 600),fontname="simhei")
