from pprint import pprint as pp
from pdb import set_trace as st
from lxml import html
import requests

LOC_URL = 'https://catalog.loc.gov/vwebv/'
USER_AGENT = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0)'}

BOOK_SEL = './/div[@class="search-results-list-description-item search-results-list-description-title"]/a/@href'
BOOK_DATA_SEL = './/span[@dir="ltr"]/text()'

book_data = {'title' : '',
             'author' : '',
             'lccn' : '',
             'isbn' : '',
             'pub_year' : 0}

url_params = {'searchArg' : '',
              'searchCode' : 'GKEY^*',
              'searchType' : '1',
              'limitTo' : 'none',
              'fromYear' : '',
              'toYear' : '',
              'limitTo' : 'LOCA=all',
              'limitTo' : 'PLAC=all',
              'limitTo' : 'TYPE=all',
              'limitTo' : 'LANG=all',
              'recCount' : '25'
              }

def get_page(url, url_params=''):
  page = requests.get(url, params=url_params, headers=USER_AGENT)
  tree = html.fromstring(page.content)
  return (tree, page)

def parse_contents(tree):
  data = tree.xpath(BOOK_DATA_SEL)
  book_data['title'] = data[1].split('/')[0].strip()
  book_data['author'] = (',').join(data[0].split(',')[0:2])
  book_data['lccn'] = data[7]
  book_data['isbn'] = int(data[5])
  book_data['pub_year'] = int(data[7].split(' ')[-1])

def books_search(title=''):
  url_params['searchArg'] = title
  tree, page = get_page(LOC_URL+'search', url_params=url_params)

  book_stub = tree.xpath(BOOK_SEL)[0]
  tree, page = get_page(LOC_URL + book_stub)
  parse_contents(tree)

books_search('categories for the working mathematician')
pp(book_data)
