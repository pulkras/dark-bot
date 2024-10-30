import telebot
from telebot import types


# Получение всех пользователей
def get_all_users():
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, username, points FROM users")
        users = cursor.fetchall()
        return users
    except Error as e:
        print(f"Ошибка при получении пользователей: {e}")
    finally:
        cursor.close()
        connection.close()

        
def admin_panel(message):
if message.from_user.username == 'pulkrasowner':
        markup = types.InlineKeyboardMarkup()
        btn_show = types.InlineKeyboardButton("Показать пользователей", callback_data="show_users")
        btn_promo = types.InlineKeyboardButton("Управление промокодами", callback_data="manage_promo")
        markup.add(btn_show, btn_promo)
        bot.send_message(message.chat.id, "Панель администратора", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")

def callback_handler(call):
    if call.data == "show_users":
        users = get_all_users()
        if users:
            for user in users:
                user_id, username, points = user
                markup = types.InlineKeyboardMarkup()
                btn_edit = types.InlineKeyboardButton(f"Изменить баллы ({points})", callback_data=f"edit_points_{user_id}")
                markup.add(btn_edit)
                bot.send_message(call.message.chat.id, f"ID: {user_id}, Username: {username}, Points: {points}", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "Нет пользователей в базе данных.")
    
    elif call.data.startswith("edit_points_"):
        user_id = int(call.data.split("_")[2])
        msg = bot.send_message(call.message.chat.id, "Введите новое количество баллов:")
        bot.register_next_step_handler(msg, process_points_change, user_id)

    elif call.data == "manage_promo":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_add = types.KeyboardButton("Добавить промокод")
        btn_delete = types.KeyboardButton("Удалить промокод")
        markup.add(btn_add, btn_delete)
        bot.send_message(call.message.chat.id, "Выберите действие с промокодами:", reply_markup=markup)
        
# Изменение баллов
def process_points_change(message, user_id):
    try:
        points = int(message.text)
        change_user_points(user_id, points)
        bot.send_message(message.chat.id, "Баллы успешно обновлены.")
    except ValueError:
        bot.send_message(message.chat.id, "Введите корректное число.")

# Функция для изменения количества баллов пользователя
def change_user_points(user_id, points):
    connection = create_db_connection()
    if connection is None:
        print("Не удалось подключиться к базе данных")
        return
    
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE users SET points = %s WHERE id = %s", (points, user_id))
        connection.commit()
        print(f"Баллы пользователя с ID {user_id} успешно обновлены до {points}")
    except Error as e:
        print(f"Ошибка при изменении баллов пользователя: {e}")
    finally:
        cursor.close()
        connection.close()



# Добавление промокода
def add_promo_code(message):
    msg = bot.send_message(message.chat.id, "Введите промокод и количество баллов через пробел (например, PROMO123 50):")
    bot.register_next_step_handler(msg, process_add_promo)

def process_add_promo(message):
    try:
        promo_code, points = message.text.split()
        points = int(points)
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO promo_codes (code, points) VALUES (%s, %s)", (promo_code, points))
        connection.commit()
        bot.send_message(message.chat.id, f"Промокод '{promo_code}' на {points} баллов добавлен.")
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка при добавлении промокода. Проверьте формат.")
        print(f"Ошибка: {e}")
    finally:
        cursor.close()
        connection.close()

# Удаление промокода
def delete_promo_code(message):
    msg = bot.send_message(message.chat.id, "Введите промокод для удаления:")
    bot.register_next_step_handler(msg, process_delete_promo)

def process_delete_promo(message):
    promo_code = message.text.strip()
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM promo_codes WHERE code = %s", (promo_code,))
        connection.commit()
        bot.send_message(message.chat.id, f"Промокод '{promo_code}' удален.")
    except Error as e:
        print(f"Ошибка при удалении промокода: {e}")
        bot.send_message(message.chat.id, "Ошибка при удалении промокода.")
    finally:
        cursor.close()
        connection.close()