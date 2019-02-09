# zomato

## 基本情况

- 起始于: 2017.12
- 相关国家和地区: 
> 亚太区: India, Australia, New Zealand, Sri Lanka (详见 input/zomato_apac.csv)  
> 中东和非洲区: UAE (详见 input/zomato_ea.csv)

- 运行服务器: 新加坡1

## 数据获取途径

- 相关API  

**app**(使用)

| 序号 | 用途 | url | 详细 |
| --- | --- | --- | --- |
| 1 | 通过城市id获取餐馆信息 | https://api.zomato.com/v2/search_restaurants.json | ... |

**WEB**(屏蔽了aws的ip段, 不能用)  

| 序号 | 用途 | url | 详细 |
| --- | --- | --- | --- |
| 1 | 根据地区名称得到餐馆列表 | https://www.zomato.com/dubai/restaurants | ... |
| 2 | 遍历每一页的餐馆 | https://www.zomato.com/dubai/restaurants?page=2 | ... |
| 3 | 对于本地区连锁的餐馆,加载并解析 | https://www.zomato.com/dubai/restaurants?cid=200003 | ... |
| 4 | 餐馆详情页, 解析页 | https://www.zomato.com/dubai/burger-king-world-trade-center/info | ... |


## 代码位置:
- [gitlab](https://gitlab.yunfutech.com/uber_crawler/zomato.git)
- 简介: 
> 重构后的代码使用scrapy框架  
> 通过zomato_start.sh启动, 包含中东和亚太两个爬虫, 可选择启动, 结果分目录输出.


## 进展
- 代码稳定运行至20180903  
- 9月10号发现异常, 有5个城市返回数据异常, 由于无法抓包(连接charles即断开), 决定通过web页面抓取
- 9/14 api返回正常, 重构到python3版本, 增加了异常的处理, 避免中断, 数据正常


## 追加要求

- 2018.06.29 新增印度四个城市: Vijaywada, Bhopal, Mysore, Madurai
- 2018.07.16 增加Sri Lanka 的数据
- 2018.09.07 中东区要求, 14日提交demo



------

## API简介
