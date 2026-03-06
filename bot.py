import telebot
import openai
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_KEY

users_context = {}


def menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("👋 Что умеет бот","👤 Мой профиль")
    markup.add("🚀 Премиум","💬 Удалить контекст")
    markup.add("🖼 Создать изображение","🎬 Создать видео")
    markup.add("🎸 Создать песню","🔎 Интернет-поиск")
    markup.add("📝 Выбрать модель","⚙️ Настройки бота")
    markup.add("🎱 Основные команды","📄 Соглашение")

    return markup


@bot.message_handler(commands=['start'])
def start(message):

    users_context[message.chat.id] = []

    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать в AI бот\n\nЗадайте любой вопрос",
        reply_markup=menu()
    )


@bot.message_handler(func=lambda m: True)
def chat(message):

    chat_id = message.chat.id
    text = message.text


    if text == "👤 Мой профиль":

        bot.send_message(
            chat_id,
            f"ID: {message.from_user.id}\nUsername: @{message.from_user.username}"
        )
        return


    if text == "💬 Удалить контекст":

        users_context[chat_id] = []
        bot.send_message(chat_id,"Контекст очищен")
        return


    if text == "🚀 Премиум":

        bot.send_message(chat_id,"⭐ Премиум скоро будет доступен")
        return


    if text == "🖼 Создать изображение":

        bot.send_message(chat_id,"Напишите описание картинки")
        return


    if text.startswith("/img"):

        prompt = text.replace("/img","")

        response = openai.images.generate(
            model="gpt-image-1",
            prompt=prompt
        )

        image_url = response.data[0].url

        bot.send_photo(chat_id,image_url)

        return


    if chat_id not in users_context:
        users_context[chat_id] = []

    users_context[chat_id].append(
        {"role":"user","content":text}
    )


    response = openai.chat.completions.create(

        model="gpt-4o-mini",

        messages=users_context[chat_id]

    )


    answer = response.choices[0].message.content

    users_context[chat_id].append(
        {"role":"assistant","content":answer}
    )


    bot.send_message(chat_id,answer)


bot.infinity_polling()
