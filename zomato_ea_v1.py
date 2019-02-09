# from _socket import timeout
import re
import requests
import bs4
import os
import csv
import random
from time import sleep
import traceback

# from urllib3.exceptions import ReadTimeoutError

from proxy_server import abuyun
# from proxy_server import jiguang


myproxies = abuyun.get_proxies
# myproxies = None

class ZomatoEaV1(object):
    def __init__(self, country):
        # self.myproxies = None
        self.country = country
        self.start_url = 'https://www.zomato.com/{}'.format(self.country)
        self.city_field = [
            'country',
            'city',
            'url'
        ]
        self.restaurant_field = [
            'resto_id',
            'url',
            'name',
            'name_str',
            'city',
            'rate',
            'popular_reviews',
            'all_reviews',
            'delivery_reviews'
        ]
        self.url_field = [
            'url',
            'city'
        ]
        self.field = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        }
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/restaurants/{}'.format(self.country))
        self.cities_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input/cities.csv')
        # 创建目录
        file_dir = os.path.split(self.cities_path)[0]
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.has_got_urls = self.load_has_got_urls()
        self.urls_path = None
        self.all_urls = []

    def parse_cities(self):
        res = self.try_request(self.start_url)
        bs = bs4.BeautifulSoup(res.text, 'html.parser')
        mtop_tag = bs.find('div', {'class':'mtop'})
        # country_tags = bs.find_all('li', {'class':'l2-list-item-l1'})
        country = self.country
        city_tags = mtop_tag.find_all('li', {'class':'col-l-4'})
        for city_tag in city_tags:
            a_tag = city_tag.find('a')
            city_name = a_tag.text
            city_url = a_tag.get('href')
            item = {
                'country': country,
                'city': city_name,
                'url': city_url,
            }
            print(item)
            self.save_item('city', item)
                
    def save_item(self, type, item):
        if type == 'city':
            self.data_path = self.cities_path
            self.field = self.city_field
        elif type == 'restaurant':
            self.data_path = os.path.join(self.data_dir, '{}.csv'.format(item.get('city')))
            self.field = self.restaurant_field
            self.has_got_urls.append(item.get('url'))
        elif type == 'url':
            self.data_path = os.path.join(self.data_dir, 'urls/urls.csv')
            self.field = self.url_field

        # 写正常输出
        file_dir = os.path.split(self.data_path)[0]
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # 写表头
        if not os.path.exists(self.data_path):
            with open(self.data_path, 'w', newline='', encoding='utf-8') as f:
                f_csv = csv.DictWriter(f, fieldnames=self.field)
                f_csv.writeheader()
        with open(self.data_path, 'a', newline='', encoding='utf-8') as fw:
            fw_csv = csv.DictWriter(fw, fieldnames=self.field)
            fw_csv.writerow(item)

    def load_cities(self):
        result = []
        with open(self.cities_path, 'r', encoding='utf-8') as f:
            csv_f = csv.DictReader(f, self.city_field)
            for row in csv_f:
                if csv_f.line_num == 1:
                    continue
                result.append(dict(row))
        return result

    def parse_restaurant_urls(self, city):
        try:
            self.all_urls = self.load_urls()
            self.has_got_urls = self.load_has_got_urls()
            url = '{}/delivery'.format(city.get('url'))
            end_tag = False
            page = 1
            base_url = url
            while end_tag is False:
                try:
                    res = self.try_request(url)
                    bs = bs4.BeautifulSoup(res.text, 'html.parser')
                    search_card_tags = bs.find_all('div', {'class':'search-card'})
                    total_tag = bs.find('div', {'class': 'pagination-number'})
                    total_page = int(total_tag.div.find_all('b')[1].text)
                    print('进度: {} / 总页数:{}'.format(page, total_page))
                    for tag in search_card_tags:
                        # 第一种情况, 只有一个餐厅
                        img_tag = tag.find('a', {'class':"feat-img"})
                        r_url = img_tag.get('href')
                        if '/info' in r_url:
                            r_url = r_url.replace('/info', '')
                        if r_url in self.all_urls:
                            print('重复, {}'.format(r_url))
                            continue
                        else:
                            url_item = {
                                'city': r_url.split('/')[3],
                                'url': r_url,
                            }
                            self.save_item('url', url_item)
                            self.all_urls.append(r_url)
                        # res = self.parse_all_info(r_url)
                        # self.save_item('restaurant', res)

                        # 如果有分店,分两种, 一种少于3个,另一种多于2个
                        more_outlet_tag = tag.find('a', {'class': 'pr10'})
                        if more_outlet_tag is None:
                            # 表示少于三个
                            outlet_tags = tag.find_all('a', {'class':'search_chain_bottom_snippet'})
                            for outlet_tag in outlet_tags:
                                tmp_r_url = outlet_tag.get('href')
                                if '/info' in tmp_r_url:
                                    tmp_r_url = tmp_r_url.replace('/info', '')
                                if tmp_r_url in self.all_urls:
                                    print('重复, {}'.format(tmp_r_url))
                                    continue
                                else:
                                    tmp_url_item = {
                                        'city': r_url.split('/')[3],
                                        'url': tmp_r_url,
                                    }
                                    self.save_item('url', tmp_url_item)
                                    self.all_urls.append(r_url)
                                # res = self.parse_all_info(tmp_r_url)
                                # self.save_item('restaurant', res)
                        else:
                            more_url = more_outlet_tag.get('href')
                            print('more_url:', more_url, "cid:", more_url.split('=')[-1])
                            more_url = 'https://www.zomato.com' + more_url
                            self.parse_more_outlets(more_url)
                except:
                    continue
                page += 1
                url = base_url + '?page={}'.format(page)
                print(url)
                print(base_url)
                if page > total_page:
                    end_tag = True
            return True
        except Exception as e:
            print(e, traceback.format_exc())
            return False

    def parse_more_outlets(self, url):
        b_url=url
        end_tag = False
        page = 1
        while end_tag is False:
            res = self.try_request(url)
            bs = bs4.BeautifulSoup(res.text, 'html.parser')
            search_card_tags = bs.find_all('div', {'class':'search-card'})
            total_tag = bs.find('div', {'class': 'pagination-number'})
            outlet_total_page = int(total_tag.div.find_all('b')[1].text)
            print('请求连锁店进度: {} / 总页数:{}'.format(page, outlet_total_page))
            for tag in search_card_tags:
                # 只有一种情况, 只有一个餐厅
                img_tag = tag.find('a', {'class':"feat-img"})
                r_url = img_tag.get('href')
                if '/info' in r_url:
                    r_url = r_url.replace('/info', '')
                if r_url in self.all_urls:
                    print('重复, {}'.format(r_url))
                    continue
                else:
                    url_item = {
                        'city': r_url.split('/')[3],
                        'url': r_url,
                    }
                    self.save_item('url', url_item)
                    self.all_urls.append(r_url)
            page += 1
            url = b_url + '&page={}'.format(page)
            if page > outlet_total_page:
                end_tag = True        

    def parse_info(self, url):
        res = self.try_request(url)
        # 获取餐馆id###################################################
        resto_id=re.findall(r' window.RES_ID = "(.*)";',res.text)[0]
        bs = bs4.BeautifulSoup(res.text, 'html.parser')
        name = url.split('/')[-1]
        print(name)
        name_str = bs.find('h1', {'class': 'res-name'}).a.text.strip()
        print(name_str)
        rate_str = bs.find('div', {'class':'rating-div'}).text.strip('"').strip()
        if '/'in rate_str:
            rate = rate_str.split('/')[0].strip()
        else:
            rate = rate_str
        try:
            popular_reviews = bs.find('a', {'data-sort': 'reviews-top'}).span.text
        except:
            popular_reviews = None
        try:
            all_reviews = bs.find('a', {'data-sort': 'reviews-dd'}).span.text
        except:
            all_reviews = None
        try:
            delivery_reviews = bs.find('a', {'data-sort': 'reviews-delivery'}).span.text
        except:
            delivery_reviews = None

        if '/info' in url:
            url = url.replace('/info', '')
        return {
            'resto_id':resto_id,
            'url': url,
            'city': url.split('/')[-2],
            'name': name,
            'name_str': name_str,
            'rate': rate,
            'popular_reviews': popular_reviews,
            'all_reviews': all_reviews,
            'delivery_reviews': delivery_reviews,
        }
    
    def have_break(self):
        sleep(random.randint(3, 7))

    def load_has_got_urls(self):
        rs = []
        files = os.listdir(self.data_dir)
        for file in files:
            if not file.endswith('.csv'):
                continue
            tmp_data_path = os.path.join(self.data_dir, file)
            with open(tmp_data_path, 'r', encoding='utf-8', newline='') as f:
                csv_reader = csv.DictReader(f, fieldnames=self.restaurant_field)
                for row in csv_reader:
                    if csv_reader.line_num == 1:
                        continue
                    rs.append(dict(row).get('url'))
        print(len(rs))
        return rs

    def load_urls(self):
        all_urls = []
        try:
            self.urls_path = os.path.join(self.data_dir, 'urls/urls.csv')
            with open(self.urls_path, 'r', encoding='utf-8', newline='') as f:
                    csv_reader = csv.DictReader(f, fieldnames=self.url_field)
                    for row in csv_reader:
                        if csv_reader.line_num == 1:
                            continue
                        all_urls.append(dict(row).get('url'))
        except:
            print('还没有保存url')
        return all_urls

    def parse_all_info(self):
        all_urls = self.load_urls()
        self.has_got_urls = self.load_has_got_urls()
        for url in all_urls:
            if url in self.has_got_urls:
                print('重复')
                continue
            # item = self.parse_info(url.get('url'))
            # 请求五次依然
            try:
                item = self.parse_info(url)
            except Exception as e:
                fail_url = os.path.join(self.data_dir, 'fail_url.txt')
                with open(fail_url,'a',encoding='utf-8')as f:
                    f.write(url+'请求出错了'+str(e.args)+'\n')
                print(url+'请求出错了'+str(e.args))
                continue
            self.save_item('restaurant', item)

    # 因为经常中断, 所以多尝试几次, 5次默认
    def try_request(self, url, time=5):
        print('请求', url)
        while time != 0:
            time -= 1
            try:
                # self.have_break()
                # self.myproxies = jiguang.get_proxies(self.myproxies)
                res = requests.get(url, headers=self.headers, timeout=2 ,proxies=myproxies())
                return res
            except Exception as e:
                print(url+str(e.args))
                # print(traceback.format_exc(), e)
        print('警告警告:请求多次依旧失败!')
        return None

if __name__ == '__main__':
    p = ZomatoEaV1('uae')
    # p.parse_cities()
    cities = p.load_cities()
    for city in cities:
        # end_tag = p.parse_restaurant_urls(city)
        p.parse_all_info()
