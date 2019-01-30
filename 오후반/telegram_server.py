from telegram import ParseMode
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler

from sktelinklibs import tasks


def start(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id=chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text

    # 아직 동작하지 않는 코드
    # task_class_list = []
    # for task in dir(tasks):
    #     try:
    #         if issubclass(tasks.BaseTask, task):
    #             print("!!!", task)
    #             task_class_list.append(task)
    #     except TypeError:
    #         pass

    TASK_CLASS_LIST = [
        tasks.야,
        tasks.단어수_세기,
        tasks.글자수_세기,
        tasks.네이버_실검,
        tasks.네이버_검색,
    ]

    try:
        for task_class in TASK_CLASS_LIST:
            task = task_class(text)
            if task.is_matched():
                response = task.make_response()
                break
        else:  # 현재 루프가 break없이 마지막까지 돌았을 때
            response = '니가 무슨 말 하는 지 모르겠어. :('
    except Exception as e:
        response = str(e)

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

# ...

if __name__ == '__main__':
    # TODO: 필요한 라이브러리 설치 : pip install python-telegram-bot
    # FIXME: 각자의 Token을 적용해주세요.
    TOKEN = "*********************************************"
    main(TOKEN)
