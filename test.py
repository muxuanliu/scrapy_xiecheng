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
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import re
import thulac
import jieba as jb


font_path = 'C:\\Windows\\Fonts\\SimHei.ttf'

plt.rcParams['font.sans-serif'] = ['SimHei']

thu1 = thulac.thulac(seg_only=True,filt=True)  #默认模式

df = pd.read_csv('D:/Pycharm/scrapy_xiecheng/result.csv', encoding='UTF-8-SIG')

def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath,'r',encoding='utf-8').readlines()]
    return stopwords


# 加载停用词
stopwords = stopwordslist("D:\Pycharm\scrapy_xiecheng\ChineseStopWords.txt")
#
# # 定义删除除字母，数字，汉字以外的所有符号的函数
# def remove_punctuation(line):
#     line = str(line)
#     # 如果使用strip()方法移除字符串两端的空白字符后字符串为空，则返回空
#     if line.strip() == '':
#         return ''
#     # 编译一个正则表达式，用于匹配英文字母、数字和中文字符
#     # regex是Python标准库中用于正则表达式操作的模块,要import re
#     rule = re.compile(u"[^a-zA-Z0-9\u4E00-\u9FA5]")
#     # 按照rule1规则移除line中所有不匹配正则表达式的字符
#     line = rule.sub('',line)
#     return line
#
# # 分词函数
# def thulac_segment(text):
#     return thu1.cut(text, text=True,)  # text_mode=True 表示模式为文本
#
# # 删除除字母，数字，汉字以外的所有符号
# df['clean_data'] = df['Data'].apply(remove_punctuation)
#
# # 对CSV文件中的每一行进行分词
# df['segmented'] = df['clean_data'].apply(thulac_segment)

df = df.astype(str)

df['cut_review'] = df.apply(
    lambda x: " ".join([w for w in jb.cut(x) if w not in stopwords])
)


# 合并所有行的'data'列到一个单一的字符串
all_text = " ".join(df['cut_review'])

# 生成词云图
wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(all_text)

# 使用matplotlib显示词云图
# 定义图形大小
plt.figure(figsize=(10, 5))
# interpolation是一个参数，指定图像插值方法，双线性插值(bilinear)是一种平滑插值方法，可以使图像在放大时边缘更平滑
plt.imshow(wordcloud, interpolation='bilinear')
# 关闭坐标轴显示
plt.axis("off")
plt.title(f'Category:travel')
# 保存词云图到文件
plt.savefig(f'wordcloud_travel.png', dpi=300, bbox_inches='tight')
plt.show()


# 统计词频
word_freq = Counter(all_text.split())
# 按频率降序排列
most_common_words = word_freq.most_common(20)  # 选择频率最高的20个词
# 创建条形图
words, frequencies = zip(*most_common_words)  # 解压两个元组列表
plt.figure(figsize=(10, 6))
plt.barh(words, frequencies, color='skyblue')
plt.xlabel('Frequency')
plt.title(f'Category:  Word Frequency')
plt.gca().invert_yaxis()  # 颠倒y轴顺序，使得最常见的词在上方
plt.savefig(f'Word_Frequency_bar.png', dpi=300, bbox_inches='tight')
plt.show()

# 创建饼图
plt.figure(figsize=(10, 10))  # 设置图形大小
plt.pie(frequencies, labels=words, autopct='%1.1f%%', startangle=140)
# 确保饼图是圆形的
plt.axis('equal')
plt.title('Top 20 Most Common Characters')  # 设置图形标题
plt.savefig(f'Word_Frequency_pie.png', dpi=300, bbox_inches='tight')
plt.show()  # 显示图形


# 将词频数据转换为DataFrame
df_word_freq = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
# 按频率降序排列
df_word_freq = df_word_freq.sort_values(by='Frequency', ascending=False)
# 显示前20个最常见的词
print(df_word_freq.head(20))
# 将DataFrame保存为CSV文件
df_word_freq.to_csv('word_frequency.csv', index=False, encoding='utf-8-sig')


# # 将分词结果保存到新的CSV文件
# df['segmented'].to_csv('result.csv', index=False, header=False, encoding='utf-8-sig')

