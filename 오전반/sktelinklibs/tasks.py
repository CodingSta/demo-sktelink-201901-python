import re
from sktelinklibs.naver import 네이버_블로그_검색, 네이버_실시간_검색어


class 단어수_세기:
    def __init__(self, text):
        self.text = text
        self.matched = None

    def is_matched(self):
        return self.text.startswith('단어수 세어줘:')

    def make_response(self):
        keyword = self.text[8:]
        단어수 = len(keyword.split())  # int 타입
        response = '단어수는 {}개입니다.'.format(단어수)
        return response


class 네이버_검색:
    def __init__(self, text):
        self.text = text
        self.matched = None

    def is_matched(self):
        네이버_검색_패턴 = r"네이버에서(.+)찾아"
        self.matched = re.match(네이버_검색_패턴, self.text)
        return bool(self.matched)

    def make_response(self):    
        keyword = self.matched.group(1)
        post_list = 네이버_블로그_검색(keyword)
        message_list = []
        for post in post_list:
            # lines = '{}\n{}'.format(post['title'], post['url'])
            message = '{title}\n{url}'.format(**post)
            message_list.append(message)
        response = '\n\n'.join(message_list)
        return response


class 네이버_실검:
    def __init__(self, text):
        self.text = text

    def is_matched(self):
        return self.text == '네이버 실검'

    def make_response(self):    
        keyword_list = 네이버_실시간_검색어()
        response = '\n'.join(keyword_list)
        return response
