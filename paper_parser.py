import requests
from lxml import etree
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import re

prefix = 'https://dl.acm.org/'
header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
}


def get_soup(url, header):
  return BeautifulSoup(requests.get(url, headers=header).content, 'html.parser')


def get_content(url, header):
  return requests.get(url, headers=header).content


lines = None
with open('href_list.txt', 'r') as f:
  lines = f.readlines()
for i, url in enumerate(lines):
  url = prefix + url
  print(url)
  content = get_content(url, header)
  with open('raw/%d.html' % i, 'wb') as f:
    f.write(content)
  print("%d / %d" % (i, len(lines)))
