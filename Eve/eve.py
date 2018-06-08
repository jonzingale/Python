import requests
import json
from pprint import pprint
from pdb import set_trace as st

UrlN = 10**7 + 2
GoodID = 34

BASE_URL = 'https://esi.tech.ccp.is/latest'
FULL_URL = BASE_URL + "/markets/10000002/orders"

resp = requests.get(FULL_URL,params={"type_id":GoodID})

def pp(resp): pprint(resp.json())

pp(resp)
st()