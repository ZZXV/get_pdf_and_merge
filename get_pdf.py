# -*- coding:utf-8 -*-
"""
author: zhou zhen
date:   2020/10/28

"""

import requests  # 导入网络请求库
import os  # 导入文件操作库
from bs4 import BeautifulSoup  # 导入html处理库
import re  # 正则库
import pdfkit  # 用于html转pdf
import PyPDF4

pic_path = 'https://learnku.com/docs/pymotw'  # 爬网页地址

res = requests.get(pic_path)
soup = BeautifulSoup(res.text, 'html.parser')
all_link = soup.findAll('a')
with open('out.txt', 'w') as f:  # 因为html编码原因,正则无法匹配,先将html转成txt匹配
    for href in all_link:
        f.write(str(href))
with open('out.txt', 'r') as f:
    lines = f.readlines()
    out_list = []
    for line in lines:
        find_one = re.compile('<a\sclass=""\shref="(.*)">')  # 获取要爬的网页地址
        out = re.findall(find_one, line)
        if out != []:
            out_list.append(out)
os.remove('out.txt')
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
    'outline-depth': 30,
    "dpi": 196
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
        os.makedirs('pdf')  # 创建pdf文件夹

create_path()
i = 0  # 生成文件名
for out in out_list:
    res = requests.get(out[0])
    new_soup = BeautifulSoup(res.text, 'html.parser')
    find_out = new_soup.find_all('div', 'extra-padding')  # 获取要转成pdf的内容
    find_out = str(find_out[0])
    html = find_out
    html = html_template.format(content=find_out)
    html = html.encode("utf-8")
    with open('out.html', 'wb') as f:
        f.write(html)
    pdfkit.from_file('out.html', 'pdf/' + 'out' + str(i) + '.pdf',options=options)  # html转pdf
    i += 1
    os.remove('out.html')

def sort_key(name):#按名称排序文件合并
    return int(re.findall(r'(\d+)',name)[0])
files=os.listdir('pdf')
files.sort(key=lambda x:sort_key(x))
pdf_all=PyPDF4.PdfFileMerger()
for file in files:#合并文件
    pdf_all.append('pdf/'+file)
pdf_all.write('pdf_all.pdf')
pdf_all.close()
