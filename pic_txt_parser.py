import requests
from lxml import etree
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import re
import os

prefix = 'https://dl.acm.org/'
header = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
}

re_access = re.compile(
    '<img\s+src="([^"]*)"\s+class="[^"]*"\s+alt="[^"]*"\s+longdesc="([^"]*)".*?class="figure-title">(.*?)<\/span>'
)


def get_soup(url, header):
  return BeautifulSoup(requests.get(url, headers=header).content, 'html.parser')


def get_content(url, header):
  return requests.get(url, headers=header).content


def file_extension(path):
  return os.path.splitext(path)[1]


lines = None
with open('href_list.txt', 'r') as f:
  lines = f.readlines()

start = 98
end = 150

for i, url in enumerate(lines):
  if i < start or i > end:
    continue
  with open('raw/%d.html' % i, 'r') as f:
    contents = f.readlines()
  s = ''.join(contents)
  ac_list = re_access.findall(s)
  for j, ac in enumerate(ac_list):
    pic_url = ac[0]
    pic_desc = BeautifulSoup(ac[1], 'lxml').text
    pic_cap = BeautifulSoup(ac[2], 'lxml').text
    print(pic_url)
    print(pic_desc)
    print(pic_cap)
    suffix = file_extension(pic_url)
    image = get_content(pic_url, header)
    with open('data/%d_%d.%s' % (i, j, suffix), 'wb') as f:
      f.write(image)
    with open('data/%d_%d.txt' % (i, j), 'w') as f:
      f.write(pic_desc)
    with open('data/%d_%d.cap' % (i, j), 'w') as f:
      f.write(pic_cap)
