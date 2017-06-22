from bs4 import BeautifulSoup as soup
from pdb import set_trace as st
from pprint import pprint as pp
import descarteslabs as dl
import urllib3
import lxml
import os
import re


lat_long = 'lat=35.6879&lon=-105.9447'

NWS_URL = 'http://forecast.weather.gov/MapClick.php?lat=%s&lon=%s'

USER_AGENT = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
NWS_HEADER = {'Accept' : 'application/vnd.noaa.dwml+xml;version=1'}

# see descartes labs docs for places.find
def get_coords_url(place):
  dl_taos = dl.places.find(place)
  lat, long = dl_taos[0]['bbox'][1:3]
  return(NWS_URL % (lat, long))

def get_santa_fe():
  santa_fe = get_coords_url('new-mexico_taos')
  return get_page(santa_fe)

def open_url(url):
  os_command = f"open {url}"
  os.system(os_command)

def get_page(url):
  agent = urllib3.PoolManager(10, headers=USER_AGENT)
  data = agent.request('GET', url).data
  return(soup(data, "html.parser"))

def post_form(url, params={}):
  agent = urllib3.PoolManager(10, headers=USER_AGENT)
  data = agent.request('POST', url, params).data
  return(soup(data, "html.parser"))

def main():
  # page = get_page(NWS_URL)
  # action = page.form['action']
  # agent = urllib3.PoolManager(10, headers=USER_AGENT)
  # action = 'http://forecast.weather.gov/zipcity.php'
  # headers = {'Accept' : 'application/vnd.noaa.dwml+xml;version=1'}
  # query = {'inputstring': '87501'}
  # print(agent.request('GET', action, fields=query, headers=headers).data)

  sf = get_santa_fe()

  # temp max and min
  temp_max = sf.find('p', class_='myforecast-current-lrg').text
  temp_min = sf.find('p', class_='myforecast-current-sm').text
  details = sf.find('div', id="current-conditions-body")

  data = {'High': temp_max, 'Low': temp_min}

  for tr in details.find_all('tr'):
    datum = map(lambda x: x.text, tr.find_all('td'))
    key, val = [*datum]
    data[key] = val.strip()

  pp(data)

main()