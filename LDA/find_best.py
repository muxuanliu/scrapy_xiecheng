import gensim
from gensim import corpora
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import warnings
import re
import multiprocessing

warnings.filterwarnings('ignore')  # To ignore all warnings that arise here to enhance clarity

from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel

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
print(data_set)

dictionary = corpora.Dictionary(data_set)  # 构建词典
corpus = [dictionary.doc2bow(text) for text in data_set]  #表示为第几个单词出现了几次


# 计算困惑度
def perplexity(num_topics):
    ldamodel = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=30)
    print(ldamodel.print_topics(num_topics=num_topics, num_words=15))
    print(ldamodel.log_perplexity(corpus))
    return ldamodel.log_perplexity(corpus)


# 计算coherence
def coherence(num_topics):
    ldamodel = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=30, random_state=1)
    print(ldamodel.print_topics(num_topics=num_topics, num_words=10))
    ldacm = CoherenceModel(model=ldamodel, texts=data_set, dictionary=dictionary, coherence='c_v')
    print(ldacm.get_coherence())
    return ldacm.get_coherence()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    x = range(1,15)
    # z = [perplexity(i) for i in x]  #如果想用困惑度就选这个
    y = [coherence(i) for i in x]
    plt.plot(x, y)
    plt.xlabel('主题数目')
    plt.ylabel('coherence大小')
    plt.rcParams['font.sans-serif']=['SimHei']
    matplotlib.rcParams['axes.unicode_minus']=False
    plt.title('主题-coherence变化情况')
    plt.savefig(f'coherence变化情况.png', dpi=300, bbox_inches='tight')
    plt.show()

