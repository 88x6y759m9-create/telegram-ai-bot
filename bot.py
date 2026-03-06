import telebot
import requests
import os
from telebot.types import ReplyKeyboardMarkup

TOKEN = os.getenv("BOT_TOKEN")
AI_KEY = os.getenv("AI_KEY")

bot = telebot.TeleBot(TOKEN)


def ask_ai(prompt):

    url = "https://api.together.xyz/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {AI_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(url, headers=headers, json=data)

    return r.json()["choices"][0]["message"]["content"]


def menu():

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("🤖 Задать вопрос")
    markup.row("👤 Мой профиль")

    return markup


@bot.message_handler(commands=["start"])
def start(msg):

    bot.send_message(
        msg.chat.id,
        "Привет 👋\n\nНапиши вопрос.",
        reply_markup=menu()
    )


@bot.message_handler(func=lambda m: True)
def chat(msg):

    answer = ask_ai(msg.text)

    bot.send_message(msg.chat.id,answer)


bot.infinity_polling()
