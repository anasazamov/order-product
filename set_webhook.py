from telegram import Bot

bot = Bot('7451785085:AAG3E1F_C86kyJ5f23ak0_3-CchGxPIUoig')

print(bot.delete_webhook())
print(bot.set_webhook('https://api.xirurgiya-pro.uz/bot/'))