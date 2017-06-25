from pprint import pprint as pp
from pdb import set_trace as st
from lxml import html
import requests

# This module scrapes malaphors and snoclones,
# and then generating them via tensor flow neural net.

USER_AGENT = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0)'}

MALAPHOR_URL = 'https://malaphors.com/'
MALAPHOR_SEL = './/h1/a/text()'

SNOWCLONE_URL = 'http://knowyourmeme.com/memes/snowclone'
SNOWCLONE_SEL = './/h2[@id="notable-examples"]/../table//li/text()'

def get_page(url):
  page = requests.get(url, headers=USER_AGENT)
  tree = html.fromstring(page.content)
  return tree

# https://en.wiktionary.org/wiki/malaphor
# We'll burn that bridge when we come to it
def malaphor():
  tree = get_page(MALAPHOR_URL)
  datum, *data = tree.xpath(MALAPHOR_SEL)
  malaphors = [line.replace(u'\xa0',' ') for line in data]
  pp(malaphors)


# https://en.wikipedia.org/wiki/Snowclone
# I’m not an X, but I play one on TV
def snowclone():
  tree = get_page(SNOWCLONE_URL)
  data = tree.xpath(SNOWCLONE_SEL)
  snowclones = [line for line in data if not line == '\n']
  pp(snowclones)


malaphor()
print('\n')
snowclone()
