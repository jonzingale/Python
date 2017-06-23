from pdb import set_trace as st
from lxml import html
import requests

page = requests.get('http://www.weathercurrents.org')
tree = html.fromstring(page.content)

weathercurrents = tree.xpath('//span/text()')[-1]

print(weathercurrents)

