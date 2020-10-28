# -*- coding:utf-8 -*-
"""
author: zhou zhen
date:   2020/10/28

"""

import requests#导入网络请求库
import os# 导入文件操作库
from bs4 import BeautifulSoup#导入html处理库
import re#正则库
import pdfkit#用于html转pdf
pic_path='https://learnku.com/docs/pymotw'# 爬网页地址



res=requests.get(pic_path)
soup = BeautifulSoup(res.text, 'html.parser')
all_link=soup.findAll('a')
with open('out.txt','w') as f:#因为html编码原因,正则无法匹配,先将html转成txt匹配
    for href in all_link:
        f.write(str(href))
with open('out.txt','r') as f:
    lines=f.readlines()
    out_list=[]
    for line in lines:
        find_one = re.compile('<a\sclass=""\shref="(.*)">')#获取要爬的网页地址
        out=re.findall(find_one,line)
        if out!=[]:
            out_list.append(out)
options = {
        'page-size': 'A4',
        'margin-top': '0.1in',
        'margin-right': '0.1in',
        'margin-bottom': '0.1in',
        'margin-left': '0.1in',
        'encoding': "utf-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'cookie': [
            ('cookie-name1', 'cookie-value1'),
            ('cookie-name2', 'cookie-value2'),
        ],
        'outline-depth': 10,
        "dpi":196
    }

html_template = """ 
<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <meta charset="UTF-8"> 
</head> 
<body> 
{content} 
</body> 
</html> 

"""
def create_path():
    if not os.path.exists('pdf'):
        os.mkdir('pdf')#创建pdf文件夹
i=0
for out in out_list:
        res=requests.get(out[0])
        new_soup=BeautifulSoup(res.text,'html.parser')
        find_out=new_soup.find_all('div','extra-padding')
        find_out=str(find_out[0])
        html = html_template.format(content=find_out)
        html = html.encode("utf-8")
        with open('out.html', 'wb') as f:
            f.write(html)
        pdfkit.from_file('out.html', 'pdf/'+'out'+str(i)+'.pdf')
        i+=1
        os.remove('out.html')
