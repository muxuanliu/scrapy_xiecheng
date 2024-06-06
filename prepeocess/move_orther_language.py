import pandas as pd
import re

# 读取CSV文件
df = pd.read_csv('D:/Pycharm/scrapy_xiecheng/Visualization/result.csv', encoding='UTF-8-SIG')

# 定义一个函数，检查DataFrame行是否包含中文字符
def contains_chinese(row):
    # 正则表达式，匹配中文字符的Unicode范围是\u4e00-\u9fff
    pattern = re.compile('[\u4e00-\u9fff]')
    # 对于行中的每个元素，检查是否至少有一个中文字符
    return any(pattern.search(str(cell)) for cell in row)

# 筛选出包含中文字符的行
chinese_rows = df.apply(contains_chinese, axis=1)

# 保留包含中文字符的行
df_chinese_only = df[chinese_rows]

# 将结果保存到新的CSV文件
df_chinese_only.to_csv('filtered_chinese_file.csv', index=False, encoding='utf-8-sig')