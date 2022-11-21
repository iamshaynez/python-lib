import datetime
import time
import requests
from lxml import etree
import pandas as pd
import re

def response(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11'}
    resposn = requests.get(url=url, headers=headers).text
    return resposn

def process(url):
    resposn = response(url)
    etree_html = etree.HTML(resposn)

    # parse book page html
    book_title = etree_html.xpath('.//h1/span/text()')[0]
    img_small = etree_html.xpath('.//div/a[@class="nbg"]/img/@src')

    # span[contains(@class, 'myclass') and normalize-space(text()) = 'qwerty']

    book_info_test = etree_html.xpath('.//div[@id="info"]')
    
    reg = re.compile("<(.*?)>")
    book_info_result = reg.sub("", etree.tostring(book_info_test[0], encoding='UTF-8').decode('UTF-8'))
    book_info_result = re.sub(' +','', book_info_result)
    book_info_result = re.sub('\n+','\n', book_info_result)
    #print(book_info_result)

    # print my book list format
    print("### X. [《{0}》]({1}) ★★★★★".format(book_title, url))
    print("")
    print("```")
    print(book_info_result)
    print("```")
    print("")
    print("![]({0})".format(img_small[0]))

if __name__ == "__main__":
    url = 'https://book.douban.com/subject/30238120/'
    process(url)
    

