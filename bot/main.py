import telebot
from mongoengine import connect
from models.cat_and_products import Text, Category
from models.user_model import User
from bot.config import *
from telebot.types import (InlineKeyboardButton,
                           InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)

connect('bot_shop', host='192.168.0.9', port=27017)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def keyboard(message):
    key_bord = ReplyKeyboardMarkup(resize_keyboard=True)
    key_bord.add(*START_KEYBOARD.values())
    User.get_or_create_user(message)
    markup = Text.get_text("Greeting")
    bot.send_message(chat_id=message.chat.id,
                     text='Hello! ' + markup, reply_markup=key_bord)

@bot.message_handler(func=lambda message: message.text == START_KEYBOARD['categories'])
def show_cats(message):
    cats_kb = InlineKeyboardMarkup()
    cats_buttons = []
    all_cats = Category.objects.all()

    for i in all_cats:
        callback_date = 'category_' + str(i.id)
        if i.is_parent:
            callback_date = 'subcategory_' + str(i.id)
        cats_buttons.append(InlineKeyboardButton(text=i.title,
                                                 callback_data=callback_date))

    cats_kb.add(*cats_buttons)
    bot.send_message(message.chat.id, text='Выберите необходимую категорию',
                     reply_markup=cats_kb)

@bot.message_handler(func=lambda call: call.data.split('_')[0] == 'subcategory')
def sub_cat(call):
    subcats_kb = InlineKeyboardMarkup()
    subcats_buttons = []
    category = Category.objects.get(id=call.data.split('_')[1])
    for c in category.sub_categories:
        callback_data = 'category_' + str(c.id)
        if c.is_parent:
            callback_data = 'subcategory_' + str(c.id)
        subcats_buttons.append(InlineKeyboardButton(text=c.title,
                                                    callback_data=callback_data))
    subcats_kb.add(*subcats_buttons)
    bot.send_message(call.message.chat.id, text='subcat example',
                     reply_markup=subcats_kb)

if __name__ == '__main__':
    print('Bot started')
    bot.polling()