import requests
from bs4 import BeautifulSoup


def 네이버_블로그_검색(검색어):
    url = 'https://search.naver.com/search.naver'

    params = {
        'where': 'post',
        'sm': 'tab_jum',
        'query': 검색어,
    }
    
    res = requests.get(url, params=params)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    
    tag_list = soup.select('#elThumbnailResultArea .sh_blog_title')
    
    post_list = []
    for tag in tag_list:
        post_url = tag['href']
        post_title = tag.text
        post_list.append({
            'url': post_url,
            'title': post_title,
        })
    
    return post_list


def 네이버_실시간_검색어():
    url = 'http://naver.com'
    응답 = requests.get(url)
    html = 응답.text

    soup = BeautifulSoup(html, 'html.parser')
    tag_list = soup.select('.PM_CL_realtimeKeyword_rolling .ah_k')

    keyword_list = []
    for tag in tag_list:
        keyword_list.append(tag.text)
    return keyword_list
