## 🪁 네이버 블로그 크롤링을 통한 국가 별 관광지 감정 분석 : </br> 주요 10개 관광지의 호감도조사 및 호감요인 분석을 통한 마케팅 활용 방안 제시

## 2021-2 Hanyang University, Social Network Analysis and Text Mining Project

---

## Part 1 : 데이터 수집

1. 한국인들이 사랑하는 주요 관광지(도시) 10개 선정

   `오사카 도쿄 방콕 후쿠오카 다낭 타이베이 홍콩 세부 하노이 삿포로` by 스카이스캐너(최대 비행 티켓팅 사이트)

   위 관광 도시에는 어떤 호감요인과 비호감요인이 존재하고, 트래버들의 마음을 이끈 것일까?

</br>

2. 네이버 블로그 크롤링 작업

   11월 25일 기준, '도시명 + 여행'으로 검색했을 때 나오는 90개의 블로그 글 수집
   (제목, 링크, 날짜, 본문)

   `dir > ST_PROJ/blogCrawling.py`

   `dir > ST_PROJ/travel_csv`

   ```python
   # input 값을 통해 원하는 범위, 기간, 단어를 사용자가 지정할 수 있도록 코딩
   def main():
   num = int(input("1페이지부터 원하는 페이지의 범위: "))
   opt = input("원하는 데이터의 수집 기간(ex. 0 = 전체 , 1 = 1시간, 2 = 1일, 3 = 1주, 4 = 1개월, 5 = 3개월, 6 = 6개월, 7 = 1년): ")
   keyw = input("크롤링을 원하는 단어: ")
   # 메인 크롤링 함수
   main_crawling(num,opt,keyw)
   ```

   ```python
    # CSV 파일 저장 함수
    def toCSV(temp_list):
    with open('blog_crawling.csv', 'a', encoding='utf-8-sig', newline='') as file:
        # encoding UTF-8 XXX -> must utf-8-sig
        csvfile = csv.writer(file)
        for row in temp_list:
            csvfile.writerow(row)
   ```

</br>

## Part 2 : 데이터 전처리

1. 트위터에서 만든 한국어 분석 라이브러리 ‘Okt’를 이용한 명사분석

</br>

2. 불용어 / 한 글자 단어 제거

   `['방콕','세부','다낭','후쿠오카','하노이','홍콩','오사카','삿포로','타이페이','도쿄','대만','필리핀','베트남','일본','중국','태국','여행','타이베이','있는','이','그','잘','못','ㅋㅋ','ㅎㅎ','홍콩의','홍콩이’]`

</br>

3. 토큰화 작업

   ```python
   #데이터전처리
   df = pd.read_csv('C:/Users/twentystones/Desktop/사회연결망분석텀프로젝트/travel_csv/'+city+'_blog_crawling.csv', header=None)
   df.rename(columns= {0:'title', 1:'URL', 2:'day', 3:'body'}, inplace=True)

   text = ''
   for i in range(1,90): #한 도시의 90개 글 모두 한 문장안에 통합
      text = text + df['body'][i]

   #명사 분리.
   tokens_ko=okt.nouns(text)

   #불용어제거
   stop_words = ['방콕','세부','다낭','후쿠오카','하노이','홍콩','오사카','삿포로','타이페이','도쿄','대만','필리핀','베트남','일본','중국','태국','여행','타이베이','있는','이','그','잘','못','ㅋㅋ','ㅎㅎ','홍콩의','홍콩이','지옥','포기','후회']
   tokens_ko = [each_word for each_word in tokens_ko if (each_word not in stop_words)&(len(each_word) !=1)]
   ```

</br>

## Part 3 : 빈출단어 분석

1.  각 지역별 빈출단어 시각화(그래프)

    ![그림1](https://user-images.githubusercontent.com/50936176/147207729-38178ce6-6104-43dc-af9b-4a942ac5bd48.png)

    ```python
      #빈출단어 카운트
      ko=nltk.Text(tokens_ko, name=city)

      #단어 빈도순 정렬
      ko.vocab()

      #워드그래프
      path = "c:/Windows/Fonts/malgun.ttf"
      if platform.system() == 'Darwin':
         rc('font', family='AppleGothic')
      elif platform.system() == 'Windows':
         font_name = font_manager.FontProperties(fname=path).get_name()
         rc('font', family=font_name)
      else:
         print('Unknown system... sorry~~~~')

      %matplotlib inline
      plt.figure(figsize=(14,8))
      plt.title(city)
      ko.plot(50)
      plt.show()
    ```

</br>

2.  각 지역별 빈출단어 시각화(워드클라우드)

    ![그림2](https://user-images.githubusercontent.com/50936176/147207737-69039cda-ca04-402b-b173-8c37cc80785c.png)

    ```python
    #워드클라우드
    data = ko.vocab().most_common(200) #단어갯수 조절
    airplain_mask=np.array(Image.open("C:/Users/twentystones/Desktop/사회연결망분석텀프로젝트/airplain.jfif"))
    wc=WordCloud(font_path='c:\windows\Fonts\malgun.ttf',background_color='white', relative_scaling=0.2,stopwords=stop_words, mask=airplain_mask).generate_from_frequencies(dict(data))

    plt.figure(figsize=(20,12))
    plt.imshow(wc)
    plt.axis('off')
    plt.title(city)
    plt.show()
    ```

</br>

3.  빈출단어 분석

    비교적 저렴한 동남아 지역(방콕, 세부, 다낭, 홍콩, 타이페이)은 ‘호텔’이라는 단어가 눈에 띄게 많이 등장

    ➩ 저렴한 가격으로 높은 서비스를 이용하는 활동이 중심이 됨

    `하나하나까지 럭셔리 호텔에서 봐 왔던 아이템이 눈에 많이 띕니다 `

    `Park Hyatt Bangkok 호텔 주변에는 왓 파툼 와나람, 에라완 사원, 룸피니 공원을 비롯해 고급 레스토랑과 푸드 홀, 디자이너숍 등이 입점해 있는 센트럴 엠버시몰까지 모두 도보로 갈 수 있습니다 `

    반면 가격대가 비교적 있는 일본의 3개 지역(후쿠오카, 오사카, 도쿄)은 ‘호텔’이라는 단어 빈출도는 매우 낮으며, 비교적 ‘사진’이라는 단어가 확연히 빈번하게 등장

    ➩ 비용이 덜 드는 활동 중심적, 주변에 알리고 추억하기를 희망

    `그래도 이 카페 분위기는 짱짱 인스타 사진 찍기 딱 좋아 `

    `뭔가 이 순간을 기억해야지 하고 사진 찍었는데이게 마지막 후쿠오카 자유여행이었네요`

</br>

4. 도시별 특이점 분석

   - 일본도시에서는 ‘투어’라는 단어가 거의 등장하지 않음

   - 타이페이/홍콩/다낭은 ‘투어’라는 단어가 적게 등장

   - 그러나 세부/하노이에서는 ‘투어’라는 단어가 눈에 띄게 많이 등장 ➩ 투어형 관광이 많음

</br>

## Part 4 : KNU 감성사전을 이용한 감성분석 및 호감도 조사

1. 국립국어원 표준국어대사전을 구성하는 각 단어의 뜻풀이를 분석하여 긍,부정어를 추출

   이를 토대로 30만 여개의 단어 중 약 1만 5천단어에 ‘매우 부정’, ‘부정’, ‘중립’, ‘긍정’, ‘매우 긍정’ 부여

   `dir > ST_PROJ/도시별_긍부정지수_및_긍부정단어목록`

2. 블로그 글마다 단어 수가 다름 ➩ 부정단어 대비 긍정단어 비율 계산

   ![그림3](https://user-images.githubusercontent.com/50936176/147208783-bf663f47-0c26-4fe0-abca-6b458962e7a1.png)

   다낭과 홍콩이 비교적 높은 긍정도를 보였고, 후쿠오카와 세부가 비교적 낮은 긍정도를 보임

</br>

3. 다낭과 홍콩의 워드클라우드 분석

   `<홍콩>`

   ![그림5](https://user-images.githubusercontent.com/50936176/147208988-1868e4f5-3b6f-4488-a977-2b195958401c.png)

   `<다낭>`

   ![그림6](https://user-images.githubusercontent.com/50936176/147208996-51e2839c-9820-45da-8d84-10c6d01109da.png)

   키워드 상에서 ‘할인, 최고, 재미, 맛집’이라는 키워드가 돋보임

</br>

4. 후쿠오카와 세부의 워드클라우드 분석

   `<세부>`

   ![그림4png](https://user-images.githubusercontent.com/50936176/147209321-450db9d7-83d3-4fb8-a9dd-84e703eda04a.png)

   `<후쿠오카>`

   ![그림7](https://user-images.githubusercontent.com/50936176/147209326-d5eb953a-1720-4195-afa3-578d2d743ec2.png)

   `'뭔가 비싸기도 하고 불편하기도 하고 위생도 걱정되었기 때문인듯 합니다, '사람 많을까봐 걱정했는데…'`

</br>

## Part 5 : 관광지별 주요 연관 키워드 분석을 통한 호감/비호감 요인 서칭

1. 관광지 도시별 키워드에 따른 중심성 계산 및 시각화(Degree Centrality, Closeness Centrality, Betweenness Centrality, Eigenvector Centrality)

   ` dir > ST_PROJ/sna.py`

   ```python
   # 중심성 별 상위 5개 출력
   degree_centrality = sorted(deg_cent, key=lambda x: x[1], reverse=True)[0:]
   closeness_centrality =sorted(closeness_cent, key=lambda x: x[1], reverse=True)[0:]
   betweeness_centrality = sorted(between_cent, key=lambda x: x[1], reverse=True)[0:]
   eigenvector_centrality = sorted(eigenvector, key=lambda x: x[1], reverse=True)[0:]

   cname = ['degree_cent','closeness_cent','betweeness_cent','eigenvec_cent']
   index = []
   result_deg = []
   result_clo = []
   result_bet = []
   result_eig = []
   for i in range(len(degree_centrality)):
      index.append(degree_centrality[i][0])
      result_deg.append(degree_centrality[i][1])
      result_clo.append(closeness_centrality[i][1])
      result_bet.append(betweeness_centrality[i][1])
      result_eig.append(eigenvector_centrality[i][1])

   td = {
      'deg_cent': result_deg,
      'clo_cent' : result_clo,
      'bet_cent' : result_bet,
      'eig_cent' : result_eig
   }


   df1 = pd.DataFrame(td)
   df1.index = index
   df1.index.names = ['word']

   # 내림차순 정렬
   plt.rc('font', family=fontprop)
   df1.plot(kind='barh',title='중심성 시각화')
   plt.savefig('Centrality.png')
   plt.show()
   ```

   ![Centrality](https://user-images.githubusercontent.com/50936176/147210131-a147c2c5-371e-4fbd-894f-b79e81451d3f.png)

   ➩ 각 노드 및 엣지의 특징을 알아볼 수 있도록 시각화의 필요성

   ➩ 가중치를 통해 노드와 엣지의 특징을 시각화 할 수 있도록 !

   </br>

2. 각 노드 및 엣지별 시각화

   각 노드 별로 중요도 및 등장 횟수 등을 수치화해 가중치로 만들어 노드에 적용

   ➩ 노드의 크기로 알아 볼 수 있도록 시각화

   각 엣지(선)은 각 도시 별로 가중치를 부여해 색깔을 나눔

   ➩ 엣지(선)의 색깔을 통해 얼마나 관련이 있는가 알아볼 수 있도록 시각화

   ```python
   for u, v, d in G.edges(data=True):
      d['weight'] = rd.random()

   edges, weights = zip(*nx.get_edge_attributes(G, 'weight').items())

   node_s = get_node_attributes(G,'nodesize')

   node_size = [v * 1.0 for v in node_s.values()]
   degree_dict = {** dict(G.degree), **node_s}

   pos = nx.spring_layout(G, k=0.6, iterations=50)
   nx.draw(G, pos=pos, node_size = [v * 20 for v in degree_dict.values()], edge_color=weights)
   ```

   </br>

3. 그래프 분석

   `dir > ST_PROJ/sna.py`

   ![그림9](https://user-images.githubusercontent.com/50936176/147561160-720343c0-5f3a-4af9-a607-9770c5d932f1.png)

   900개의 블로그 글의 제목별로 연결망 분석

   ➩ 일정 이상의 지지도를 가질 때 노드 표시하고,일정 이상의 신뢰도를 가질 때 링크 표시

   ➩ 모든 여행지에서 ‘맛집’ 키워드가 자주 등장

   ➩ 동남아 여행지들은 ‘골프’ 단어가 자주 등장하며, 동남아 골프관광을 보여줌

   ➩ ‘일상’ 이라는 키워드는 일본관련 키워드 하고만 높은 신뢰도를 보이는데, 이것은 지리/인문적 일본과의 밀접함을 보여줌

   ➩ 추가로, 낯선 단어 ‘버블’과 ‘트래블’간 confidence값이 크다는 것을 볼 수 있는데, 이는 코로나와 함께 등장한 ‘트래블 버블’로 보임

   `dir > ST_PROJ/citySNA.py`

   <img width="1062" alt="스크린샷 2021-12-28 오후 8 23 36" src="https://user-images.githubusercontent.com/50936176/147561493-ae788de4-fa54-43e4-87e8-b6c59498b174.png">

   ➩ 위에서 주장한 바들을 뒷받침하는 근거로 도시별로 지지도를 높여서 SNA 시도

   `dir > ST_PROJ/posnegSNA.py`

   ![긍정](https://user-images.githubusercontent.com/50936176/147561500-0729457d-8d9e-44ee-ba39-ec29558a9f65.png)

   ➩ 도시별 긍정단어 SNA

   ![부정](https://user-images.githubusercontent.com/50936176/147561497-c5fb7ead-4d28-40bb-b74b-bc5df28ff69a.png)

   ➩ 도시별 부정단어 SNA

   ![긍부정](https://user-images.githubusercontent.com/50936176/147561502-7c72f434-c8b2-41db-8b4c-eca5bab46f97.png)

   ➩ 도시별 긍/부정 단어 SNA

   </br>

## Part 6 : 결과 및 활용방안

### `동남아지역은 호텔, 골프, 투어와 연관성 높음`

➩ 가격경쟁력을 앞세운 럭셔리 여행개발이 필요

➩ 골프와 투어형 관광을 묶은 상품개발 필요

</br>

### `일본은 사진, 일상과 연관성이 높음`

➩ 투어형 관광개발 필요가 상대적으로 적음

➩ 자유여행과 일본의 일상 및 감성을 즐기는데 중점을 둔 교통권 및 숙박권 패키지개발이 필요

➩ 외국인의 한국관광을 발전시키기 위해 일본의 사례를 참고할 필요가 있음

➩ 가격경쟁력이 적은만큼 보다 일상과 감성에 중점을 둔 관광상품 개발이 필요

</br>

### `종합적으로 한국인에게 만족도가 높은 지역`

➩ 다낭, 홍콩

</br>

### `종합적으로 한국인에게 만족도가 낮은 지역`

➩ 후쿠오카, 세부

</br>

### `활용 방안 추가 제언`

➩ 모든 지역에서 ‘맛집’이라는 단어가 빈출도가 매우 높음

➩ 여행에서 식도락이 중요

➩ 우리나라도 관광개발을 위해서는 식도락 개발 및 홍보가 최우선적으로 필요

</br>

### `한계 및 후속연구 제언`

➩ 최근 90개의 글들은 대부분 코로나시대에 속하였으므로 애프터 코로나 시대에 적합한 분석이 필요

➩ 코로나시대에 여행이 제한적이었다는 점을 감안할 때, 데이터수집시 크롤링의 기준시점을 조정한다면 더 많은 인사이트 추출 가능
