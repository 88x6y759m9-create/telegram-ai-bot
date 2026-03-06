import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)


def menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(
        KeyboardButton("👋 Что умеет бот"),
        KeyboardButton("👤 Мой профиль")
    )

    markup.add(
        KeyboardButton("🚀 Премиум"),
        KeyboardButton("💬 Удалить контекст")
    )

    markup.add(
        KeyboardButton("🖼 Создать изображение"),
        KeyboardButton("🎬 Создать видео")
    )

    markup.add(
        KeyboardButton("🎸 Создать песню"),
        KeyboardButton("🔎 Интернет-поиск")
    )

    markup.add(
        KeyboardButton("📝 Выбрать модель"),
        KeyboardButton("⚙️ Настройки бота")
    )

    markup.add(
        KeyboardButton("🎱 Основные команды"),
        KeyboardButton("📄 Соглашение")
    )

    return markup


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать!\n\nВыберите действие:",
        reply_markup=menu()
    )


@bot.message_handler(func=lambda m: True)
def handler(message):

    text = message.text

    if text == "👋 Что умеет бот":
        bot.send_message(message.chat.id,"Я умею отвечать на вопросы и генерировать контент.")

    elif text == "👤 Мой профиль":
        bot.send_message(message.chat.id,f"Ваш ID: {message.from_user.id}")

    elif text == "🚀 Премиум":
        bot.send_message(message.chat.id,"⭐ Премиум скоро будет доступен.")

    elif text == "💬 Удалить контекст":
        bot.send_message(message.chat.id,"Контекст очищен.")

    elif text == "🖼 Создать изображение":
        bot.send_message(message.chat.id,"Напишите описание картинки.")

    elif text == "🎬 Создать видео":
        bot.send_message(message.chat.id,"Функция видео скоро появится.")

    elif text == "🎸 Создать песню":
        bot.send_message(message.chat.id,"Напишите текст песни.")

    elif text == "🔎 Интернет-поиск":
        bot.send_message(message.chat.id,"Напишите что нужно найти.")

    elif text == "📝 Выбрать модель":
        bot.send_message(message.chat.id,"Выберите модель AI.")

    elif text == "⚙️ Настройки бота":
        bot.send_message(message.chat.id,"Настройки пока пустые.")

    elif text == "🎱 Основные команды":
        bot.send_message(message.chat.id,"/start /help /premium")

    elif text == "📄 Соглашение":
        bot.send_message(message.chat.id,"Пользовательское соглашение.")

    else:
        bot.send_message(message.chat.id,"Напишите вопрос.")


bot.infinity_polling()
