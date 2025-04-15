# product/signals.py
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from product.models import Order, Contact, OrderItem
import logging
from bot.views import updater
from bot.models import BotAdmin
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

bot = updater.bot

logger = logging.getLogger(__name__)

@receiver(post_save, sender=OrderItem)
def order_item_created_signal(sender, instance, created, **kwargs):
    print(f"OrderItem created: {instance}")
    if created:
        order = instance.order
        bot_admins = BotAdmin.objects.filter(is_active=True)
        product_names = ", ".join(
            [f"{item.product.name} x {item.quantity}" for item in order.order_items.all()]
        )
        order_id = order.pk
        region = order.get_region_display()
        keyboard = [[
            InlineKeyboardButton("📦 Посмотреть заказ", callback_data=f"order_{order_id}"),
        ]]
        message = (
            f"🛒 <b>Новый заказ!</b>\n"
            f"📌 <b>Товар:</b> {product_names}\n"
            f"📍 <b>Регион:</b> {region}\n"
            f"🔍 Нажмите, чтобы посмотреть детали заказа."
        )
        for admin in bot_admins:
            bot.send_message(
                chat_id=admin.chat_id,
                text=message,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="HTML"
            )


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
