from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from product.models import BlogType, Blog, Product, Order, Contact
from telegram.ext import CallbackContext
from django.core.paginator import Paginator

from bot.models import BotAdmin

def start(update: Update, context: CallbackContext):

    chat_id = update.effective_chat.id

    if BotAdmin.objects.filter(chat_id=chat_id, is_active=True).exists():
        update.message.reply_text(
            'Здравствуйте, добро пожаловать в бота для заказов и уведомлений!',
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton('🛒 Просмотреть заказы'), KeyboardButton('📝 Просмотреть сообщения')]],
                resize_keyboard=True
            )
        )
        return

    update.message.reply_text('Чтобы использовать бота, запросите разрешение у администратора!', reply_markup=ReplyKeyboardMarkup([[KeyboardButton('🔑 Запросить доступ')]], resize_keyboard=True))
    return

def admin_permission(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    fullname = update.effective_chat.full_name
    username = update.effective_chat.username

    if BotAdmin.objects.filter(chat_id=chat_id).exists():
        update.message.reply_text('Вы уже пытались запросить разрешение!')
        return

    BotAdmin.objects.create(chat_id=chat_id, fullname=fullname, username=username, is_active=False)
    bot_admin = BotAdmin.objects.filter(is_active=True).values('chat_id', 'fullname', 'username')
    for admin in bot_admin:
        context.bot.send_message(admin['chat_id'], f'Пользователь запросил разрешение администратора! \n\nChat ID: {chat_id}\nПолное имя: {fullname}\nИмя пользователя: {username}', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Разрешить', callback_data=f'allow_access_{chat_id}'), InlineKeyboardButton('Отклонить', callback_data=f'deny_access_{chat_id}')]]))
    update.message.reply_text('Запрос успешно принят! Пожалуйста, подождите, вам скоро дадут разрешение!')

def allow_access(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    if data.startswith('allow_access_'):
        chat_id = data.split('_')[2]
        BotAdmin.objects.filter(chat_id=chat_id).update(is_active=True)
        context.bot.send_message(chat_id, 'Администратор дал вам разрешение!\n\nОтправьте команду /start для использования бота!')
        query.edit_message_text('Разрешение предоставлено!')

    elif data.startswith('deny_access_'):
        chat_id = data.split('_')[2]
        BotAdmin.objects.filter(chat_id=chat_id).delete()
        context.bot.send_message(chat_id, 'Администратор не дал вам разрешение!')
        query.edit_message_text('Разрешение не предоставлено!')

def view_order_types(update: Update, context: CallbackContext):
    order_types = Order.STATUS_TYPES
    order_types_buttons = []
    for i in range(0, len(order_types), 2):
        buttons = []
        for j in range(2):
            if i + j < len(order_types):
                status_code, status_name = order_types[i + j]
                order_count = Order.objects.filter(status=status_code).count()
                buttons.append(InlineKeyboardButton(f"{status_name} ({order_count})", callback_data=f"order_status_{status_code}"))
        order_types_buttons.append(buttons)

    order_types_buttons.append([InlineKeyboardButton('🔙 Назад', callback_data='back_to_start')])

    update.message.reply_text(
        'Выберите статус заказа:',
        reply_markup=InlineKeyboardMarkup(order_types_buttons)
    )

def view_order_regions(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data.startswith("order_status_"):
        status_code = query.data.split("_")[2]
        regions = Order.UZB_REGIONS

        region_buttons = []
        for i in range(0, len(regions), 2):
            buttons = []
            for j in range(2):
                if i + j < len(regions):
                    region_code, region_name = regions[i + j]
                    region_count = Order.objects.filter(status=status_code, region=region_code).count()
                    buttons.append(InlineKeyboardButton(f"{region_name} ({region_count})", callback_data=f"region_{region_code}_{status_code}"))
            region_buttons.append(buttons)
        region_buttons.append([InlineKeyboardButton('🔙 Назад', callback_data='back_to_start_')])

        query.edit_message_text(
            'Количество заказов по регионам:',
            reply_markup=InlineKeyboardMarkup(region_buttons)
        )


def view_orders_by_region_status(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data.startswith("region_"):
        _, region_code, status_code = query.data.split("_")

        orders = Order.objects.filter(region=region_code, status=status_code)

        if not orders.exists():
            query.edit_message_text("Заказы по этому региону и статусу не найдены.")
            return

        page_number = int(context.args[0]) if context.args else 1
        paginator = Paginator(orders, 10)

        if page_number < 1 or page_number > paginator.num_pages:
            page_number = 1

        current_page = paginator.page(page_number)

        keyboard = [
            [InlineKeyboardButton(f"Продукт: {order.product.name}", callback_data=f"order_{order.pk}")]
            for order in current_page
        ]

        navigation_buttons = []
        if current_page.has_previous():
            navigation_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"region_{region_code}_{status_code}_{page_number - 1}"))

        if current_page.has_next():
            navigation_buttons.append(InlineKeyboardButton("Вперёд ➡️", callback_data=f"region_{region_code}_{status_code}_{page_number + 1}"))

        if navigation_buttons:
            keyboard.append(navigation_buttons)

        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data=f"order_status_{status_code}")])
        try:
            query.edit_message_text("Список заказов:", reply_markup=InlineKeyboardMarkup(keyboard))
        except:
            query.message.delete()
            query.message.reply_text("Список заказов:", reply_markup=InlineKeyboardMarkup(keyboard))
        

def view_order(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data.startswith("order_"):
        query.message.delete()
        order_id = query.data.split("_")[-1]
        order = Order.objects.get(id=order_id)

        order_status_buttons = [[InlineKeyboardButton("Говорить", callback_data=f"st_chat_{order_id}"), InlineKeyboardButton("Переговоры", callback_data=f"st_rechat_{order_id}")],
                                [InlineKeyboardButton("Завершить успешно", callback_data=f"st_success_{order_id}"), InlineKeyboardButton("Отменено", callback_data=f"st_cancel_{order_id}")],
                                [InlineKeyboardButton("🔙 Назад", callback_data=f"region_{order.region}_{order.status}")]]

        if order.product.photo:
            return context.bot.send_photo(
                chat_id=query.message.chat_id,
                photo=order.product.photo.file,
                caption=f"Заказ: {order.product.name}\n"
                f"Клиент: {order.client_name}\n"
                f"Телефон: {order.phone_number}\n"
                f"Статус заказа: {order.get_status_display()}\n"
                f"Регион: {order.get_region_display()}\n"
                f"Создано: {order.created_at.strftime('%d-%m-%Y %H:%M')}\n"
                f"Обновлено: {order.updated_at.strftime('%d-%m-%Y %H:%M')}",
                reply_markup=InlineKeyboardMarkup(order_status_buttons)
            )

def order_statused(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data.startswith("st_chat_"):
        order_id = query.data.split("_")[2]
        order = Order.objects.get(pk=order_id)
        order.status = "cn"
        order.save()
        query.message.delete()
        query.message.reply_text("Идёт общение с клиентом!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data=f"back_to_start")]]))

    elif query.data.startswith("st_rechat_"):
        order_id = query.data.split("_")[2]
        order = Order.objects.get(pk=order_id)
        order.status = "rc"
        order.save()
        query.message.delete()
        query.message.reply_text("Оставлено для повторного общения с клиентом!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data=f"back_to_start")]]))

    elif query.data.startswith("st_success_"):
        order_id = query.data.split("_")[2]
        order = Order.objects.get(pk=order_id)
        order.status = "cd"
        order.save()
        query.message.delete()
        query.message.reply_text("Заказ успешно завершён!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data=f"back_to_start")]]))

    elif query.data.startswith("st_cancel_"):
        order_id = query.data.split("_")[2]
        order = Order.objects.get(pk=order_id)
        order.status = "cnd"
        order.save()
        query.message.delete()
        query.message.reply_text("Заказ отменён!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data=f"back_to_start")]]))

def back_to_start(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    query.message.delete()
    query.message.reply_text(
        'Добро пожаловать в бота для заказов и уведомлений!',
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton('🛒 Просмотр заказов'), KeyboardButton('📝 Просмотр сообщений')]],
            resize_keyboard=True
        )
    )


def view_contacts(update: Update, context: CallbackContext):
    page_number = int(context.args[0]) if context.args else 1

    contacts = Contact.objects.all()

    if not contacts.exists():
        update.message.reply_text("Сообщения не найдены!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")]]))
        return

    paginator = Paginator(contacts, 10)

    if page_number < 1 or page_number > paginator.num_pages:
        page_number = 1

    current_page = paginator.page(page_number)

    keyboard = [
        [InlineKeyboardButton(f"{contact.name} ({contact.phone})", callback_data=f"contact_{contact.id}")]
        for contact in current_page
    ]

    navigation_buttons = []

    if current_page.has_previous():
        navigation_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"contacts_page_{page_number - 1}"))

    if current_page.has_next():
        navigation_buttons.append(InlineKeyboardButton("Вперёд ➡️", callback_data=f"contacts_page_{page_number + 1}"))

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    update.message.reply_text("Список сообщений:", reply_markup=InlineKeyboardMarkup(keyboard))


def view_contact_detail(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    contact_id = int(query.data.split("_")[1])
    contact = Contact.objects.get(id=contact_id)

    message = f"Имя: {contact.name}\nТелефон: {contact.phone}\nСообщение: {contact.message}"

    query.edit_message_text(message, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back_to_start")]]))
