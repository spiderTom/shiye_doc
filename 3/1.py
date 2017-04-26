# -*- coding: utf-8 -*-
import requests
import os
import string
from bs4 import BeautifulSoup
from lxml import etree
import sys


#reload(sys)
#sys.setdefaultencoding('utf-8')
isProxyNeeded = True


class AllData:
    def __init__(self):
        self.m_chapters = []

    def add_chapter(self, chapter):
        self.m_chapters.append(chapter)

class Chapter:
    def __init__(self, name= "", address = ""):
        self.m_name = name
        self.m_address = address

    def setName(self, name):
        self.m_name = name

    def setAddress(self, address):
        self.m_address = address


class NetWorkSetting:
    def __init__(self):
        self.proxy = {
            "http": 'http://10.144.1.10:8080',
            "https": 'https://10.144.1.10:8080'}
        self.searchUrl = 'http://docs.huihoo.com/jgroups/2.0/user-guide/'
        self.prefixUrl = 'http://docs.huihoo.com/jgroups/2.0/user-guide/'
        self.myHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://docs.huihoo.com/jgroups/'}
        self.savePath = "D:\\test\\shiye\\userguide"

#1. get result for key word search
print ("1, get chapter list source")
wmp = AllData()
setting = NetWorkSetting()
session = requests.Session()

if isProxyNeeded:
    result = session.get(setting.searchUrl, headers=setting.myHeaders, proxies=setting.proxy)
else:
    result = session.get(setting.searchUrl, headers=setting.myHeaders)
print (result.url, result.status_code)

soup = BeautifulSoup(result.content)

record = []

for link in soup.find_all('a'):
    if link.text != None and link.get('HREF') != "":
        print(link.text)
        print(link.get('href'))
        temp = link.get('href')
        temp = str(temp)

        if temp != None:
            if temp in record:
                pass
            else:
                record.append(temp)
                print("target : %s" % temp)
                eachChapter = Chapter()
                chapter_url = setting.prefixUrl + str(link.get('href'))
                eachChapter.setAddress(chapter_url)
                eachChapter.setName(link.text + ".html")
                wmp.add_chapter(eachChapter)
    else:
        print(link)

#2, makdir for docs
print ("2, makdir for xiaoshuo")
if os.path.exists(setting.savePath):
    pass
else:
    os.makedirs(setting.savePath)

#3, get all the chapters for docs
print ("3, get all the chapters for xiaoshuo")
index = 1
for chapter in wmp.m_chapters:
    print(chapter.m_name.strip('\n'))
    chapter.m_name = chapter.m_name.strip('\n')
    if ".html" == chapter.m_name:
        continue
    newfilename = setting.savePath + "\\" + str(index) + "_"+ chapter.m_name
    index += 1
    print ("newfilename is %s" % newfilename)
    if os.path.exists(newfilename):
        pass
    else:
        if isProxyNeeded:
            result = session.get(chapter.m_address, headers=setting.myHeaders, proxies=setting.proxy)
        else:
            result = session.get(chapter.m_address, headers=setting.myHeaders)

        if result.status_code == 200:
            f = open(newfilename,'w+')
            f.write(result.content.decode('utf-8'))
            f.close()

print ("end of now")



