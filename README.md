# 🪁 ST_Proj

2021-2 Hanyang University, Social Network Analysis and Text Mining Project

네이버 블로그 크롤링을 통한 국가 별 관광지 감정 분석 : 주요 10개 관광지의 호감도조사 및 호감요인 분석을 통한 마케팅 활용 방안 제시

---

## Part 1 : 데이터 수집

1. 한국인들이 사랑하는 주요 관광지(도시) 10개 선정

   `오사카 도쿄 방콕 후쿠오카 다낭 타이베이 홍콩 세부 하노이 삿포로`

   by 스카이스캐너(최대 비행 티켓팅 사이트)

   위 관광 도시에는 어떤 호감요인과 비호감요인이 존재하고, 트래버들의 마음을 이끈 것일까?

2. 네이버 블로그 크롤링 작업

   11월 25일 기준, '도시명 + 여행'으로 검색했을 때 나오는 90개의 블로그 글 수집
   (제목, 링크, 날짜, 본문)

   `dir > ST_PROJ/blogCrawling.py`

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
2. 불용어 / 한 글자 단어 제거

   `['방콕','세부','다낭','후쿠오카','하노이','홍콩','오사카','삿포로','타이페이','도쿄','대만','필리핀','베트남','일본','중국','태국','여행','타이베이','있는','이','그','잘','못','ㅋㅋ','ㅎㅎ','홍콩의','홍콩이’]`

3. 토큰화 작업

</br>

## Part 3 : 빈출단어 분석
