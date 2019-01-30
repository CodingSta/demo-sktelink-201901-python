import re
from jinja2 import Template
from sktelinklibs.naver import 네이버_블로그_검색, 네이버_실시간_검색어


class BaseTask:
    def __init__(self, text):
        self.text = text


class 야(BaseTask):
    def is_matched(self):
        return self.text == '야'
    
    def make_response(self):
        return '왜?'


class 단어수_세기(BaseTask):
    def is_matched(self):
        return self.text.startswith('단어수 세어줘:')
    
    def make_response(self):
        문자열 = self.text[8:]
        단어수 = len(문자열.split())
        response = '단어는 {}개입니다.'.format(단어수)
        return response


class 글자수_세기(BaseTask):
    def is_matched(self):
        return self.text.startswith('글자수 세어줘:')
    
    def make_response(self):
        문자열 = self.text[8:]
        글자수 = 0
        for 한글자 in 문자열:
            if 한글자 not in [' ', '\n', '\r', '\t']:
                글자수 += 1
        response = '글자는 {}개입니다.'.format(글자수)
        return response


class 네이버_실검(BaseTask):
    def is_matched(self):
        return self.text == '네이버 실검'

    def make_response(self):
        검색어_리스트 = 네이버_실시간_검색어()
        message_list = []
        for rank, 검색어 in enumerate(검색어_리스트, 1):
            message = '{} {}'.format(rank, 검색어)
            message_list.append(message)
        response = '\n'.join(message_list)
        return response


class 네이버_검색(BaseTask):
    def __init__(self, text):
        super().__init__(text)
        self.keyword = None
    
    def is_matched(self):
        네이버_검색_패턴 = r"네이버에서(.+)찾아"

        matched = re.match(네이버_검색_패턴, self.text)
        if matched:
            self.keyword = matched.group(1)
        return bool(matched)
    
    def make_response(self):
        post_list = 네이버_블로그_검색(self.keyword)

        # 타입 1
        # message_list = []
        # for post in post_list:
        #     # message = '{}\n{}'.format(post['title'], post['url'])
        #     message = '{title}\n{url}'.format(**post)
        #     message_list.append(message)
        # response = '\n\n'.join(message_list)

        # 타입 2
        template = Template('''검색어 "{{ 검색어 }}"에 대한 검색결과

{% for post in post_list -%}
<a href="{{ post.url }}">{{ post.title }}</a>
{% endfor %}''')
        response = template.render(검색어=self.keyword, post_list=post_list)

        return response
