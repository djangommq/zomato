import requests
import json
import csv
import os

# location去重列表
has_loc=[]

info_list=[
    "place_id",
    "place_type",
    "place_name",
    "subzone_id",
    "city_name",
    "city_id",
    "real_city_name",
    "delivery_subzone_id",
    "delivery_subzone_name",
    "delivery_subzone_id"
]


place_info_headers=[
    "lat",
    "lng",
    "place_id",
    "place_type",
    "place_name",
    "subzone_id",
    "city_name",
    "city_id",
    "real_city_name",
    "delivery_subzone_id",
    "delivery_subzone_name",
    "delivery_subzone_id"
]

# 通过经纬度获取地区信息
def get_place_info(lat,lng):
    url = "https://api.zomato.com/v2/deliverygeocode.json"
    querystring = {
                   "lat":lat,
                   "lon":lng,
                   "uuid":"c3eced96-bdb3-4471-b9f0-f89fc8ed7650",
                   "lang":["zh","zh"],
                   "android_language":["zh","zh"],
                   "android_country":["CN","CN"]
                }
    payload = ""
    headers = {
        'X-Zomato-App-Version-Code': "5610001",
        'Akamai-Referrer': "com.application.zomato.ordering/5.6.1-release [c2f5165]",
        'X-Jumbo-Session-Id': "f0c0e2fb-ce42-4b6d-9a6a-49f2bdd006c31541649019",
        'X-Zomato-API-Key': "e74fd9cf3dd6408f97cddf52a2d673bf",
        'X-App-Language': "&lang=zh&android_language=zh&android_country=CN",
        'X-Access-UUID': "0e9248ba-472e-49e0-86a4-8b8b38c3520d",
        'X-Zomato-App-Version': "561",
        'X-Network-Type': "wifi",
        'X-Present-Long': "55.300432997143986",
        'X-Zomato-UUID': "c3eced96-bdb3-4471-b9f0-f89fc8ed7650",
        'X-O2-City-Id': "51",
        'User-Agent': "&source=android_market&version=5.0.2&device_manufacturer=HUAWEI&device_brand=HONOR&device_model=PLK-TL01H&app_type=android_ordering",
        'X-Device-Pixel-Ratio': "3.0",
        'X-Access-Token': "",
        'X-Installer-Package-Name': "com.android.vending",
        'X-City-Id': "51",
        'X-Device-Width': "1080",
        'Akamai-Mobile-Connectivity': "type=wifi;v=tpv1;tpresult=2;appdata=com.application.zomato.ordering;prepositioned=true;websdk=18.4.2;devicetype=3;rwnd=2097152;optimization=transport",
        'X-Client-Id': "zomato_android_v2",
        'X-Present-Lat': "25.247883735592705",
        'Accept': "image/webp",
        'X-Device-Height': "1794",
        'Host': "api.zomato.com",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'cache-control': "no-cache",
        'Postman-Token': "1275044b-9c71-468f-aad4-0229fb3a8601"
        }

    try:
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring,timeout=2)
        # 解析数据
        parse_info(lat, lng, response.text)
    except TimeoutError as e:
        error_log(str(lat)+','+str(lng)+'请求超时')
    except Exception as e:
        error_log(str(lat)+','+str(lng)+'请求发生其他错误')


# 数据解析
def parse_info(lat,lng,place_info):
    placeinfo_dict=json.loads(place_info)
    if placeinfo_dict['status'] == 'success':
        # place
        placeinfo_place=placeinfo_dict['place']
        placeinfo_dict=dict(placeinfo_dict,**placeinfo_place)

        # 地区信息保存
        save_place_info(lat,lng,placeinfo_dict)


# 地区信息的保存
def save_place_info(lat,lng,placeinfo_dict):
    place_info={}
    place_info['lat']=lat
    place_info['lng']=lng
    for h in info_list:
        place_info[h]=placeinfo_dict[h]

    if place_info['place_info'] in has_loc:
            return
    filename=os.path.join(os.path.dirname(__file__),'input_data/location.csv')
    if not os.path.exists(filename):
        with open(filename,'w',encoding='utf-8',newline='')as f:
            writer=csv.DictWriter(f,fieldnames=place_info_headers)
            writer.writeheader()

    with open(filename,'a',encoding='utf-8',newline='')as f:
        writer=csv.DictWriter(f,fieldnames=place_info_headers)
        writer.writerow(place_info)

    has_loc.append(place_info['place_info'])

# 错误日志
def error_log(error_str):
    logname = os.path.join(os.path.dirname(__file__), 'input_data/error_log.txt')
    with open(logname,'a',encoding='utf-8')as f:
        f.write(error_str+'\n')


if __name__ == '__main__':
    lat_top_left = 25.375272
    lng_top_left = 54.849978
    lat_bottom_right = 24.612031
    lng_bottom_right = 55.722834

    i = lat_bottom_right
    while i < lat_top_left:
        j = lng_top_left
        while j < lng_bottom_right:
            lat = i
            lng = j
            print('请求:'+str(lat)+','+str(lng))
            get_place_info(lat,lng)
            j+=0.01
        i+=0.01