import requests
import json
url1 = 'http://127.0.0.1:8001/accounts/login/'
data = {"username":"siuweide","password":"123456"}
url = 'http://127.0.0.1:8001/api/get_event_list/'
headers = {"Cookie":"sessionid=405rwd5fiz8wbr8ifx94i0vbwau4mh8x"}

res = requests.post(url=url1,data=data)
cookies = res.cookies
res = requests.utils.dict_from_cookiejar(cookies)
print(res)
print(type(res))

res1 = requests.get(url=url,headers=headers)
result = json.dumps(res1)
print(result)