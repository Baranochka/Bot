import telebot
import sqlite3
import hashlib
import schedule
import threading

from telebot import types

print('Bot started')
TOKEN = ''
bot = telebot.TeleBot(TOKEN)
condition_users = {}


markup = types.InlineKeyboardMarkup()
btn1 = types.InlineKeyboardButton("Начать", callback_data="btn_click")
markup.add(btn1)
@bot.callback_query_handler(func=lambda call: call.data == "btn_click")
def button_click(call):
    bot.send_message(call.message.chat.id, "Введите значение для показателя отчёта Исходные звонки:")
    condition_users[call.message.chat.id] = 'value_original_calls'

@bot.message_handler(regexp="^[0-9]+$")
def input_value(message):
    print(1)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    if condition_users.get(message.chat.id) == 'value_original_calls':
        print(2)
        print(message.text)
        print(type(message.text))
        cursor.execute('SELECT val_orig_calls FROM users WHERE chat_id = ?', (message.chat.id,))
        result = cursor.fetchone()[0]
        print(result)
        print(type(result))
        cursor.execute('UPDATE users SET val_orig_calls = val_orig_calls + ? WHERE chat_id = ?', (result, message.chat.id))
        conn.commit()
    conn.close()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Welcome to malahit_bot by Maksim!')
    bot.send_message(message.chat.id, 'Введите Фамилию Имя')
    
# @bot.message_handler(commands=['registr'])
# def registration(message):
#     if condition_users.get(message.chat.id) == 'login_success':
#         bot.reply_to(message, 'Вы в системе!')
#     else:
#         conn = sqlite3.connect('users.db')
#         cursor = conn.cursor()
#         # Поиск пользователя в базе данных по имени пользователя
#         result = 0
#         cursor.execute('SELECT chat_id FROM users WHERE chat_id = ?', (message.chat.id,))
#         result = cursor.fetchone()
#         conn.close()
#         if result == None:
#             bot.send_message(message.chat.id, 'Введите пароль\n\nПароль должен содержать не менее 5 символов, цифры, '
#                                               'заглавные и строчные буквы')
#             condition_users[message.chat.id] = 'registration'
#         else:
#             bot.send_message(message.chat.id, 'Вы уже зарегистрированы!')

@bot.message_handler(regexp="^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$")
def input_password(message):
    bot.send_message(message.chat.id, message.text)

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (chat_id, user_name, val_orig_calls) VALUES (?, ?, ?)', (message.chat.id, message.text, 0))
    # Сохранение изменений и закрытие соединения с базой данных
    conn.commit()
    conn.close()
    send_daily_message()
    
    

# === Функция для рассылки ===
def send_daily_message():
    bot.send_message(chat_id, "Добрый вечер! Время добавить отчёт ☺", reply_markup=markup)

# === Планировщик в отдельном потоке ===
def schedule_checker():
    schedule.every().monday.at("18:00","Asia/Yekaterinburg").do(send_daily_message)
    schedule.every().tuesday.at("18:00","Asia/Yekaterinburg").do(send_daily_message)
    schedule.every().wednesday.at("18:00","Asia/Yekaterinburg").do(send_daily_message)
    schedule.every().thursday.at("18:00","Asia/Yekaterinburg").do(send_daily_message)
    schedule.every().friday.at("18:00","Asia/Yekaterinburg").do(send_daily_message)
    while True:
        schedule.run_pending()


# === Запуск планировщика в отдельном потоке ===
threading.Thread(target=schedule_checker, daemon=True).start()

    #         bot.send_message(password.chat.id, 'Вы успешно зарегистрированы!')
#         bot.send_message(password.chat.id, 'Войдите в систему!')
#         condition_users[password.chat.id] = 0
#     else:
#         bot.send_message(password.chat.id, 'Неправильный ввод пароля!')
#         condition_users[password.chat.id] = 0

# def validate_password(new_password):
#     # Проверка длины пароля
#     if len(new_password) < 5:
#         print(1)
#         return False

#     # Проверка наличия цифр в пароле
#     if not any(char.isdigit() for char in new_password):
#         print(2)
#         return False


#     # Проверка наличия символов верхнего регистра в пароле
#     if not any(char.isupper() for char in new_password):
#         print(3)
#         return False


#     # Проверка наличия символов нижнего регистра в пароле
#     if not any(char.islower() for char in new_password):
#         print(4)
#         return False

#     # Если пароль прошел все проверки, возвращаем True
#     return True

# @bot.message_handler(commands=['login'])
# def login(message):
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()
#     # Поиск пользователя в базе данных по имени пользователя
#     result = 0
#     cursor.execute('SELECT chat_id FROM users WHERE chat_id = ?', (message.chat.id,))
#     result = cursor.fetchone()
#     conn.close()
#     if result != None:
#         bot.send_message(message.chat.id, 'Введите пароль')
#         condition_users[message.chat.id] = 'login'
#     else:
#         bot.send_message(message.chat.id, 'Вы не зарегистрированы!')


# @bot.message_handler(func=lambda message: condition_users.get(message.chat.id) == 'login')
# def autentification(password):
#     hashed_password = hash_password(password.text)
#     # Создание подключения к базе данных
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()
#     # Поиск пользователя в базе данных по имени пользователя
#     cursor.execute('SELECT password FROM users WHERE chat_id = ?', (password.chat.id,))
#     result = cursor.fetchone()
#     # Проверка соответствия хешей паролей
#     if result and hashed_password == result[0]:
#         bot.send_message(password.chat.id, 'Аутентификация успешна!')
#         condition_users[password.chat.id] = 'login_success'
#     else:
#         bot.send_message(password.chat.id, 'Неверный пароль!')
#         condition_users[password.chat.id] = 0
#     # Закрытие соединения с базой данных
#     conn.close()




# bot.polling()
bot.infinity_polling()
