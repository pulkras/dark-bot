import telebot
import config 
from telebot import types
import time
from telethon import TelegramClient, events
import mysql.connector
from mysql.connector import Error
import threading

from admin import admin_panel, callback_handler, add_promo_code, delete_promo_code, view_promocodes

bot = telebot.TeleBot(config.TOKEN)
client = TelegramClient('/home/botuser/test_bot/dark_bot/daerkmem_bot', config.API_ID, config.API_HASH)

# CHAT_ID = '-1002258778202'  # ID вашего чата
CHANNEL_ID = bot.get_chat("@darkmemtoken").id  # ID вашего канала
channel_name = 'darkmemtoken'
balance = None
approved = False
global language
language = "RU"


# Подключение к базе данных MySQL
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='dark',
            user='botuser',
            password=config.PASSWORD
        )
        if connection.is_connected():
            print("Соединение с базой данных установлено")
            return connection
    except Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

@bot.callback_query_handler(func=lambda call: call.data == "approval")
def check_subscription(call):
    user_id = call.from_user.id

    try:
        # Проверка подписки на чат
        channel_member = bot.get_chat_member(CHANNEL_ID, user_id)

        if channel_member.status in ['участник', 'member', 'administrator', 'creator']:
            global approved
            approved = True
            if language == "RU":
            # Пользователь подписан и на чат, и на канал
                bot.send_message(call.message.chat.id, "Вы подписаны на канал. Проверка пройдена.")
            elif language == "EN":
                bot.send_message(call.message.chat.id, "Checking is approved")
            is_approved(call.message)
        else:
            if language == "RU":
            # Пользователь не подписан на один или оба ресурса
                bot.send_message(call.message.chat.id, "Вы не подписаны на канал.")
            elif language == "EN":
                bot.send_message(call.message.chat.id, "You didn't subscribe channel")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Ошибка API Telegram: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "nft")
def check_nft_ref(call):
    if language == "RU":
       bot.send_message(call.message.chat.id, "🙁На данный момент вам не хватает рефералов для получения уникальной NFT.\n\nДля получения персональной NFT вы должны пригласить 5+ рефералов через свою пригласительную ссылку.")
    elif language == "EN":
        bot.send_message(call.message.chat.id, "🙁At the moment you don’t have enough referrals to receive a unique NFT.\n\nTo receive a personalized NFT, you must invite 5+ referrals through your invite link.")


@bot.message_handler(commands=['admin'])
def admin_command(message):
    admin_panel(message, bot)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    callback_handler(call, bot)

@bot.message_handler(func=lambda message: message.text == "Добавить промокод")
def add_promo(message):
    add_promo_code(message, bot)

@bot.message_handler(func=lambda message: message.text == "Удалить промокод")
def delete_promo(message):
    delete_promo_code(message, bot)

@bot.message_handler(func=lambda msg: msg.text == "Просмотр промокодов")
def handle_view_promocodes(msg):
    view_promocodes(msg, bot)
# Добавление или обновление пользователя и его баллов
def update_user_points(username, points, referral=False):
    connection = create_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (username, points, referrals) VALUES (%s, %s, %s)", (username, points, 0))
        else:
            if referral:
                # Увеличиваем количество рефералов на 1
                cursor.execute("UPDATE users SET referrals = referrals + 1 WHERE username = %s", (username,))
            cursor.execute("UPDATE users SET points = points + %s WHERE username = %s", (points, username))
        connection.commit()
    except Error as e:
        print(f"Ошибка работы с таблицей пользователей: {e}")
    finally:
        cursor.close()
        connection.close()


def is_approved(message):
    if language == "RU":
        first_markup = types.InlineKeyboardMarkup(row_width=2)
        our_news = types.InlineKeyboardButton("Новости", callback_data="news", url="https://t.me/darkmemtoken")
    
        first_markup.add(our_news)
    
        second_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        wallet = types.KeyboardButton("Кошелек")
        referal = types.KeyboardButton("Реф.")
        lang = types.KeyboardButton("Язык")
        promo = types.KeyboardButton("Промокод")
        admin = types.KeyboardButton("Админка")

        second_markup.add(wallet, referal, lang, promo, admin)
        bot.send_message(message.chat.id, "...", reply_markup=second_markup)
        bot.send_photo(message.chat.id, open('images/dark_welcome.jpg', 'rb'), caption="Привет!\n\nДобро пожаловать в официального бота $DARK! 🎉Здесь вы можете получать монеты $DARK за свою активность. Все просто: реагируйте на посты и подписывайтесь на наш канал Dark, чтобы получать вознаграждения. Чем больше активности — тем больше монет $DARK у вас на счету. 🚀\n\nНачнем?", parse_mode="html", reply_markup=first_markup)
    elif language == "EN":
        first_markup = types.InlineKeyboardMarkup(row_width=2)
        our_news = types.InlineKeyboardButton("News", callback_data="news", url="https://t.me/darkmemtoken")
    
        first_markup.add(our_news)
    
        second_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        wallet = types.KeyboardButton("Wallet")
        referal = types.KeyboardButton("REF")
        lang = types.KeyboardButton("LANG")
        promo = types.KeyboardButton("PromoCode")
        admin = types.KeyboardButton("Admin")

        second_markup.add(wallet, referal, lang, promo, admin)
        bot.send_message(message.chat.id, "...", reply_markup=second_markup)
        bot.send_photo(message.chat.id, open('images/dark_welcome.jpg', 'rb'), caption="Hi!\n\nWelcome to the official $DARK bot! 🎉Here you can get $DARK coins for your activity. It's simple: react to posts and subscribe to our Dark channel to get rewards. The more activity - the more $DARK coins you have in your account. 🚀 \n\nShall we get started?", parse_mode="html", reply_markup=first_markup)

def choose_lang(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        russian = types.KeyboardButton("RU")
        english = types.KeyboardButton("EN")

        markup.add(russian, english)

        bot.send_message(message.chat.id, "Please specify language:", parse_mode="html", reply_markup=markup)

def subscriptions(message):
    if  not approved:
        if message.text == "RU":
            global language
            language = "RU"
            markup = types.InlineKeyboardMarkup(row_width=2)
            our_chat = types.InlineKeyboardButton("Чат", callback_data="chat", url="https://t.me/+IhtDEuLaKpZlZDky")
            our_channel = types.InlineKeyboardButton("Канал", callback_data="channel", url="https://t.me/darkmemtoken")
            approval = types.InlineKeyboardButton("Проверка", callback_data="approval")

            markup.add(our_chat, our_channel, approval)

            bot.send_message(message.chat.id, "Перед тем как использовать бот, подпишитесь к нам на канал и чат :)", parse_mode="html", reply_markup=markup)
        elif message.text == "EN":
            language = "EN"
            markup = types.InlineKeyboardMarkup(row_width=2)
            our_chat = types.InlineKeyboardButton("Chat", callback_data="chat", url="https://t.me/+IhtDEuLaKpZlZDky")
            our_channel = types.InlineKeyboardButton("$DARK", callback_data="channel", url="https://t.me/darkmemtoken")
            approval = types.InlineKeyboardButton("Checking", callback_data="approval")

            markup.add(our_chat, our_channel, approval)

            bot.send_message(message.chat.id, "Subscribe to our chat and channel before using bot :)", parse_mode="html", reply_markup=markup)
    else:
        is_approved(message)

def wallet(message):
    if message.text == "Кошелек" or message.text == "Wallet":
        balance = 20
        if language == "RU":
            first_markup = types.InlineKeyboardMarkup()
            my_nft = types.InlineKeyboardButton("Мои NFT", callback_data="nft")
        
            first_markup.add(my_nft)
        
            second_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Назад")
    
            second_markup.add(back)
            bot.send_message(message.chat.id, "...", reply_markup=second_markup)
            bot.send_photo(message.chat.id, open('images/dark_wallet.jpg', 'rb'), caption="💸 Ваш баланс:  DARK " + str(balance) + "\n\nВаш кошелек:\n\n👨‍👨‍👦‍👦Приглашайте друзей, чтобы зарабатывать больше")
        elif language == "EN":
            first_markup = types.InlineKeyboardMarkup()
            my_nft = types.InlineKeyboardButton("My NFT", callback_data="nft")
        
            first_markup.add(my_nft)
        
            second_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Back")
    
            second_markup.add(back)
            bot.send_message(message.chat.id, "...", reply_markup=second_markup)
            bot.send_photo(message.chat.id, open('images/dark_wallet.jpg', 'rb'), caption="💸 Your balance: DARK " + str(balance) + "\n\nYour wallet:\n\n👨‍👨‍👦‍👦Invite friends to earn more")

# Обработчик нажатия на кнопку "Промокод" (или "PromoCode")
@bot.message_handler(func=lambda message: message.text in ["Промокод", "PromoCode"])
def prompt_for_code(message):
    if language == "RU":
        msg = bot.send_message(message.chat.id, "Введите промокод:")
    else:
        msg = bot.send_message(message.chat.id, "Enter promo code:")
    bot.register_next_step_handler(msg, validate_promocode)

# Функция для проверки валидности промокода
def validate_promocode(message):
    promo_code = message.text.strip()
    connection = create_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT points FROM promo_codes WHERE code = %s", (promo_code,))
        result = cursor.fetchone()
        
        if result:
            points = result[0]
            update_user_points(message.from_user.username, points)
            if language == "RU":
                bot.send_message(message.chat.id, f"Промокод успешно применен! Вам начислено {points} баллов.")
            else:
                bot.send_message(message.chat.id, f"The promo code has been successfully applied! You have been credited with {points} points.")
        else:
            if language == "RU":
                bot.send_message(message.chat.id, "Неверный промокод. Попробуйте еще раз.")
            else:
                bot.send_message(message.chat.id, "Invalid promo code. Please try again.")
    except Error as e:
        print(f"Ошибка при проверке промокода: {e}")
    finally:
        cursor.close()
        connection.close()

def get_user_balance(username):
    connection = create_db_connection()
    cursor = None
    balance = 0  # Инициализация баланса

    try:
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute("SELECT points FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()  # Получаем результат запроса
            
            if result is not None:  # Проверяем, есть ли результат
                balance = result[0]  # Получаем баланс
    except Error as e:
        print(f"Ошибка работы с базой данных: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

    return balance


def generate_referral_link(user_name):
    return f"https://t.me/ThisDarkBot?start=ref?user={user_name}"

def get_user_referrals_count(username):
    connection = create_db_connection()
    cursor = None
    count = 0  # Инициализация счетчика рефералов

    try:
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute("SELECT referrals FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()  # Получаем результат запроса
            
            if result is not None:  # Проверяем, есть ли результат
                count = result[0]  # Получаем количество рефералов
    except Error as e:
        print(f"Ошибка работы с базой данных: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

    return count
def enter_refferal(message):
    if message.text == "Реф." or message.text == "REF":
        user_id = message.from_user.id
        username = message.from_user.username  # Получаем имя пользователя
        balance = get_user_balance(username)  # Получаем баланс пользователя
        refferals_count = get_user_referrals_count(username)  # Получаем количество рефералов

        # Генерируем реферальную ссылку
        referral_link = generate_referral_link(username)

        # Увеличиваем количество рефералов на 1 для реферера
        # update_user_points(username, 0, referral=True)

        if language == "RU":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Назад")
    
            markup.add(back)
            bot.send_photo(message.chat.id, open('images/dark_wallet.jpg', 'rb'), caption=f"Ваш баланс: DARK {balance}\n\n1 реф. = 20 $DARK\n\nПригласить больше друзей 👇🏼\n\n🎖 У вас рефералов: {refferals_count} чел.\n\n🛎 Ваша ссылка: {referral_link}", parse_mode="html", reply_markup=markup)
        elif language == "EN":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Back")
    
            markup.add(back)
            bot.send_photo(message.chat.id, open('images/dark_wallet.jpg', 'rb'), caption=f"Your balance: DARK {balance}\n\n1 ref. = 20 $DARK\n\nInvite more friends 👇🏼\n\n🎖 Your referrals: {refferals_count} people.\n\n🛎 Your referrer: {referral_link}", parse_mode="html", reply_markup=markup)

def add_points_to_referrer(referrer_id, points):
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE users SET points = points + %s WHERE id = %s", (points, referrer_id))
        connection.commit()
    except Error as e:
        print(f"Ошибка при добавлении баллов рефереру: {e}")
    finally:
        cursor.close()
        connection.close()

def update_referral_count(referrer_id):
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE users SET referrals = referrals + 1 WHERE id = %s", (referrer_id,))
        connection.commit()
    except Error as e:
        print(f"Ошибка при обновлении количества рефералов: {e}")
    finally:
        cursor.close()
        connection.close()


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username  # Получаем имя пользователя
    if not approved:
        if message.text.startswith('/start ref_'):
            referrer_username = message.text.split('_')[1]  # Получаем имя реферала
            
            # Подключаемся к базе данных и получаем ID реферала
            connection = create_db_connection()
            if connection is None:
                bot.send_message(message.chat.id, "Ошибка подключения к базе данных.")
                return
            
            cursor = connection.cursor()
            cursor.execute("SELECT id, has_referral FROM users WHERE username = %s", (referrer_username,))
            result = cursor.fetchone()  # Получаем результат запроса
            
            if result:
                referrer_id, has_referral = result  # Получаем ID и статус реферала
                
                # Проверка, использовал ли пользователь реферальную ссылку ранее
                if not has_referral:
                    # Добавление баллов за приглашенного реферала
                    if referrer_id != user_id:  # Проверка, что реферал не сам пользователь
                        add_points_to_referrer(referrer_id, 20)  # Функция добавления 20 баллов рефереру

                        # Обновление данных о рефералах
                        update_referral_count(referrer_id)  # Увеличение счётчика рефералов для реферера
                        # update_user_points(username, 0, referral=True)

                        # Уведомление реферера о новом приглашенном
                        bot.send_message(referrer_id, "Ваш реферал успешно зарегистрировался! Вам начислено 20 баллов.")
                        
                        # Обновление статуса реферала
                        cursor.execute("UPDATE users SET has_referral = 1 WHERE username = %s", (username,))
                        connection.commit()
                    else:
                        bot.send_message(message.chat.id, "Вы не можете использовать свою собственную реферальную ссылку.")
                else:
                    bot.send_message(message.chat.id, "Вы уже использовали реферальную ссылку.")
            else:
                bot.send_message(message.chat.id, "Реферальный пользователь не найден.")
            
            cursor.close()
            connection.close()
        choose_lang(message)
    else:
        is_approved(message)

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.chat.type == 'private':
        subscriptions(message)
        wallet(message)
        enter_refferal(message)

        if message.text == "Язык" or message.text == "LANG":
            choose_lang(message)

        if message.text == "Назад" or message.text == "Back":
            is_approved(message)



# Обработчик событий добавления реакции
# @client.on(events.ChatAction)
# async def handle_reaction(event):
#     if event.chat.username == channel_name:
#         if event.user_added or event.user_joined:
#             user = await event.get_user()
#             username = user.username or f"{user.id}"  # Используем ID, если username отсутствует

#             # Если пользователь поставил реакцию, начисляем 4 балла
#             if event.action_message.reactions:
#                 update_user_points(username, 4)
#                 print(f"{username} получил {4} баллов за реакцию.")

def start_telethon_client():
    client.start()
    client.run_until_disconnected()

# Запуск TeleBot клиента
def start_telebot_client():
    bot.polling(none_stop=True)

# Создаем потоки для обоих клиентов
telethon_thread = threading.Thread(target=start_telethon_client)
telebot_thread = threading.Thread(target=start_telebot_client)

# Запускаем оба потока
telethon_thread.start()
telebot_thread.start()

# Ждем завершения обоих потоков
telethon_thread.join()
telebot_thread.join()
