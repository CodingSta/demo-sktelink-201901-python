from telegram import ParseMode
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
import requests
from bs4 import BeautifulSoup
from jinja2 import Template


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


def 단어수_세기(문자열):
    return len(문자열.split())


def 글자수_세기(문자열):
    글자수 = 0
    for 한글자 in 문자열:
        # if 한글자 != ' ':
        # if 한글자 != ' ' and 한글자 != '\n' and 한글자 != '\r' and 한글자 != '\t':
        if 한글자 not in [' ', '\n', '\r', '\t']:
            글자수 += 1
    return 글자수


def start(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text

    try:
        if text.startswith('네이버 블로그 검색:'):
            검색어 = text[11:]
            post_list = 네이버_블로그_검색(검색어)
            
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
            response = template.render(검색어=검색어, post_list=post_list)

        elif text == '네이버 실검':
            검색어_리스트 = 네이버_실시간_검색어()
            rank = 1
            message_list = []
            for 검색어 in 검색어_리스트:
                message = '{} {}'.format(rank, 검색어)
                message_list.append(message)
                rank += 1
            response = '\n'.join(message_list)

        elif text.startswith('단어수 세어줘:'):
            문자열 = text[8:]
            단어수 = 단어수_세기(문자열)
            response = '단어는 {}개입니다.'.format(단어수)

        elif text.startswith('글자수 세어줘:'):
            문자열 = text[8:]
            글자수 = 글자수_세기(문자열)
            response = '글자는 {}개입니다.'.format(글자수)

        elif text == '야':
            response = '왜?'

        else:
            response = '니가 무슨 말 하는 지 모르겠어. :('
    except Exception as e:
        response = str(e)

    bot.send_message(chat_id=chat_id, text=response, parse_mode=ParseMode.HTML)


def main(token):
    bot = Updater(token=TOKEN)

    handler = CommandHandler('start', start)
    bot.dispatcher.add_handler(handler)

    handler = MessageHandler(Filters.text, echo)
    bot.dispatcher.add_handler(handler)

    bot.start_polling()

    print('running telegram bot ...')
    bot.idle()

# ...

if __name__ == '__main__':
    # TODO: 필요한 라이브러리 설치 : pip install python-telegram-bot
    # FIXME: 각자의 Token을 적용해주세요.
    TOKEN = "*********************************************"
    main(TOKEN)
