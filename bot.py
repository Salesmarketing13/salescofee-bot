from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

NAME, AGE, EDUCATION, JOB, HOBBY, OFFER, PHONE = range(7)
user_data = {}

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "👋Привіт! Ми дуже раді, що ви завітали!
"
        "Щоб отримати безкоштовну каву, дайте будь ласка коротку відповідь на кілька запитань, щоб краще познайомитися 😊"
    )
    update.message.reply_text("1️⃣ Як я можу до вас звертатися?")
    return NAME

def name(update: Update, context: CallbackContext) -> int:
    user_data["name"] = update.message.text
    update.message.reply_text("2️⃣ Скільки вам років?")
    return AGE

def age(update: Update, context: CallbackContext) -> int:
    user_data["age"] = update.message.text
    update.message.reply_text("3️⃣ Яка ваша освіта/професія?")
    return EDUCATION

def education(update: Update, context: CallbackContext) -> int:
    user_data["education"] = update.message.text
    update.message.reply_text("4️⃣ Ким ви працюєте чи навчаєтесь?")
    return JOB

def job(update: Update, context: CallbackContext) -> int:
    user_data["job"] = update.message.text
    keyboard = [['Пропустити']]
    update.message.reply_text("5️⃣ Чи маєте ви хобі? Якщо так, то які?", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
    return HOBBY

def hobby(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    if text.lower() == "пропустити":
        user_data["hobby"] = "Не вказано"
    else:
        user_data["hobby"] = text
    keyboard = [["Так", "Ні"]]
    update.message.reply_text("6️⃣ Чи хочете ви отримувати пропозиції по роботі, освіті чи стажуванням?",
                              reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True))
    return OFFER

def offer(update: Update, context: CallbackContext) -> int:
    user_data["offer"] = update.message.text
    contact_btn = KeyboardButton("Поділитися контактом", request_contact=True)
    keyboard = [[contact_btn]]
    update.message.reply_text(
        "7️⃣ Для підтвердження анкети і отримання безкоштовної кави поділіться своїм контактом.
"
        "Обіцяємо, що не будемо набридати 😊",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return PHONE

def phone(update: Update, context: CallbackContext) -> int:
    if not update.message.contact:
        update.message.reply_text("⚠️ Будь ласка, скористайтеся кнопкою для відправки контакту.")
        return PHONE
    user_data["phone"] = update.message.contact.phone_number
    update.message.reply_text(
        "✅ Дякуємо за ваші відповіді!
"
        "Щоб отримати свою каву, зверніться до барісти і покажіть це повідомлення.
"
        "Гарного дня! 😺"
    )
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Дякуємо! Якщо захочете продовжити — просто напишіть /start 😊")
    return ConversationHandler.END

def main():
    import os
    TOKEN = os.environ.get("BOT_TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            AGE: [MessageHandler(Filters.text & ~Filters.command, age)],
            EDUCATION: [MessageHandler(Filters.text & ~Filters.command, education)],
            JOB: [MessageHandler(Filters.text & ~Filters.command, job)],
            HOBBY: [MessageHandler(Filters.text & ~Filters.command, hobby)],
            OFFER: [MessageHandler(Filters.text & ~Filters.command, offer)],
            PHONE: [MessageHandler(Filters.contact, phone),
                    MessageHandler(Filters.text & ~Filters.command, phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
