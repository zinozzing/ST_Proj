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

df = pd.read_csv('도시별_긍부정지수_및_긍부정단어목록/긍부정단어목록.csv', header=None)
df = df.iloc[:,0:5]
df['pos'] = df[1]+df[2]
df['neg'] = df[3]+df[4]
df.drop([0,1,2,3,4], axis=1, inplace=True)
df = df.iloc[1:]

def text_cleaning(text):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') 
    result = hangul.sub('', text)
    return result

df['ko_text'] = df['pos'].apply(lambda x : text_cleaning(x))  #pos neg 조절


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
    min_support=0.3,
    min_confidence=0.5,
    min_lift=1.5,
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

# 그래프 디자인과 관련된 파라미터를 설정합니다.
pos = nx.spring_layout(G, k=0.6, iterations=50)
nx.draw(G, pos=pos, node_size = [v * 20 for v in degree_dict.values()], edge_color=weights)


#폰트설정
font_fname = 'NanumGothic.ttf'
fontprop=fm.FontProperties(fname=font_fname, size=18).get_name()

nx.draw_networkx_labels(G, pos=pos, font_family=fontprop, font_size=25)


deg_cent = []
closeness_cent = []
between_cent = []
eigenvector = []


for node in G.nodes():
    deg_cent.append([node,nx.degree_centrality(G)[node]])
    closeness_cent.append([node,nx.closeness_centrality(G, node)])
    between_cent.append([node,nx.betweenness_centrality(G)[node]])
    eigenvector.append([node,nx.eigenvector_centrality(G, max_iter=1000)[node]])

## 중심성 별 상위 5개 출력
print("degree centrality: ",sorted(deg_cent, key=lambda x: x[1], reverse=True)[0:6])
print("closeness centrality: ",sorted(closeness_cent, key=lambda x: x[1], reverse=True)[0:6])
print("betweeness centrality: ",sorted(between_cent, key=lambda x: x[1], reverse=True)[0:6])
print("eigenvector centrality: ",sorted(eigenvector, key=lambda x: x[1], reverse=True)[0:6])


# 그래프를 출력합니다.
ax = plt.gca()
plt.savefig('posnegSNA.png')
plt.show() 