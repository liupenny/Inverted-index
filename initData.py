import os
import time
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()
english_stopwords = stopwords.words('english')
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '{', '}', '&', '!', '*', '@', '#', '$', '%', '-', "'", "''", '``']

#分词
def split_word(text):
    texts_tokenized = []
    sens = sent_tokenize(text)
    for sent in sens:   
        wt = word_tokenize(sent)
        for word in wt:
            if word.isalpha():
                texts_tokenized.append(word)

    texts_filtered_stopwords = [word for word in texts_tokenized if not word in english_stopwords]
    texts_filtered = [word for word in texts_filtered_stopwords if not word in english_punctuations]
    texts_stemmed = [st.stem(word) for word in texts_filtered]
    texts = texts_stemmed
    return texts

#建立倒排索引
def build_data(word_dict, text, k):
    words = split_word(text)
    for word in words:
        if word in word_dict:
            d = word_dict[word]
            if k in d:
                d[k] += 1
            else:
                d[k] = 1
        else:
            d = word_dict.setdefault(word, {})
            d[k] = 1

#预处理数据、存储倒排索引文件
def load_data():
    path = './data'
    for data in os.walk(path):
        files = data[2]
        word_dict = {}
        k = 0
        for file in files:
            with open(path + '/' + file, 'r') as f:
                text = f.readline()
                t =  f.readlines()[6:]
                for word in t:
                    text += word
            build_data(word_dict, text, k)
            k += 1

        word_dict = {k: word_dict[k] for k in sorted(word_dict.keys())} #从小到大排序
        with open('inverted_file', 'w') as f:
            for item in word_dict.items():
                s = str(item[0]) + '\t'
                for d in item[1].items():
                    s += str(d[0]) + ':' + str(d[1]) + ' '
                f.writelines(s + '\n')


if __name__ == '__main__':
    start = time.clock()
    load_data()
    end = time.clock()
    print('索引构建时间：', end - start, '(s)')
