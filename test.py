# base_url = 'https://hotel.qunar.com/cn/chongqing_city/?fromDate=2024-06-04&toDate=2024-06-05&cityName='
#
# # 城市列表
# page_list = ['重庆', '北京', '上海']
#
# # 使用列表推导式生成start_urls列表
# start_urls = [base_url + city for city in page_list]
#
# print(start_urls)


# import pandas as pd
# import chardet
#
# # 检测文件编码
# def detect_encoding(file_path):
#     with open(file_path, 'rb') as f:
#         result = chardet.detect(f.read())
#     return result['encoding']
#
# csv_file_path = 'D:\Pycharm\scrapy_xiecheng\prepeocess\orignal.csv'
#
# print(detect_encoding(csv_file_path))


import pandas as pd
import thulac
import re

thu1 = thulac.thulac()  #默认模式

df = pd.read_csv('D:/Pycharm/scrapy_xiecheng/prepeocess/orignal.csv', encoding='UTF-8-SIG')

# 定义删除除字母，数字，汉字以外的所有符号的函数
def remove_punctuation(line):
    line = str(line)
    # 如果使用strip()方法移除字符串两端的空白字符后字符串为空，则返回空
    if line.strip() == '':
        return ''
    # 编译一个正则表达式，用于匹配英文字母、数字和中文字符
    # regex是Python标准库中用于正则表达式操作的模块,要import re
    rule = re.compile(u"[^a-zA-Z0-9\u4E00-\u9FA5]")
    # 按照rule1规则移除line中所有不匹配正则表达式的字符
    line = rule.sub('',line)
    return line

# 分词函数
def thulac_segment(text):
    return thu1.cut(text, text=True)  # text_mode=True 表示模式为文本

# 删除除字母，数字，汉字以外的所有符号
df['clean_data'] = df['Data'].apply(remove_punctuation)

# 对CSV文件中的每一行进行分词
df['segmented'] = df['clean_data'].apply(thulac_segment)

# 将分词结果保存到新的CSV文件
df.to_csv('result.csv', index=False, header=False, encoding='utf-8-sig')

