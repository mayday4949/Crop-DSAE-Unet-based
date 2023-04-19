# -*- coding: utf-8 -*-

import math
import jieba
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

def cosine_similarity(s1, s2):
    # 将字符串分词并转换为向量
    vec1 = list(jieba.cut(s1))
    vec2 = list(jieba.cut(s2))
    
    # 将所有的单词存储到set中
    words = set(vec1 + vec2)
    
    # 计算每个向量中每个单词的出现次数
    vec1 = [vec1.count(w) for w in words]
    vec2 = [vec2.count(w) for w in words]
    
    # 计算余弦相似度
    dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(v1 ** 2 for v1 in vec1))
    magnitude2 = math.sqrt(sum(v2 ** 2 for v2 in vec2))
    
    # 处理分母为0的情况
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    
    similarity = dot_product / (magnitude1 * magnitude2)
    return similarity

def calculate_similarity(json_data):
    json_data = json.loads(json_data)

    tfidf = TfidfVectorizer()
    documents = [json_data[f"str{i}"] for i in range(0, 6)]
    sparse_matrix = tfidf.fit_transform(documents)
    similarities = cosine_similarity(sparse_matrix[0], sparse_matrix[1:])
    return similarities.flatten()

json_data = '{"str0":"农业发展对国家经济至关重要","str1":"我国拥有广阔的耕地和良好的自然条件，因此农业发展非常重要。","str2":"农业是我国经济的重要支柱，为国家的发展作出了巨大贡献。","str3":"农村地区的经济发展与农业密切相关，农业的发展对农村经济和社会发展起到了关键作用。","str4":"许多地区的居民都从事农业生产，农业成为了这些地区主要的产业。","str5":"农业产值占据了我国国民经济的很大比重，农业的发展对我国经济的发展有着至关重要的作用。"}'
target_str = "农业发展对国家经济至关重要。"

similarities = calculate_similarity(json_data)
print(similarities)

