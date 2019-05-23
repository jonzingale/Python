from pprint import pprint as pp
from pdb import set_trace as st
from books.models import Book # comment out when testing without server.
from lxml import html
import requests
import time
import re

BOOK_REGEX_ARY = ['Personal name','(Uniform|Main) title','LC classification',
                  'ISBN','Published']

USER_AGENT = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0)'}
LOC_URL = 'https://catalog.loc.gov/vwebv/'
NO_RESULTS = 'Your search found no results.'

BOOK_LINK = './/div[@class="search-results-list-description-item search-results-list-description-title"]/a'
ERROR_SEL = '//div[@class="error-container"]/h3/text()'
BOOK_VAL_SEL = './following-sibling::ul/li//span'
BOOK_DATA_SEL = './/span[@dir="ltr"]/text()'
HEAD_SEL = './/h3[@class="item-title"]'

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

def get_data_by_tag(tree, tag, datum=None):
  text_comparer = lambda x : re.findall(x[1], x[0].text)
  key_elems = tree.xpath(HEAD_SEL)

  for elem in key_elems:
    match_cond = text_comparer((elem, tag))
    if match_cond:
      datum = elem.xpath(BOOK_VAL_SEL)[0].text
      break
  return(datum)

def get_page(url, url_params=''):
  page = requests.get(url, params=url_params, headers=USER_AGENT)
  tree = html.fromstring(page.content)
  return (tree, page)

def parse_contents(page, tree): # should become method on page object.
  # if tree.xpath(ERROR_SEL): st()

  data = []
  for datum in BOOK_REGEX_ARY: data.append(get_data_by_tag(tree, datum))
  author, title, lccn, isbn, pub_created, *extras = data

  pub_year = re.findall('\d+',pub_created.split(',')[-1])[0]
  if isbn: isbn = int(isbn.split(' ')[0])
  else: isbn = 0
  if author: author = (',').join(author.split(',')[0:2])
  else: author = title.split('/')[1].strip()
  clean_author = re.match('edited by (.+)', author)
  if clean_author: author = clean_author.group(1)

  # Make Title Ascii clean
  title = title.split('/')[0].strip()
  clean_title = ''.join(e for e in title if e.isalnum() or e == ' ')

  book_data['title'] = clean_title[:200] # db len limit.
  book_data['author'] = author[:200]
  book_data['pub_year'] = int(pub_year)
  book_data['lccn'] = lccn
  book_data['isbn'] = isbn

def get_bookdata(page, tree):
  book_links = tree.xpath(BOOK_LINK)

  # If a list of possible books is returned.
  if book_links:
    book_stubs = []
    for book in book_links: # Remove sound recordings from query response.
      if not re.search('\[sound recording\]', book.text):
        book_stubs.append(book)

    book_stub = book_stubs[0].xpath('./@href')[0] # <-- Select more Cleverly.
    tree, page = get_page(LOC_URL + book_stub)

  parse_contents(page, tree)

def books_search(title='', tries=30):
  url_params['searchArg'] = title
  url = LOC_URL + 'search'

  while tries > 0:
    tree, page = get_page(url, url_params=url_params)

    error = tree.xpath(ERROR_SEL)

    if error and error[0] == NO_RESULTS:
      print(NO_RESULTS)
      break
    elif error: # No Connections Available
      print((error[0], tries))
      time.sleep(1)
      tries -= 1
    else:
      print('SUCCESSFUL LANDING')
      get_bookdata(page, tree)
      pp(book_data)
      bb = Book(**book_data)
      bb.save()
      break

def clean_title(title):
  clean_title = re.sub('^(the|a|an) ','',title.lower())
  return(clean_title)

def find_book(title='categories for the working mathematician'):
  title = clean_title(title)
  books_search(title)
