import requests
from lxml import etree
from pyquery import PyQuery as pq
import re

re_href = re.compile('href="([^"]*)"')

year = 2019
document = pq(filename='chi%d.html' % year)
html_link_list = document('a[name="FullTextHtml"]')

print(len(html_link_list))

href_list = []

for html in html_link_list:
  s = str(pq(html))
  # print(s)
  href_match = re_href.search(s)
  href = href_match.groups()[0]
  href_list.append(href)

with open('chi%d_href_list.txt' % year, 'w') as f:
  f.writelines('\n'.join(href_list))
