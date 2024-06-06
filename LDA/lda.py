from gensim.models import LdaModel
import pandas as pd
from gensim.corpora import Dictionary
from gensim import corpora, models
import csv
import pyLDAvis
import pyLDAvis.gensim_models



df = pd.read_csv('D:/Pycharm/scrapy_xiecheng/prepeocess/filtered_chinese_file.csv', encoding='UTF-8-SIG')

# 直接给columns属性赋值来添加或修改列名
df.columns = ['or', 'np', 'sp']


data_set = []  # 建立存储分词的列表
for i in range(len(df['sp'])):
    result = []
    text = str(df['sp'][i])
    seg_list = text.split()
    for w in seg_list:  # 读取每一行分词
        result.append(w)
    data_set.append(result)

dictionary = corpora.Dictionary(data_set)  # 构建词典
corpus = [dictionary.doc2bow(text) for text in data_set]  #表示为第几个单词出现了几次

lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=6, passes=30, random_state=1)
topic_list = lda.print_topics()

# 保存模型到文件
lda.save('lda_model.model')
print(topic_list)

for i in lda.get_document_topics(corpus)[:]:
    listj = []
    for j in i:
        listj.append(j[1])
    bz = listj.index(max(listj))
    # print(i[bz][0])

# 使用pyLDAvis准备可视化
vis = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary)

pyLDAvis.display(vis)
