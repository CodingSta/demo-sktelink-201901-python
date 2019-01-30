import re

from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler

# from sktelink.tasks import 단어수_세기, 네이버_검색
from sktelinklibs import tasks


def start(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text

    task_class_list = [
        tasks.단어수_세기,
        # tasks.네이버_검색,
        tasks.네이버_실검,
    ]

    try:
        for task_class in task_class_list:
            task = task_class(text)
            if task.is_matched():
                response = task.make_response()
                break
        else:  # break없이 마지막 루프까지 돌았을 때
            response = '니가 무슨 말 하는 지 모르겠어.'

    except Exception as e:
        response = str(e)

    bot.send_message(chat_id=chat_id, text=response)


#     elif text == '네이버 실검':
#         keyword_list = 네이버_실시간_검색어()
#         response = '\n'.join(keyword_list)

#     elif text.startswith('네이버:'):
#         검색어 = text[4:]
#         post_list = 네이버_블로그_검색(검색어)  # 개별: url, title

#         # 버전 1
#         # message_list = []
#         # for post in post_list:
#         #     # lines = '{}\n{}'.format(post['title'], post['url'])
#         #     message = '{title}\n{url}'.format(**post)
#         #     message_list.append(message)
#         # response = '\n\n'.join(message_list)

#         # 버전 2
#         template = Template('''{{ 검색어 }} 검색결과
# {% for post in post_list %}
# {{ post.title }}
# {{ post.url }}
# {% endfor %}''')
#         response = template.render(검색어=검색어, post_list=post_list)

#     elif text == '야':
#         response = '왜?'

#     elif text == '네이버에서 맛집 찾아줘.':
#         response = '니가 찾아봐. http://naver.com'

#     else:
#         response = '니가 무슨 말 하는 지 모르겠어.'

#     bot.send_message(chat_id=chat_id, text=response)


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
