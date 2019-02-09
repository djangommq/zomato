# -*- coding: utf-8 -*-
import csv
import datetime
import time
import logging
import os
import requests
import traceback

date = datetime.datetime.now().strftime("%Y-%m-%d")
VERSION = date

logFilename = '../crawlerOutput/{}/log/zomato.log'.format(VERSION)
log_dir = os.path.split(logFilename)[0]
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
  level = logging.DEBUG,  # 定义输出到文件的log级别，
  format = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
  datefmt= '%Y-%m-%d %A %H:%M:%S',  # 时间
  filename = logFilename,  # log文件名
  filemode = 'w')

basic_dir = '../crawlerOutput/{}/zomato'.format(VERSION)

#  保存城市所有的餐馆
resto_file = 'resto_details_city.csv'
# 保存城市所有的连锁店第一家
chain_file = 'chain_resto_details.csv'
# 保存连锁餐馆的详细列表
ch_file = 'ch_resto.csv'
fields = [
    'resto_id',
    'resto_name',
    'resto_loc_addr',
    'resto_loc_locality',
    'resto_loc_city',
    'resto_loc_lat',
    'resto_loc_lng',
    'resto_phone',
    'resto_mob_phone',
    'resto_mob_phone_display',
    'resto_cuisines',
    'resto_avg_cost_for_two',
    'resto_price_range',
    'resto_user_rating_agg_rating',
    'resto_user_rating_votes',
    'resto_review_counts',
    'resto_entity_type',
    'resto_all_reviews_count',
    'resto_has_online_delivery',
    'resto_chain_id',
]


def getData(city_id, next_res_start=0, ch_id=0):
    api_url = 'https://api.zomato.com/v2/search_restaurants.json'
    header = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'referer': 'https://www.zomato.com/',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
        # *****update api_key*****
        'x-zomato-api-key': '239899c6817b488ba5d82bbd49676a76'
    }
    data = {
        'start': next_res_start,
        'count': 50,
        'category': 0,
        'sort': 'popularity',
        # city_id - 1-New Delhi; 3-Mumbai; 7-Chennai;
        'entity_id': city_id,
        'entity_type': 'city',
        # update user_id with your info
        'user_id': 43324240,
        'lang': 'en',
        'android_language': 'en',
        'android_country': 'IN',
        # update timestamp
        'timestamp': 1536914767,
        'trigger_page': 'search_suggestion_home_tab',
        'trigger_identifier': 'search_all',
        'page': 1,
    }
    if ch_id != 0:
        data['chain_id'] = ch_id
    try:
        with requests.get(api_url, params=data, headers=header, timeout=60) as res:
            print(res.url)
            try:
                return res.json()
            except:
                return {}
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        return {}


def save(data, file_path):
    file_dir = os.path.split(file_path)[0]
    if not os.path.exists(file_dir):
        print(file_dir)
        os.makedirs(file_dir)
    # 写表头
    if not os.path.exists(file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            f_csv = csv.DictWriter(f, fieldnames=fields)
            f_csv.writeheader()
    with open(file_path, 'a', newline='', encoding='utf-8') as fw:
        fw_csv = csv.DictWriter(fw, fieldnames=fields)
        fw_csv.writerow(data)


def load_cities():
    file_path = './input/zomato_ea.csv'
    city_fields = [
        'country',
        'city',
        'id',
    ]
    result = []
    with open(file_path, 'r', encoding='utf-8') as f:
        csv_f = csv.DictReader(f, city_fields)
        for row in csv_f:
            if csv_f.line_num == 1:
                continue
            result.append(dict(row))
    print(result)
    return result


def eachCity():
    print(date)
    cities = load_cities()
    for tmp_city in cities:
        # 按城市列表获取, i[2]是city_id
        city_id = tmp_city.get('id')
        city = tmp_city.get('city')
        country = tmp_city.get('country').replace(' ', '_')
        #  保存城市所有的餐馆
        resto_file = '{}/{}_resto_details_city.csv'.format(country, city)
        # 保存城市所有的连锁店第一家
        chain_detail_file = '{}/{}_chain_resto_details.csv'.format(country, city)
        # 保存连锁餐馆的详细列表
        chain_all_file = '{}/{}_ch_resto.csv'.format(country, city)

        resto_path = os.path.join(basic_dir, resto_file)
        chain_detail_path = os.path.join(basic_dir, chain_detail_file)
        chain_all_path = os.path.join(basic_dir, chain_all_file)

        try:
            # 普通的餐馆id, 每次获取50个
            res = getData(city_id)
            if res == {}:
                logging.info('请求出错, 错误')
            res_to = res.get('results_found')
            logging.info('{}的餐馆总数: {}'.format(city, res_to))
            for x in range(0, res_to - 50, 50):
                res = getData(city_id, x)
                if res == {}:
                    logging.info('请求出错, 错误')
                    continue
                restaurants = res.get('restaurants')
                for r in restaurants:
                    tmp_restaurant = r.get('restaurant')
                    item = {
                        "resto_id": tmp_restaurant.get('id'),
                        "resto_name": tmp_restaurant.get('name')
                    }
                    tmp_location = tmp_restaurant.get('location')
                    item["resto_loc_addr"] = tmp_location.get('address')
                    item["resto_loc_locality"] = tmp_location.get('locality')
                    item["resto_loc_city"] = tmp_location.get('city')
                    item["resto_loc_lat"] = tmp_location.get('latitude')
                    item["resto_loc_lng"] = tmp_location.get('longitude')
                    item["resto_phone"] = tmp_restaurant.get('phone')
                    item["resto_mob_phone"] = tmp_restaurant.get('mobile_phone')
                    item["resto_mob_phone_display"] = tmp_restaurant.get('mobile_phone_display')
                    item["resto_cuisines"] = tmp_restaurant.get('cuisines')
                    item["resto_avg_cost_for_two"] = tmp_restaurant.get('average_cost_for_two')
                    item["resto_price_range"] = tmp_restaurant.get('price_range')
                    tmp_user_rating = tmp_restaurant.get('user_rating')
                    item["resto_user_rating_agg_rating"] = tmp_user_rating.get('aggregate_rating')
                    item["resto_user_rating_votes"] = tmp_user_rating.get('votes')
                    item["resto_review_counts"] = tmp_restaurant.get('reviews_count')
                    item["resto_entity_type"] = tmp_restaurant.get('entity_type')
                    item["resto_all_reviews_count"] = tmp_restaurant.get('all_reviews_count')
                    item["resto_has_online_delivery"] = tmp_restaurant.get('has_online_delivery')
                    item["resto_chain_id"] = tmp_restaurant.get('chain_id')

                    save(item, resto_path)

                    if item.get('resto_chain_id') is not None:
                        save(item, chain_detail_path)
                        # 请求连锁店的其他店铺
                        logging.info('请求连锁店铺')
                        tmp_chain_id = item.get('resto_chain_id')
                        res = getData(city_id, 0, tmp_chain_id)
                        if res == {}:
                            logging.info('请求出错, 错误')
                            continue
                        tot_res = res.get('all_results')
                        total_count3 = res.get('results_found')
                        logging.info('name:{}, id:{}连锁店铺的请求结果: all_results: {}, results_found: {}'.format(
                            item.get('resto_name'),
                            item.get('resto_chain_id'),
                            tot_res, total_count3))
                        # 如果返回为空, 跳过
                        if total_count3 is None:
                            logging.error("餐馆{}的连锁店请求返回空, 需要排查异常, chain_id为{}".format(item['resto_name'], item['resto_chain_id']))
                            continue
                        # print 'total_count3', total_count3
                        for offset in range(0, int(total_count3), 50):
                            if offset < 150:
                                # logging.info("爬取%s的%d~%d条" % (chain_data['resto_name'], offset, offset + 50))
                                res = getData(city_id, offset, tmp_chain_id)
                                if res == {}:
                                    logging.info('请求出错, 错误')
                                    continue
                                restaurants = res.get('restaurants')
                                for r in restaurants:
                                    tmp_restaurant = r.get('restaurant')
                                    tmp_item = {
                                        "resto_id": tmp_restaurant.get('id'),
                                        "resto_name": tmp_restaurant.get('name')
                                    }
                                    tmp_location = tmp_restaurant.get('location')
                                    tmp_item["resto_loc_addr"] = tmp_location.get('address')
                                    tmp_item["resto_loc_locality"] = tmp_location.get('locality')
                                    tmp_item["resto_loc_city"] = tmp_location.get('city')
                                    tmp_item["resto_loc_lat"] = tmp_location.get('latitude')
                                    tmp_item["resto_loc_lng"] = tmp_location.get('longitude')
                                    tmp_item["resto_phone"] = tmp_restaurant.get('phone')
                                    tmp_item["resto_mob_phone"] = tmp_restaurant.get('mobile_phone')
                                    tmp_item["resto_mob_phone_display"] = tmp_restaurant.get('mobile_phone_display')
                                    tmp_item["resto_cuisines"] = tmp_restaurant.get('cuisines')
                                    tmp_item["resto_avg_cost_for_two"] = tmp_restaurant.get('average_cost_for_two')
                                    tmp_item["resto_price_range"] = tmp_restaurant.get('price_range')
                                    tmp_user_rating = tmp_restaurant.get('user_rating')
                                    tmp_item["resto_user_rating_agg_rating"] = tmp_user_rating.get('aggregate_rating')
                                    tmp_item["resto_user_rating_votes"] = tmp_user_rating.get('votes')
                                    tmp_item["resto_review_counts"] = tmp_restaurant.get('reviews_count')
                                    tmp_item["resto_entity_type"] = tmp_restaurant.get('entity_type')
                                    tmp_item["resto_all_reviews_count"] = tmp_restaurant.get('all_reviews_count')
                                    tmp_item["resto_has_online_delivery"] = tmp_restaurant.get('has_online_deliver')
                                    tmp_item["resto_chain_id"] = tmp_restaurant.get('chain_id')

                                    save(tmp_item, chain_all_path)
        except requests.exceptions.ConnectionError:
            logging.error('出现超时错误')
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())


if __name__ == '__main__':
    eachCity()
