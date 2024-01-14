import telebot
import sqlite3
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from time import sleep
import datetime

import config
import inline_markup
import reply_markup


#  LIBRARY VARIABLS  #

bot = telebot.TeleBot(config.TOKEN)

db = sqlite3.connect("pillow_ai_bot_database.db", check_same_thread=False)
sql = db.cursor()

DateTime = datetime.datetime.now()



#  CREATE TABLE  #

sql.execute('''CREATE TABLE IF NOT EXISTS user_data (ID INTEGER, USERNAME TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, DATE_TIME TIMESTAMP)''')
db.commit()





#  START  #

@bot.message_handler(commands=['start'])
def start (message):

    sql.execute(f'''SELECT ID FROM user_data WHERE ID = {message.chat.id}''')
    user_id = sql.fetchone()

    if user_id == None:

        sql.execute('''INSERT INTO user_data (ID, USERNAME, FIRST_NAME, LAST_NAME, DATE_TIME) VALUES (?, ?, ?, ?, ?)''',
        (str(message.chat.id), str(message.from_user.username), str(message.from_user.first_name), str(message.from_user.last_name), DateTime))
        db.commit()

        bot.send_message(message.chat.id, f'<b> {message.from_user.full_name}'
                                          f'\n\nДобро пожаловать  👋 </b>', parse_mode='html')
        bot.send_message(message.chat.id, "<b> Отправьте мне любое фото после чего я вам предоставлю разные эффекты  ✨</b>", parse_mode="html")

    else:

        bot.send_message(message.chat.id, "<b> Отправьте мне любое фото после чего я вам предоставлю разные эффекты  ✨ </b>", parse_mode="html")





#  PHOTO  #

@bot.message_handler(content_types=['photo'])
def select_effect(message):


    file_info = bot.get_file(message.photo[-1].file_id)
    file = bot.download_file(file_info.file_path)

    with open(f"photo/Original/{message.chat.id}.jpg", "wb") as new_file:
        new_file.write(file)
        with open(f"photo/Original/{message.chat.id}.jpg", "rb") as photo:
            bot.send_message(message.chat.id, "<b> Выберите эффект: </b>", parse_mode="html",)
            bot.send_photo(message.chat.id, photo,  reply_markup=inline_markup.effects_inline)












#  IMAGE SIZE  #

def image(message):

    bot.send_chat_action(message.chat.id, 'upload_photo')


    file_info = bot.get_file(message.photo[-1].file_id)
    file = bot.download_file(file_info.file_path)
    
    with open(f"photo/Original/{message.chat.id}.jpg", "wb") as new_file:
        new_file.write(file)
        
        img = Image.open(f"photo/Original/{message.chat.id}.jpg")
        
        #  РАЗМЕР ФОТО  #

        # img.thumbnail((1000, 1000))
        # img.save(f"photo/Original/{message.chat.id}.jpg")
        

        #  ОБРЕЗКА ФОТО  #

        # crop_img = img.crop((100, 200, 300, 400))
        # crop_img.save(f"photo/Original/{message.chat.id}.jpg")


        #  ИНФО ФОТО  #

        # size = img.size
        # format = img.format
        # mode = img.mode


        #  ПОВАРАЧИВАТЬ ФОТО  #

        # rotated_image = img.rotate(180)
        # rotated_image.save(f"photo/Original/{message.chat.id}.jpg")

        

        #  FILTER  #

        # BLUR                  # БЛЮР
        # CONTOUR               # БЕЛЫЙ КОНТУР
        # DETAIL                # Минус четкость (мало)
        # EDGE_ENHANCE          # Минус четкость (средне)
        # EDGE_ENHANCE_MORE     # Минус четкость (средне)
        # EMBOSS                # БЕТОН
        # FIND_EDGES            # ЧЕРНЫЙ
        # SMOOTH                # ФОКУС (мало)
        # SMOOTH_MORE           # ФОКУС (больше)
        # SHARPEN               # Минус четкость (мало)


        filtered_image = img.filter(ImageFilter.EMBOSS)
        filtered_image.save(f"photo/Original/{message.chat.id}.jpg")


        #  TEXT  #

        # img = ImageDraw.Draw(img)
        # headline = ImageFont.truetype("arial.ttf", size=30)
        # img.text((40, 20), "Text")


        #  LINK  #

        # url = input("Отправьте ссылку: ")
        # response = requests.get(message.text, stream = True).raw
        # img = Image.open(response)
        # img.save("photo.jpg")
        

        with open(f"photo/Original/{message.chat.id}.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, reply_markup=inline_markup.effects_inline)
            





#  CALLBACK  #

@bot.callback_query_handler(func=lambda call: True)
def inline(call):


    if call.data == "back_inline":
        with open(f"photo/Original/{call.message.chat.id}.jpg", "rb") as photo:
            bot.send_message(call.message.chat.id, '<b> Выберите эффект: </b>', parse_mode="html")
            bot.send_photo(call.message.chat.id, photo, reply_markup=inline_markup.effects_inline)

    if call.data == "reset_inline":
        with open(f"photo/Original/{call.message.chat.id}.jpg", "rb") as photo:
            bot.send_chat_action(call.message.chat.id, 'upload_photo')
            bot.send_message(call.message.chat.id, '<b> ❌  Все эффекты удалены </b>', parse_mode="html")
            bot.send_photo(call.message.chat.id, photo, reply_markup=inline_markup.effects_inline)





    if call.data == "image":
        image(call.message)

    















if __name__=='__main__':

    while True:

        try:

            bot.polling(non_stop=True, interval=0)

        except Exception as e:

            print(e)
            sleep(5)
            continue