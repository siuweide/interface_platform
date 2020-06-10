import json
import requests

url = 'http://127.0.0.1:8001/accounts/login/'

data = {"username":"siuweide",
        "password":"123456"}

url1 = 'http://127.0.0.1:8001/api/get_event_list/?eid=1'
res = requests.post(url, data=data)
cookies = requests.utils.dict_from_cookiejar(res.cookies)
cookies = 'sessionid=' + cookies['sessionid']
print(cookies)
# cookies = {"Cookie":cookies}
# res = requests.get(url1, headers=cookies)
# print(res.text)