import os 
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
from bot.callback import (
    start,
    admin_permission,
    allow_access,
    view_order_types,
    view_order_regions,
    view_orders_by_region_status,
    view_order,
    order_statused,
    back_to_start,
    view_contacts,
    view_contact_detail
)

updater = Updater('TOKEN', use_context=True)
dispatcher = updater.dispatcher

def main():
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.regex('🔑 Ruxsat so\'rash'), admin_permission))
    dispatcher.add_handler(CallbackQueryHandler(allow_access, pattern='^allow_access_|^deny_access_'))
    dispatcher.add_handler(MessageHandler(Filters.regex('🛒 Buyurtmalarni korish'), view_order_types))
    dispatcher.add_handler(CallbackQueryHandler(view_order_regions, pattern='^order_status_'))
    dispatcher.add_handler(CallbackQueryHandler(view_orders_by_region_status, pattern='^region_'))
    dispatcher.add_handler(CallbackQueryHandler(view_order, pattern='^order_'))
    dispatcher.add_handler(CallbackQueryHandler(order_statused, pattern='^(st_chat_|st_success_|st_cancel_|st_rechat_)'))
    dispatcher.add_handler(CallbackQueryHandler(back_to_start, pattern='^back_to_start_'))
    dispatcher.add_handler(MessageHandler(Filters.regex('📝 Xabarlarni korish'), view_contacts))
    dispatcher.add_handler(CallbackQueryHandler(view_contact_detail, pattern='^contact_'))
    dispatcher.add_handler(CallbackQueryHandler(back_to_start, pattern='^back_to_start'))

    print('Bot is running...')
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

    