# -*- coding: utf-8 -*-
import os
import string
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

folderName = "dahuangmanshen//"

if os.path.exists(folderName + "target"):
    pass
else:
    os.makedirs(folderName + "target")

index = 1
isRuning = True
while isRuning:
    filename = folderName + str(index) + ".html"
    if os.path.exists(filename):
        f1 = filename
        f2 = folderName + "target//" + str(index) + ".html"
        with open (f2,'w') as ff2:
            with open(f1,'r') as ff1:
                for x in ff1:
                    if x.find("var next_page") != -1 :
                        x = "var next_page = " + '"' + str(index + 1) + ".html" + '"' + ";\n"

                    if x.find("var preview_page") != -1 :
                        x = "var preview_page = " + '"' + str(index - 1) + ".html" + '"' + ";\n"

                    ff2.write(x)
    else:
        isRuning = False
    index += 1


