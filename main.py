import telebot
import config 
from telebot import types
import time

bot = telebot.TeleBot(config.TOKEN)

CHAT_ID = "@IhtDEuLaKpZlZDky"  # ID вашего чата
CHANNEL_ID = "@darkmemtoken"  # ID вашего канала
balance = None
approved = False
global language
language = "RU"


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

        second_markup.add(wallet, referal, lang, promo)
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

        second_markup.add(wallet, referal, lang, promo)
        bot.send_message(message.chat.id, "...", reply_markup=second_markup)
        bot.send_photo(message.chat.id, open('images/dark_welcome.jpg', 'rb'), caption="Hi!\n\nWelcome to the official $DARK bot! 🎉Here you can get $DARK coins for your activity. It's simple: react to posts and subscribe to our Dark channel to get rewards. The more activity - the more $DARK coins you have in your account. 🚀 \n\nShall we get started?", parse_mode="html", reply_markup=first_markup)

def choose_lang(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        russian = types.KeyboardButton("RU")
        english = types.KeyboardButton("EN")

        markup.add(russian, english)

        bot.send_message(message.chat.id, "Please specify language:", parse_mode="html", reply_markup=markup)

def subscriptions(message):
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

def enter_promocode(message):
    if message.text == "Промокод" or message.text == "PromoCode":
        if language == "RU":
            bot.send_photo(message.chat.id, open('images/dark_special_offer.jpg', 'rb'), caption="Введите промокод:")
        elif language == "EN":
            bot.send_photo(message.chat.id, open('images/dark_special_offer.jpg', 'rb'), caption="Enter promo code:")

def enter_refferal(message):
    if message.text == "Реф." or message.text == "REF":
        refferals = 0
        if language == "RU":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Назад")
    
            markup.add(back)
            bot.send_photo(message.chat.id, open('images/dark_wallet.jpg', 'rb'), caption="Ваш баланс:  DARK " + str(balance) + "\n\n1 реф. = 20 $DARK\n\nПригласить больше друзей 👇🏼\n\n🎖 У вас рефералов: " + str(refferals) + " чел.\n\n🛎 Ваша ссылка: https://", parse_mode="html", reply_markup=markup)
        elif language == "EN":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("Back")
    
            markup.add(back)
            bot.send_photo(message.chat.id, open('images/dark_wallet.jpg', 'rb'), caption="Your balance: DARK " + str(balance) + "\n\n1ref. = 20 $DARK\n\nInvite more friends \n\n🎖 Your referrals: " + str(refferals) + " people.\n\n🛎 Your referrer: https://", parse_mode="html", reply_markup=markup)

@bot.message_handler(commands=['start'])
def welcome(message):
    # if not approved:
    #     choose_lang(message)
    # else:
        is_approved(message)

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.chat.type == 'private':
        subscriptions(message)
        wallet(message)
        enter_promocode(message)
        enter_refferal(message)

        if message.text == "Язык" or message.text == "LANG":
            choose_lang(message)

        if message.text == "Назад" or message.text == "Back":
            is_approved(message)

@bot.callback_query_handler(func=lambda call: call.data == "approval")
def check_subscription(call):
    # user_id = call.from_user.id

    # # Проверка подписки на чат
    # chat_member = bot.get_chat_member(CHAT_ID, user_id)
    # channel_member = bot.get_chat_member(CHANNEL_ID, user_id)

    # if chat_member.status in ['member', 'administrator', 'creator'] and channel_member.status in ['member', 'administrator', 'creator']:
    #     global approved
    #     approved = True
    #     if language == "RU":
    #     # Пользователь подписан и на чат, и на канал
    #         bot.answer_callback_query(call.id, "Проверка пройдена!")
    #         bot.send_message(call.message.chat.id, "Вы подписаны на оба ресурса. Проверка пройдена.")
    #     elif language == "EN":
    #         bot.answer_callback_query(call.id, "Approved!")
    #         bot.send_message(call.message.chat.id, "Checking is approved")
    # else:
    #     if language == "RU":
    #     # Пользователь не подписан на один или оба ресурса
    #         bot.answer_callback_query(call.id, "Вы не подписаны!")
    #         bot.send_message(call.message.chat.id, "Вы не подписаны на чат или канал.")
    #     elif language == "EN":
    #         bot.answer_callback_query(call.id, "Didn't subscribe!")
    #         bot.send_message(call.message.chat.id, "You didn't subscribe chat or channel")
    is_approved(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "nft")
def check_nft_ref(call):
    if language == "RU":
       bot.send_message(call.message.chat.id, "🙁На данный момент вам не хватает рефералов для получения уникальной NFT.\n\nДля получения персональной NFT вы должны пригласить 5+ рефералов через свою пригласительную ссылку.")
    elif language == "EN":
        bot.send_message(call.message.chat.id, "🙁At the moment you don’t have enough referrals to receive a unique NFT.\n\nTo receive a personalized NFT, you must invite 5+ referrals through your invite link.")

bot.polling(none_stop=True)