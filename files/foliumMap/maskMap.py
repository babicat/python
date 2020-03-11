# terminal > pip install requests
# terminal > pip install folium
import json
import requests
import folium
from time import gmtime, strftime

# address loading
# response = requests.get('https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json')

# geo loading
response = requests.get('https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByGeo/json')

datas = []
status = response.status_code
if status == 200 :
    text = response.text
    text_dict = json.loads(text)
    text_count = text_dict['count']
    text_stores = text_dict['stores']

    for temp in text_stores:
        t = {"name": temp['name'], "lat": temp['lat'], "lng": temp['lng'], "remain": temp['remain_stat']}
        datas.append(t)

# map start point
m = folium.Map(
    location = [37.5838699,127.0565831],
    zoom_start = 12
)

if 0 < len(datas):
    for idx in range(len(datas)):
        colorType = 'blue'
        if datas[idx]['remain'] == 'empty':
            colorType = 'red'

        folium.Marker(
            location = [datas[idx]['lat'], datas[idx]['lng']],
            popup = datas[idx]['remain'],
            tooltip = datas[idx]['name'],
            icon = folium.Icon(color=colorType, icon='star')
        ).add_to(m)


fileName = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
fileName += '.html'
m.save(fileName)
