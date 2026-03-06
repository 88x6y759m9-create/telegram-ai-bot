import telebot
import openai
import os
from telebot.types import ReplyKeyboardMarkup

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_KEY

users_context = {}
image_mode = {}


def menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("🤖 Задать вопрос")
    markup.row("🖼 Создать изображение")
    markup.row("👤 Мой профиль", "💬 Очистить чат")

    return markup


@bot.message_handler(commands=["start"])
def start(message):

    users_context[message.chat.id] = []

    bot.send_message(
        message.chat.id,
        "Привет 👋\n\nНапиши вопрос или выбери функцию.",
        reply_markup=menu()
    )


@bot.message_handler(func=lambda m: True)
def handler(message):

    chat_id = message.chat.id
    text = message.text


    if text == "👤 Мой профиль":

        bot.send_message(
            chat_id,
            f"ID: {message.from_user.id}\n"
            f"Username: @{message.from_user.username}"
        )
        return


    if text == "💬 Очистить чат":

        users_context[chat_id] = []
        bot.send_message(chat_id,"Контекст очищен")
        return


    if text == "🖼 Создать изображение":

        image_mode[chat_id] = True
        bot.send_message(chat_id,"Напишите описание картинки")
        return


    if image_mode.get(chat_id):

        image_mode[chat_id] = False

        response = openai.images.generate(
            model="gpt-image-1",
            prompt=text
        )

        image_url = response.data[0].url

        bot.send_photo(chat_id,image_url)

        return


    if chat_id not in users_context:
        users_context[chat_id] = []


    users_context[chat_id].append({
        "role":"user",
        "content":text
    })


    response = openai.chat.completions.create(

        model="gpt-4o-mini",

        messages=users_context[chat_id]

    )


    answer = response.choices[0].message.content


    users_context[chat_id].append({
        "role":"assistant",
        "content":answer
    })


    bot.send_message(chat_id,answer)


bot.infinity_polling()
