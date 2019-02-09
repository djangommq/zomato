import requests
import json
import csv
import os
from urllib.parse import urlencode
import time
location_fields=[
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

rest_fields=[
        "id",
        "res_id",
        "cost_for_two_multiplier",
        "delivery_subzone_id",
        "name",
        "address",
        "locality",
        "city",
        "city_id",
        "latitude",
        "longitude",
        "zipcode",
        "country_id",
        "locality_verbose",
        "switch_to_order_menu",
        "chain_id",
        "cuisines",
        "average_cost_for_two",
        "currency",
        "currency_affix",
        "open_timings_string",
        "should_track_as_ad",
        "is_o2_ad",
        "ad_type",
        # "offers",
        "aggregate_rating",
        "rating_text",
        "rating_color",
        "votes",
        "show_rating",
        "num_outlets",
        "has_online_delivery",
        "is_delivering_now",
        "status",
        "min_order",
        "current_commission",
        "acceptance_rate",
        "city_id",
        "accepts_online_payment",
        "currency",
        "currency_affix",
        "accepts_loyalty",
        "has_delivery_mode",
        "average_delivery_time",
        "has_pickup_mode",
        "preferred_delivery_mode",
        "show_delivery_mode_screen",
        "has_logistics",
        "logistics_partner_id",
        "tax_display_string",
        "should_show_egg_flag",
        "is_collapsible_menu_available",
        "res_delivery_info_string",
        "should_hide_cuisine",
        "should_hide_photo_review",
        "should_hide_rating",
        "was_user_treats_subscribed",
        "rate",
        "code",
        "is_runnr",
        "is_pin_required",
        "show_online_payment_text",
        "ivr_verification_flag",
        "is_treats_user_subscribed",
        "is_restaurant_treats_member",
        "is_dominos",
        "is_pre_address",
        "can_apply_promo_on_cash",
        "vendor_id",
        "cost_for_two_multiplier",
        "cost_for_one",
        "cost_display",
        "cft_display",
        "average_delivery_time_display",
        "min_order_display",
        "payment_display",
        "show_info_snippet",
        "is_o2_new_arrival",
        "delivery_estimation_info",
        "delivery_closing_info",
        "is_runnr",
        "disable_cooking_instruction",
        "include_bogo_offers",
        "is_opening_soon",
        "disable_back_button_on_payments_screen",
        "payment_info_display_string"
]

# 解析餐馆信息
def parse_info(rest):
        # 获取餐馆信息字典
        rest_dict = rest.get('restaurant')
        # R
        if 'R' in rest_dict.keys():
                rest_R = rest_dict['R']
                rest_dict = dict(rest_dict, **rest_R)

        # location
        if 'location' in rest_dict.keys():
                rest_location = rest_dict['location']
                rest_dict = dict(rest_dict, **rest_location)

        # user_rating
        if 'user_rating' in rest_dict.keys():
                rest_user_rating = rest_dict['user_rating']
                rest_dict = dict(rest_dict, **rest_user_rating)

        # delivery_info
        if 'delivery_info' in rest_dict.keys():
                rest_delivery_info = rest_dict['delivery_info']
                rest_dict = dict(rest_dict, **rest_delivery_info)

        # banner_offer
        if 'banner_offer' in rest_dict.keys():
                rest_banner_offer = rest_dict['banner_offer']
                rest_dict = dict(rest_dict, **rest_banner_offer)

        return rest_dict

# 存储餐馆信息
def save_info(rest_info):
        res={}
        for field in rest_fields:
                if field in rest_info.keys():
                        res[field]=rest_info[field]
                else:
                        res[field]=''
        rest_path=os.path.join(os.path.dirname(__file__),'input_data/rest.csv')
        if not os.path.exists(rest_path):
                with open(rest_path,'w',encoding='utf-8',newline='')as f:
                        write=csv.DictWriter(f,fieldnames=rest_fields)
                        write.writeheader()
        with open (rest_path,'a',encoding='utf-8',newline='')as f:
                write=csv.DictWriter(f,fieldnames=rest_fields)
                write.writerow(res)

# 获取餐馆信息
def get_rest_info(result):
        flag=True
        if result !=None:
                result = json.loads(result)
                rest_info_list = result.get('restaurants')
                # restaurants  key值对应的是一个列表,列表中有多个字典存放着餐馆信息
                if rest_info_list != None:
                        for rest in rest_info_list:
                                # 获取某个餐馆的信息
                                rest_info = parse_info(rest)
                                # 将餐馆信息写入文件
                                save_info(rest_info)
                        flag=False
        return flag

# 错误日志
def rest_log(place_id,str):
        log_fields=[
                'place_id',
                'cause'
        ]

        log_dict={
                'place_id':place_id,
                'cause':str
        }

        log_path=os.path.join(os.path.dirname(__file__),'input_data/rest_log.csv')
        if not os.path.exists(log_path):
                with open(log_path,'w',encoding='utf-8',newline='')as f:
                        write=csv.DictWriter(f,fieldnames=log_fields)
                        write.writeheader()
        with open(log_path, 'a', encoding='utf-8', newline='')as f:
                write = csv.DictWriter(f, fieldnames=log_fields)
                write.writerow(log_dict)


# 获取请求响应
def get_response( payload = "",place_id=0,count=1):
        url = "https://api.zomato.com/v2/order/search.json"

        querystring = {"user_id": "0",
                       "lat": "25.247883735592705",
                       "lon": "55.300432997143986",
                       "mode": "delivery",
                       "delivery_subzone_id":"0" ,
                       "android_country": "CN",
                       "android_language": "zh",
                       "lang": "zh",
                       "sort": "popular",
                       "place_id": place_id,
                       "place_type": "DSZ",
                       "place_name": "Al%20Karama,%20Dubai",

                       }


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
                'Content-Type': "application/x-www-form-urlencoded",
                'Akamai-Mobile-Connectivity': "type=wifi;v=tpv1;tpresult=2;appdata=com.application.zomato.ordering;prepositioned=true;websdk=18.4.2;devicetype=3;rwnd=2097152;optimization=transport",
                'X-Client-Id': "zomato_android_v2",
                'X-Present-Lat': "25.247883735592705",
                'Accept': "image/webp",
                'X-Device-Height': "1794",
                # 'Content-Length': "404",
                'Host': "api.zomato.com",
                'Connection': "Keep-Alive",
                'Accept-Encoding': "gzip",
                'cache-control': "no-cache",
                'Postman-Token': "9c6aa193-39ce-4456-a6de-a5d6cbd5cabb",
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        return response

if __name__ == '__main__':
        # 请求过的location
        has_path =os.path.join(os.path.dirname(__file__),'input_data/has_location.txt')
        if os.path.exists(has_path):
                with open(has_path,'r',encoding='utf-8')as f:
                        has_location=f.readlines()
        else:
                has_location=[]

        # 读取location文件
        location={}
        # 存储location信息
        location_list=[]
        location_path=os.path.join(os.path.dirname(__file__),'input_data/location.csv')
        with open(location_path,'r',encoding='utf-8',newline='')as f:
                reader=csv.DictReader(f,fieldnames=location_fields)
                for row in reader:
                     if reader.line_num==1:
                         continue
                     else:
                          location[row['place_id']]=dict(row)
        location_list=location.keys()

        for loc in location_list:
                if loc+'\n' in has_location:
                        print('请求过')
                        continue

                print('请求%s'%loc)
                postback_params=''
                rest_id_list=[]
                count=1

                # 请求获取响应,请求第一页
                try:
                        response=get_response(payload='',place_id=loc,count=count)
                except:
                        print('请求异常,休息3秒,重新请求')
                        time.sleep(3)
                        try:
                                response = get_response(payload='', place_id=loc, count=count)
                        except Exception as e:
                                print('%s第一页请求错误'%(loc))
                                rest_log(loc,'%s第一页请求错误'%(loc))

                # 获取餐馆信息并保存到文件
                get_rest_info(response.text)

                # 请求该place_id餐馆的总页数
                has_total = json.loads(response.text)['has_total']

                # 该placeId无has_total时,has_total默认为0
                if has_total == None:
                        has_total=0

                print(has_total)

                print(count)
                # 获取请求页面中的postback_params,作为下次请求的请求体
                postback_params = json.loads(response.text)['postback_params']
                while len(rest_id_list)<has_total:
                        count+=1
                        print(count)
                        # 获取请求过的餐馆id加入列表,作为下次请求的请求体
                        for rest in json.loads(response.text)['restaurants']:
                                rest_id_list.append(rest['restaurant']['chain_id'])

                        payload={
                        "postback_params": postback_params,
                        "processed_res_ids[]": rest_id_list
                        }

                        # payload=urlencode(payload)

                        try:
                                response = get_response(payload=payload,place_id=loc,count=count)
                        except:
                                print('请求异常,休息3秒,重新请求')
                                time.sleep(3)
                                try:
                                        response = get_response(payload=payload,place_id=loc,count=count)
                                except Exception as e:
                                        # with open('fail_log.txt','a',encoding='utf-8')as f:
                                        #         fail_info="25.247883735592705"+','+"55.300432997143986"+","+"3792"+'请求异常'+'一共'+str(has_total)+'家餐馆'+','+'获取'+str(len(rest_id_list))+'家餐馆'
                                        #         f.write(fail_info+'\n')
                                        print('%s第%s页请求出错:%s' % (loc, count, str(e.args)))
                                        rest_log(loc, '%s第%s页请求出错:%s,一共%s家餐馆获取%s家餐馆' % (loc, count, str(e.args),has_total,len(rest_id_list)))
                                        break

                        # 获取餐馆信息并保存到文件
                        flag=get_rest_info(response.text)

                        if flag:
                                break

                        # print(postback_params)

                        time.sleep(1)

                with open(has_path,'a',encoding='utf-8')as f:
                        f.write(loc+'\n')




