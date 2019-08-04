#!/usr/bin/env python 3.5
# -*- coding: utf-8 -*-
# @Time    : 2019/8/4 16:57
# @Author  : wkend
# @File    : crawl.py
# @Software: PyCharm

import requests
from lxml import etree  # xpath
from wordcloud import WordCloud
import PIL.Image as image  # 引入读取图片的工具
import numpy as np
import jieba  # 分词


def getPage(url):
    """获取HTML源代码"""
    headers = {
        "User - Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64)"
                        "AppleWebKit / 537.36(KHTML, likeGecko) "
                        "Chrome / 75.0.3770.100Safari / 537.36"
    }

    response = requests.get(url, headers=headers).text
    return response


def all_page():
    """循环获取所有页面的url"""
    base_url = "https://movie.douban.com/subject/26794435/comments?start"
    # 列表存放所有的网页，共10页
    urllist = []
    for page in range(0, 200, 20):
        allurl = base_url + str(page)
        urllist.append(allurl)
    return urllist


def parse_page():
    """解析网页"""
    all_comment = []  # 列表存放所有的短评
    number = 1
    for url in all_page():
        # 初始化
        html = etree.HTML(getPage(url))
        # 短评
        comment = html.xpath("//div[@class='comment']//p/span/text()")
        all_comment.append(comment)
        print("第" + str(number) + "页解析并保存成功")
        number += 1
    return all_comment


def save_txt():
    """保存到本地"""
    result = parse_page()
    for i in range(len(result)):
        with open("哪吒短评集.txt", "a+", encoding="utf-8") as f:
            f.write(str(result[i]) + '\n')  # 按行存储每一页的数据


def trans_CN(text):
    """将爬取的文档进行分词"""
    word_list = jieba.cut(text)
    result = " ".join(word_list)  # 用空格分割每个分词
    return result


def get_word_cloud():
    """制作词云"""
    path_txt = "哪吒短评集.txt"  # 文档
    path_jpg = "1.jpg"  # 词云形状图片
    path_font = "C:\\Windows\\Fonts\\msyh.ttc"  # 字体

    text = open(path_txt, encoding='utf-8').read()
    # 剔除无关字
    irrelevant_words = ["真的", "什么", "但是", "而且", "那么", "就是", "可以",
                        "不是", "觉得", "还是", "本来", "不要", "不想", "哪里",
                        "一种","其实","今天","这部","你们","哈哈","更是","包括",
                        "因为","本片","总体","有人","暑期","这么","部分","只要","出来","尤其",]
    for irrelevant_word in irrelevant_words:
        text = text.replace(irrelevant_word, "")



    text = trans_CN(text)
    mask = np.array(image.open(path_jpg))  # 词云图案

    wordcloud = WordCloud(
        background_color='white',
        mask=mask,
        scale=15,
        max_font_size=80,
        font_path=path_font
    ).generate(text)

    wordcloud.to_file('哪吒评论词云.jpg')


if __name__ == '__main__':
    save_txt()
    print('所有页面保存成功')
    get_word_cloud()
    print('词云图制作成功')
