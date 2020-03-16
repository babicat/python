# terminal > pip install requests
# terminal > pip install folium
import json
import requests
import folium
from time import gmtime, strftime

# address loading
# response = requests.get('https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByAddr/json')
# geo loading
# 까치산역 37.5317675,126.8467055
response = requests.get('https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/storesByGeo/json?lat=37.5317675&lng=126.8467055&m=5000')

# map start point
m = folium.Map(
    location = [37.5317675,126.8467055],
    zoom_start = 12
)

datas = []
status = response.status_code
if status == 200 :
    text = response.text
    text_dict = json.loads(text)
    text_count = text_dict['count']
    text_stores = text_dict['stores']

    for temp in text_stores:
        if "remain_stat" in temp:
            colorType = 'blue'
            if temp['remain_stat'] == 'empty':
                colorType = 'red'
            elif temp['remain_stat'] == 'break':
                colorType = 'red'
            elif temp['remain_stat'] == None:
                colorType = 'red'

            folium.Marker(
                location = [temp['lat'], temp['lng']],
                popup = temp['remain_stat'],
                tooltip = temp['name'],
                icon = folium.Icon(color=colorType, icon='star')
            ).add_to(m)
       
fileName = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
fileName += '.html'
m.save(fileName)
