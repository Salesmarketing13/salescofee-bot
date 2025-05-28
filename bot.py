import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

user_data = {}

# Стан користувача
user_state = {}

# Запитання по черзі
questions = [
    "1. Як я можу до вас звертатися? (Ім'я та прізвище)",
    "2. Скільки вам років?",
    "3. Яка ваша освіта або професія?",
    "4. Ким ви працюєте чи навчаєтесь?",
    "5. Чи маєте ви хобі? Якщо так — які? (Можна пропустити)",
    "6. Чи хочете ви отримувати пропозиції по роботі, освіті чи стажуванням? (Так/Ні)"
]

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = []
    user_state[chat_id] = 0

    bot.send_message(chat_id, "👋Привіт! Ми дуже раді що ви завітали! Щоб отримати безкоштовну каву, дайте будь-ласка коротку відповідь на кілька запитань щоб краще прзнайомитися 😊")
    bot.send_message(chat_id, questions[0])

@bot.message_handler(func=lambda message: True, content_types=['text', 'contact'])
def handle_message(message):
    chat_id = message.chat.id

    # Перевірка на наявність стану
    if chat_id not in user_state:
        bot.send_message(chat_id, "Натисніть /start щоб почати")
        return

    # Якщо останнє питання (контакт)
    if user_state[chat_id] == len(questions):
        if message.contact and message.contact.phone_number:
            user_data[chat_id].append(f"Телефон: {message.contact.phone_number}")
            bot.send_message(chat_id, "☕️ Дякуємо за ваші відповіді! Щоб отримати свою каву, зверніться до барісти і покажіть це повідомлення. Гарного дня! 😺")
            del user_state[chat_id]
        else:
            bot.send_message(chat_id, "‼️ Будь ласка, натисніть кнопку нижче, щоб поділитися контактом.")
            request_contact_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            contact_button = KeyboardButton(text="Поділитися номером", request_contact=True)
            request_contact_keyboard.add(contact_button)
            bot.send_message(chat_id, "Для підтвердження анкети і отримання безкоштовної кави поділіться своїм контактом. Обіцяємо, що не будемо набридати 😊", reply_markup=request_contact_keyboard)
        return

    # Зберігаємо відповідь
    user_data[chat_id].append(message.text)
    user_state[chat_id] += 1

    # Наступне питання або запит контакту
    if user_state[chat_id] < len(questions):
        bot.send_message(chat_id, questions[user_state[chat_id]])
    else:
        # Переходимо до запиту контакту
        request_contact_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        contact_button = KeyboardButton(text="Поділитися номером", request_contact=True)
        request_contact_keyboard.add(contact_button)
        bot.send_message(chat_id, "Для підтвердження анкети і отримання безкоштовної кави поділіться своїм контактом. Обіцяємо, що не будемо набридати 😊", reply_markup=request_contact_keyboard)

bot.polling()