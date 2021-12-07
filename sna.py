#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mpl
from networkx.classes.function import get_node_attributes
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import matplotlib.font_manager as fm
import re
from konlpy.tag import Okt
from collections import Counter
from apyori import apriori
import networkx as nx
import random as rd


"""
- graph로부터 다음 세 가지 centrality와 pagerank를 계산하여 딕셔너리로 리턴해주는 함수
    - weighted degree centrality
    - closeness centrality
    - betweenness centrality
    - pagerank
"""

def return_centralities_as_dict(input_g):
    # weighted degree centrality를 딕셔너리로 리턴
    def return_weighted_degree_centrality(input_g, normalized=False):
        w_d_centrality = {n:0.0 for n in input_g.nodes()}
        for u, v, d in input_g.edges(data=True):
            w_d_centrality[u]+=d['weight']
            w_d_centrality[v]+=d['weight']
        if normalized==True:
            weighted_sum = sum(w_d_centrality.values())
            return {k:v/weighted_sum for k, v in w_d_centrality.items()}
        else:
            return w_d_centrality
    def return_closeness_centrality(input_g):
        new_g_with_distance = input_g.copy()
        for u,v,d in new_g_with_distance.edges(data=True):
            if 'distance' not in d:
                d['distance'] = 1.0/d['weight']
        return nx.closeness_centrality(new_g_with_distance, distance='distance')
    def return_betweenness_centrality(input_g):
        return nx.betweenness_centrality(input_g, weight='weight')
    def return_pagerank(input_g):
        return nx.pagerank(input_g, weight='weight')
    return {
        'weighted_deg':return_weighted_degree_centrality(input_g),
        'closeness_cent':return_closeness_centrality(input_g), 
        'betweeness_cent':return_betweenness_centrality(input_g),
        'pagerank':return_pagerank(input_g)
    }


# data = pd.read_csv('도시별_긍부정지수_및_긍부정단어목록/긍부정단어목록.csv')

city_list = ['bangkok','cebu','danang','fukuoka','hanoi','hongkong','osaka','sapporo','taipei','tokyo']
data = pd.DataFrame()

for city in city_list:     ######
    #데이터전처리
    df = pd.read_csv('travel_csv/'+city+'_blog_crawling.csv', header=None)
    data = pd.concat([data,df],axis=0)
df = data.iloc[:,0:1].reset_index()


def text_cleaning(text):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') 
    result = hangul.sub('', text)
    return result

df['ko_text'] = df[0].apply(lambda x : text_cleaning(x))


stopwords = ['여행','타이베이','있는']

def get_nouns(x):
    nouns_tagger = Okt()
    nouns = nouns_tagger.nouns(x)
    # 한글자 키워드를 제거합니다.
    nouns = [noun for noun in nouns if len(noun) > 1]
    # 불용어를 제거합니다.
    nouns = [noun for noun in nouns if noun not in stopwords]
    return nouns

# ‘ko_text’ 피처에 이를 적용합니다.
df['nouns'] = df['ko_text'].apply(lambda x: get_nouns(x))

# 트랜잭션 데이터를 추출합니다.
transactions = df['nouns'].tolist()
transactions = [transaction for transaction in transactions if transaction] # 공백 문자열을 방지합니다.

# 연관 분석을 수행합니다.
results = list(apriori(transactions,
    min_support=0.01,       #지지도 - 표시되는 노드수가 많아짐
    min_confidence=0.05,    #신뢰도 - 선의 갯수가 달라짐
    min_lift=2,
    max_length=2))

# 데이터 프레임 형태로 정리합니다.
columns = ['source', 'target', 'support']
network_df = pd.DataFrame(columns=columns)

# 규칙의 조건절을 source, 결과절을 target, 지지도를 support 라는 데이터 프레임의 피처로 변환합니다.
for result in results:
    if len(result.items) == 2:
        items = [x for x in result.items]
        row = [items[0], items[1], result.support]
        series = pd.Series(row, index=network_df.columns)
        network_df = network_df.append(series, ignore_index=True)

# 말뭉치를 추출합니다.
corpus = "".join(df['ko_text'].tolist())

# 명사 키워드를 추출합니다.
nouns_tagger = Okt()
nouns = nouns_tagger.nouns(corpus)
count = Counter(nouns)

# 한글자 키워드를 제거합니다.
remove_char_counter = Counter({x : count[x] for x in count if len(x) > 1})

# 키워드와 키워드 빈도 점수를 ‘node’, ‘nodesize’ 라는 데이터 프레임의 피처로 생성합니다.
node_df = pd.DataFrame(remove_char_counter.items(), columns=['node', 'nodesize'])
node_df = node_df[node_df['nodesize'] >= 10] # 시각화의 편의를 위해 ‘nodesize’ 5 이하는 제거합니다.
node_df.head()

plt.figure(figsize=(25,25))

# networkx 그래프 객체를 생성합니다.
G = nx.Graph()


# node_df의 키워드 빈도수를 데이터로 하여, 네트워크 그래프의 ‘노드’ 역할을 하는 원을 생성합니다.
for index, row in node_df.iterrows():
    G.add_node(row['node'], nodesize=row['nodesize'])

# network_df의 연관 분석 데이터를 기반으로, 네트워크 그래프의 ‘관계’ 역할을 하는 선을 생성합니다.
for index, row in network_df.iterrows():
    G.add_weighted_edges_from([(row['source'], row['target'], row['support'])])


for u, v, d in G.edges(data=True):
    d['weight'] = rd.random()
    
edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())

node_s = get_node_attributes(G,'nodesize')

node_size = [v * 1.0 for v in node_s.values()]
degree_dict = {** dict(G.degree), **node_s}

# node_size = [v * 100 for v in node_s.values()]
# 그래프 디자인과 관련된 파라미터를 설정합니다.
pos = nx.spring_layout(G, k=0.6, iterations=50)
# sizes = [G.nodes[node]['nodesize']*25 for node in G]
nx.draw(G, pos=pos, node_size = [v * 20 for v in degree_dict.values()], edge_color=weights)



#폰트설정
font_fname = 'NanumGothic.ttf'
fontprop=fm.FontProperties(fname=font_fname, size=18).get_name()


nx.draw_networkx_labels(G, pos=pos, font_family=fontprop, font_size=15)


weigh_deg = []
cloness_cent = []
between_cent = []
page_rank = []


# 중심성 구하기
for k, v in list(return_centralities_as_dict(G).items()):
    result = "{}: {}".format(k, v)


# 그래프를 출력합니다.
ax = plt.gca()
plt.show()