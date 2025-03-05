# product/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from product.models import Order, Contact
import logging
from bot.views import updater
from bot.models import BotAdmin
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

bot = updater.bot

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Order)
def order_created_signal(sender, instance, created, **kwargs):
    if created:
        bot_admins = BotAdmin.objects.filter(is_active=True)
        product_name = instance.product.name
        order_id = instance.pk
        region = instance.region
        keyboard = [[
            InlineKeyboardButton("📦 Посмотреть заказ", callback_data=f"order_{order_id}"),
        ]]
        
        for admin in bot_admins:
            message = (
                f"🛒 <b>Новый заказ!</b>\n"
                f"📌 <b>Товар:</b> {product_name}\n"
                f"📍 <b>Регион:</b> {region}\n"
                f"🔍 Нажмите, чтобы посмотреть детали заказа."
            )
            bot.send_message(chat_id=admin.chat_id, text=message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")


@receiver(post_save, sender=Contact)
def contact_created_signal(sender, instance, created, **kwargs):
    if created:
        bot_admins = BotAdmin.objects.filter(is_active=True)
        name = instance.name
        phone = instance.phone
        contact_id = instance.pk
        keyboard = [[
            InlineKeyboardButton("📩 Просмотреть сообщение", callback_data=f"contact_{contact_id}"),
        ]]
        
        for admin in bot_admins:
            message = (
                f"📬 <b>Новое сообщение!</b>\n"
                f"👤 <b>Имя:</b> {name}\n"
                f"📞 <b>Телефон:</b> {phone}\n"
                f"🔍 Нажмите, чтобы просмотреть детали."
            )
            bot.send_message(chat_id=admin.chat_id, text=message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
