import telegram

# FIXME: 여러분의 Bot Token
TOKEN = "*********************************************"

bot = telegram.Bot(token=TOKEN)

# FIXME: 여러분의 CHAT-ID
chat_id = '********'

bot.sendMessage(chat_id=chat_id, text="안녕!!!!!!!!!")

