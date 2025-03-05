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
        name = instance.product.name
        id = instance.pk
        region = instance.region
        keyboard = [[
            InlineKeyboardButton("Buyurtmani Ko'rish", callback_data=f"order_{id}"),
        ]]
        
        for admin in bot_admins:
            bot.send_message(chat_id=admin.chat_id, text=f"🛒 Yangi buyurtma qo'shildi: {name} - {region}", reply_markup=InlineKeyboardMarkup(keyboard))

@receiver(post_save, sender=Contact)
def contact_created_signal(sender, instance, created, **kwargs):
    if created:
        bot_admins = BotAdmin.objects.filter(is_active=True)
        name = instance.name
        phone = instance.phone
        keyboard = [[
            InlineKeyboardButton("Xabarni ko'rish", callback_data=f"contact_{instance.pk}"),
        ]]
        for admin in bot_admins:
            bot.send_message(chat_id=admin.chat_id, text=f"📝 Yangi xabar qo'shildi: {name} - {phone}", reply_markup=InlineKeyboardMarkup(keyboard))