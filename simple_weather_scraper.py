from bs4 import BeautifulSoup as soup
from pdb import set_trace as st
from pprint import pprint as pp
import descarteslabs as dl
import urllib3
import os

NWS_URL = 'http://forecast.weather.gov/MapClick.php?lat=%s&lon=%s'
USER_AGENT = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}

# see descartes labs docs for places.find
def get_coords_url(place):
  dl_taos = dl.places.find(place)
  lat , lng = dl_taos[0]['bbox'][1:3]
  return(NWS_URL % (lat, lng))

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
  sf = get_santa_fe()

  # nws weather data
  temp = sf.find('p', class_='myforecast-current-lrg').text
  details = sf.find('div', id="current-conditions-body")

  data = {'Temp': temp}

  for tr in details.find_all('tr'):
    key, val = map(lambda x: x.text, tr.find_all('td'))
    data[key] = val.strip()

  pp(data)

main()
