# -*- coding: utf-8 -*-
import requests
import os
import string
from bs4 import BeautifulSoup
from lxml import etree
import sys
import shutil


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
        self.m_name = str(name).strip('\n')

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
            'Cookie': '__utma=104082069.72684850.1493021797.1493023736.1493172406.3; __utmc=104082069; __utmz=104082069.1493021798.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
            'Host': 'docs.huihoo.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdc',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Proxy-Connection': 'keep - alive',
            'Upgrade-Insecure-Requests': '1',
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'http://docs.huihoo.com/jgroups/'}
        self.savePath = "D:\\test\\shiye\\userguide\\"
        self.imgPath = "D:\\test\\shiye\\userguide\\images\\"


def doDownLoad(url, path):
    print("enter doDownLoad: url is %s" % url)
    print("path is %s" % path)
    if isProxyNeeded:
        res = session.get(url, headers=setting.myHeaders, proxies=setting.proxy)
    else:
        res = session.get(url, headers=setting.myHeaders)
    if path != "":
        if res.status_code == 200:
            f = open(path, 'w+')
            f.write(res.content.decode('utf-8'))
            f.close()

    return res.content


def downloadpicture(url, path):
    print("enter downloadpicture: url is %s" % url)
    print("path is %s" % path)
    if isProxyNeeded:
        res = session.get(url, headers=setting.myHeaders, proxies=setting.proxy, stream=True)
    else:
        res = session.get(url, headers=setting.myHeaders, stream=True)
    if path != "":
        if res.status_code == 200:
            with open(path, 'wb') as f:
                res.raw.decode_content = True
                shutil.copyfileobj(res.raw, f)

#1. get result for key word search
print("1, get chapter list source")
wmp = AllData()
setting = NetWorkSetting()
session = requests.Session()

content = doDownLoad(setting.searchUrl, setting.savePath + "index.html")

soup = BeautifulSoup(content)

for link in soup.find_all('a'):
    if link.get('href') != "" and link.text != "" and str(link.get('href')).find(".html") != -1 and link.text != None:
        temp = link.get('href')
        temp = str(temp)

        if temp.find("#") == -1:
            eachChapter = Chapter()
            chapter_url = setting.prefixUrl + str(link.get('href'))
            eachChapter.setAddress(chapter_url)
            eachChapter.setName(str(link.get('href')))
            wmp.add_chapter(eachChapter)
        #else:
            #print("ignore : %s" % temp)

#2, makdir for docs
print ("2, makdir for docs")
if os.path.exists(setting.savePath):
    pass
else:
    os.makedirs(setting.savePath)
if os.path.exists(setting.imgPath):
    pass
else:
    os.makedirs(setting.imgPath)

#3, get all the chapters for docs
print ("3, get all the chapters for docs, if page contain picture, download it")
for chapter in wmp.m_chapters:
    newfilename = setting.savePath + chapter.m_name
    print ("newfilename is %s" % newfilename)

    pagecontent = doDownLoad(chapter.m_address, setting.savePath + chapter.m_name)
    soup = BeautifulSoup(pagecontent)
    for img in soup.find_all('img'):

        if img.get('src') != "" and img.get('src') != None and str(img.get('src')).find("latex2html") == -1:
            print("~~~~~~~~~~~~~~~~")
            print(img.get('src'))
            print("~~~~~~~~~~~~~~~~")
            imgname = str(img.get('src'))
            imgurl = setting.prefixUrl + imgname
            print(imgname)
            downloadpicture(imgurl, setting.imgPath + imgname)


print ("end of now")



