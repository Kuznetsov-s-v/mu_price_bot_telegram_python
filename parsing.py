import requests
import json
r = requests.get('http://api.exchangeratesapi.io/v1/latest'
                 '?access_key=879f9633d045e852b4509ff3ecbb0bab'
                 # '&base=RUB'
                 '&symbols=USD,EUR,CNY,RUB')
value = json.loads(r.content)
result = value['rates']

base = result['RUB']
USD = 1/(base/result['USD'])
EUR = 1/base
CNY = 1/(base/result['CNY'])
RUB = 1