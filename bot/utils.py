import json

import yfinance as yf
import requests

base = "https://api.groupme.com/v3"
end = "?token=85w8CudYavVwkN7YAdOQwSyzXyCYDx7SV9aLBoRL"

def get_members(group):
    mid = f"/groups/{group}"
    response = requests.get(base+mid+end)
    members = response.json()["response"]["members"]
    return members

def get_id(group, user):
    members = get_members(group)
    result = list(filter(lambda x: int(x['user_id']) == int(user), members))
    return result[0]['id']

def evan_voyager():
    stock = yf.Ticker("VYGVF")
    info = stock.info
    price = float(info['currentPrice'])
    d = (price - 16) * 300
    t = "made" if d > 0 else "lost"
    d = round(abs(d),2)
    return f"Evan has {t} ${d} from Voyager."

def remove_user(group, id):
    mid = f"/groups/{group}/members/{id}/remove"
    data = {"membership_id":id}
    requests.post(base+mid+end,data=json.dumps(data))

#print(get_members(69502628))