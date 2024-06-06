# base_url = 'https://hotel.qunar.com/cn/chongqing_city/?fromDate=2024-06-04&toDate=2024-06-05&cityName='
#
# # 城市列表
# page_list = ['重庆', '北京', '上海']
#
# # 使用列表推导式生成start_urls列表
# start_urls = [base_url + city for city in page_list]
#
# print(start_urls)


import pandas as pd
import chardet

# 检测文件编码
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

csv_file_path = 'D:\Pycharm\scrapy_xiecheng\prepeocess\orignal.csv'

print(detect_encoding(csv_file_path))
