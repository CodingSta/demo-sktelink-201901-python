from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler

import requests
from bs4 import BeautifulSoup

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


def start(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text

    if text.startswith('단어수 세어줘:'):
        문자열 = text[8:]
        단어수 = len(문자열.split())  # int 타입
        response = '단어수는 {}개입니다.'.format(단어수)

    elif text == '네이버 실검':
        keyword_list = 네이버_실시간_검색어()
        response = '\n'.join(keyword_list)

    elif text.startswith('네이버에서 찾아줘:'):
        검색어 = text[10:]
        # TODO: 네이버에서 검색결과를 찾을 수 있어요. !!!
        response = '검색결과가 없습니다.'

    elif text == '야':
        response = '왜?'

    elif text == '네이버에서 맛집 찾아줘.':
        response = '니가 찾아봐. http://naver.com'

    else:
        response = '니가 무슨 말 하는 지 모르겠어.'

    bot.send_message(chat_id=chat_id, text=response)


def main(token):
    bot = Updater(token=TOKEN)

    handler = CommandHandler('start', start)
    bot.dispatcher.add_handler(handler)

    handler = MessageHandler(Filters.text, echo)
    bot.dispatcher.add_handler(handler)

    bot.start_polling()

    print('running telegram bot ...')
    bot.idle()


if __name__ == '__main__':
    # TODO: 필요한 라이브러리 설치 : pip install python-telegram-bot
    # FIXME: 각자의 Token을 적용해주세요.
    TOKEN = "*********************************************"
    main(TOKEN)

