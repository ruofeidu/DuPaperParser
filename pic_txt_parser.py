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


year = 2019
start = 0
end = 695
download_image = False
write_title = False
# start = 624
# end = 624
# download_image = True

lines = None
with open('chi%d_href_list.txt' % year, 'r') as f:
  lines = f.readlines()

for i, url in enumerate(lines):
  if i < start or i > end:
    continue
  print(i)
  with open('chi%d_raw/%d.html' % (year, i), 'r') as f:
    contents = f.readlines()
  s = ''.join(contents)

  if write_title:
    title = BeautifulSoup(s, 'lxml').title.string
    with open('chi%d_data/%d.title' % (year, i), 'w') as f:
      f.write(title)

  ac_list = re_access.findall(s)
  for j, ac in enumerate(ac_list):
    pic_url = ac[0]
    pic_desc = BeautifulSoup(ac[1], 'lxml').text
    pic_cap = BeautifulSoup(ac[2], 'lxml').text
    suffix = file_extension(pic_url)

    if download_image:
      print(pic_url)
      print(pic_desc)
      print(pic_cap)
      image = get_content(pic_url, header)
      with open('chi%d_data/%d_%d%s' % (year, i, j, suffix), 'wb') as f:
        f.write(image)
      with open('chi%d_data/%d_%d.txt' % (year, i, j), 'w') as f:
        f.write(pic_desc)
      with open('chi%d_data/%d_%d.cap' % (year, i, j), 'w') as f:
        f.write(pic_cap)

    else:
      # try:
      #   os.rename('chi%d_data/%d_%d.%s' % (year, i, j, suffix),
      #             'chi%d_data/%d_%d%s' % (year, i, j, suffix))
      # except:
      #   print('chi%d_data/%d_%d.%s was not found.' % (year, i, j, suffix))
      #   pass
      pass
