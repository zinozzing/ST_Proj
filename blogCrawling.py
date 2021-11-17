import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote


def delete_iframe(url):
    headers = {"User-Agent":"mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/537.36 (khtml, like gecko) chrome/95.0.4638.69 safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status() # 예외처리
    soup = BeautifulSoup(res.text, "lxml") # lxml 방식의 파싱
    src_url = "https://blog.naver.com/" + soup.iframe["src"]
    return src_url


# 네이버블로그 본문 스크래핑
def text_scraping(url):
    headers = {"User-Agent":"mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/537.36 (khtml, like gecko) chrome/95.0.4638.69 safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status() # 예외처리
    soup = BeautifulSoup(res.text, "lxml") # lxml 방식의 파싱

    if soup.find("div", attrs={"class":"se-main-container"}):
        text = soup.find("div", attrs={"class":"se-main-container"}).get_text()
        text = text.replace("\n","") #공백 제거
        return text

    elif soup.find("div", attrs={"id":"postViewArea"}):
        text = soup.find("div", attrs={"id":"postViewArea"}).get_text()
        text = text.replace("\n","")
        return text
    else:
        return "네이버 블로그는 맞지만, 확인불가"


def main_crawling(end,option,keyword):
    for i in range(1,end*30,30):
        query = str(keyword)
        base_url = 'https://search.naver.com/search.naver?where=post&query='
        url = base_url + quote(query) + '&sm=tab_opt&date_option='+str(option)+'&start=' + str(i) # date_option 0 = 전체 , 1 = 1시간, 2 = 1일, 3 = 1주, 4 = 1개월, 5 = 3개월, 6 = 6개월, 7 = 1년 

        headers = {"User-Agent":"mozilla/5.0 (macintosh; intel mac os x 10_15_7) applewebkit/537.36 (khtml, like gecko) chrome/95.0.4638.69 safari/537.36"}
        res = requests.get(url, headers=headers)
        res.raise_for_status() # 문제시 프로그램 종료
        soup = BeautifulSoup(res.text, "lxml")

        posts = soup.find_all("div", attrs={"class":"total_area"})

        for post in posts:
            print("-"*50)
            # 제목 크롤링
            post_title = post.find('a',class_='api_txt_lines total_tit').get_text()
            print("제목 :",post_title)
            
            # 링크 크롤링
            post_link = post.find("a",class_='api_txt_lines total_tit')['href']
            print("link :", post_link)
            
            # 날짜 크롤링
            post_time = post.find("span",class_='sub_time sub_txt').get_text()
            print("date :", post_time)
            
            
            blog_p = re.compile("blog.naver.com")
            blog_m = blog_p.search(post_link)


            # 본문 내용 크롤링
            if blog_m:
                blog_text = text_scraping(delete_iframe(post_link))
                print("<본문>")
                print(blog_text)
                
            else:
                print("카페 및 포스트 : 확인 불가")

            print("-"*50)
        

num = int(input("1페이지부터 원하는 페이지의 범위: "))
opt = input("원하는 데이터의 수집 기간(ex. 0 = 전체 , 1 = 1시간, 2 = 1일, 3 = 1주, 4 = 1개월, 5 = 3개월, 6 = 6개월, 7 = 1년): ")
keyw = input("크롤링을 원하는 단어: ")
main_crawling(num,opt,keyw)