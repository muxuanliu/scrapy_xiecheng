import pandas as pd
import chardet

# 检测文件编码
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

csv_file_path = 'orignal.csv'

for i in range(1, 10):  # 假设文件名是从1.text到9.text
    encode_list = ['UTF-8-SIG','utf-8','Windows-1254']
    filepath = f'D:/Pycharm/scrapy_xiecheng/data/{i}.txt'  # 使用f-string来插入变量i
    for encoding in encode_list:
        try:
            # 读取文件并存储每一行为一个元素的列表
            data = []
            with open(filepath, 'r', encoding=encoding) as file:
                for line in file:
                    # 移除行尾的换行符并添加到列表中
                    data.append(line.strip())

            # 创建DataFrame，这里我们有一个列名'Data'
            df = pd.DataFrame(data, columns=['Data'])

            df.to_csv(csv_file_path,index=False,encoding=encoding)

            # 显示DataFrame的前几行以检查结果
            print(df.head())
            break
        except UnicodeDecodeError:
            continue
    # print(df)