import telebot;
import os
from telebot import types
from aiogram.dispatcher.filters import Text
import re
import mysql.connector


bot = telebot.TeleBot('Token_here');

normal_chance = [0.75, 0.65, 0.55, 0.45, 0.35, 0.25]

data = []
notgran = 30
FT1_check = 11;
FT2_check = 11;
FT3_check = 11;
n=0;
chance_comp = 0.75; 
chance = 0.75;
alt_chance = 0.75;

dic75 = [0.75, 0.488, 0.268, 0.121]
dic65 = [0.65, 0.358, 0.161, 0.056]
dic55 = [0.55, 0.248, 0.087, 0.022]
dic45 = [0.45, 0.158, 0.039, 0.01]
dic35 = [0.35, 0.088, 0.022, 0.005]
dic25 = [0.25, 0.063, 0.016, 0.004]

FT1 = "๐ถ๐ถ๐ถ๐ถ๐ถ ๐ถ๐ถ๐ถ๐ถ๐ถ\n"
FT2 = "๐ถ๐ถ๐ถ๐ถ๐ถ ๐ถ๐ถ๐ถ๐ถ๐ถ\n"
FT3 = "๐ถ๐ถ๐ถ๐ถ๐ถ ๐ถ๐ถ๐ถ๐ถ๐ถ\n"
fetranit = FT1 + FT2 + FT3 

def add_data(data):
    connection = mysql.connector.connect(host='localhost',database='Fetranian_tricks',user='root',password='Extremm0')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO `fetranian_tricks`.`tricks` (T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23,T24,T25,T26,T27,T28,T29,T30) VALUES (" + ", ".join(str(x) for x in data) + ");")
    connection.commit()
    print("ะัะฟัะฐะฒะปะตะฝะพ")
def chance_normal():
    global n, chance
    print("data - ", data)
    chance_actual(data, chance)
    if ((data[-1] == 1) & (n+1 != 6)):
        n = n+1
    elif ((data[-1] == 0) & (n-1 != -1)):
        n = n-1
    chance = normal_chance[n]
    

def chance_actual(data, chance):
    global chance_comp, alt_chance
    k = len(data)
    counter = 0
    #print("k - ", k)
    while (k>1)&(data[k-1] == data[k-2]):
        k = k-1
        counter = counter + 1
    if counter == 0:
        chance_comp = chance
    elif counter > 2:
        counter = 2
        
    if data[k-1] == 1:
        alt_chance = eval('dic' + str(round(chance_comp*100))+'['+str(counter+1)+']')
    elif data[k-1] == 0:
        alt_chance = eval('1 - dic' + str(round(100 - chance_comp*100))+'['+str(counter+1)+']')
        
    #print('alt_chance',alt_chance)
    #print(chance, chance_comp)    
    #print("ัะธัะปะพ ", data[k-1])
    #print(counter)
        
            
        

def change(message, row, res):
    global fetranit, FT1, FT2, FT3, FT1_check, FT2_check, FT3_check
    if res == 1:
        if row == 1:
            FT1 = FT1.replace('๐ถ','๐', 1)
            FT1_check = FT1_check - 1
        elif row == 2:
            FT2 = FT2.replace('๐ถ','๐', 1)
            FT2_check = FT2_check - 1
        elif row == 3:
            FT3 = FT3.replace('๐ถ','๐', 1)
            FT3_check = FT3_check - 1
    elif res == 0:
        if row == 1:
            FT1 = FT1.replace('๐ถ','๐ท', 1)
            FT1_check = FT1_check - 1
        elif row == 2:
            FT2 = FT2.replace('๐ถ','๐ท', 1)
            FT2_check = FT2_check - 1
        elif row == 3:
            FT3 = FT3.replace('๐ถ','๐ท', 1)
            FT3_check = FT3_check - 1

    fetranit = FT1 + FT2 + FT3
    print(fetranit)
    #bot.send_message(message.from_user.id, fetranit)
    
def cut(message,result):
    global notgran
    global fetranit
    global data, chance

    print(data, chance, alt_chance)
    
    if notgran > 0:
        
        if result != 3:
            data.append(result)
            #print(data)#
            notgran = notgran -1
            chance_normal()
        bot.send_message(message.from_user.id, "ะััะฐะปะพัั ะพะณัะฐะฝะธัั " + str(notgran) + " ัะฐะท" + "\n ะจะฐะฝั ััะฟะตัะฝะพะน ะพะณัะฐะฝะบะธ " + str(round(chance*100))+"%" + "\n ะะฐัะตะผะฐัะธัะตัะบะธะน ัะฐะฝั ััะฟะตัะฝะพะน ะพะณัะฐะฝะบะธ " + str(round(alt_chance*100, 2))+"%")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add('ะขะะ?1 โ', 'ะขะะ?1 โ')
        keyboard.add('ะขะะ?2 โ', 'ะขะะ?2 โ')
        keyboard.add('ะขะะ?3 โ', 'ะขะะ?3 โ')
        keyboard.add("FINISH")
        msg = bot.reply_to(message, fetranit, reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_step)

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "ะะฐะบ ะผะฝะพะณะธะต ะทะฝะฐัั, ะฒะตัะพััะฝะพััั ะฒัะฟะฐะดะตะฝะธั \"ะัะปะฐ\" ะฟัะธ ะฑัะพัะบะต ะผะพะฝะตัะบะธ ัะพััะฐะฒะปัะตั ะพะบะพะปะพ 50%. ะะพ ะตัะปะธ ะผั ะณะพะฒะพัะธะผ ะพ ัะฐะฝัะต ะฒัะฟะฐะดะตะฝะธั ะดะฒัั \"ะัะปะพะฒ\" ะฒ ะฟะพะดััะด, ัะพ ััะพั ัะฐะฝั ะผะตะฝัะตััั ะฒ ะผะตะฝัััั ััะพัะพะฝั. \n \n ะญัะพั ะฑะพั ะฟะพะทะฒะพะปัะตั ะฒัััะธััะฒะฐัั ัะฐะฝั ัะดะฐัะฝะพะน ะพะณัะฐะฝะบะธ ัะตััะฐะฝะธัะพะฒ ะฟะพ ััะพะถะตะผั ะฟัะธะฝัะธะฟั ะธััะพะดั ะธะท ะฒะตัะพััะฝะพััะธ ัะพะฒะตััะตะฝะธั ะฟะพัะปะตะดะพะฒะฐัะตะปัะฝัั ัะดะฐัะฝัั ะธะปะธ ะฝะตัะดะฐัะฝัั ัะดะฐัะพะฒ ะผะพะปะพัะพัะบะพะผ. \n \n ะะปั ะฝะฐัะฐะปะฐ ะพะณัะฐะฝะบะธ ะฒะฒะตะดะธัะต ะบะพะผะฐะฝะดั \" /cut \". \n ะะปั ะฟัะพัะผะพััะฐ ะฒcะตั ะดะพัััะฟะฝัั ะบะพะผะฐะฝะด ะฒะฒะตะดะธัะต ะบะพะผะฐะฝะดั \" /help \"")
    if message.text == "/cut":
        bot.send_message(message.from_user.id, "ะัะธะฒะตั!") 
        cut(message, 3)
    if message.text == "/help":
        bot.send_message(message.from_user.id, "ะัะปะธ ะฑะพั ะดะฐะป ะพัะตัะบั ะธะปะธ ะฒั ะฝะฐัะปะธ ะพัะธะฑะบั, ัะพ ะฟะธัะธัะต ะผะฝะต, ะตะณะพ ัะพะทะดะฐัะตะปั. ะะพะน ะฝะธะบ ะฒ ะขะ - @Ka_strazh, ะผะพะน ะฝะธะบ ะฒ ะธะณัะต - ะญัะธะฐะฑะตั. \n\n ะ ะฑัะดััะตะผ ะฑะพั ะฟะพะฟะพะปะฝะธััั ะฝะพะฒะพะน ััะฝะบัะธะตะน ะฟัะตะดัะบะฐะทัะฒะฐััะตะน ะฝะฐะธะปัััะตะต ัะตัะตะฝะธะต ะธััะพะดั ะธะท ะผะฝะพะถะตััะฒะฐ ะฟะพะฟััะพะบ ะพะณัะฐะฝะบะธ ะธ ะฑัะดะตั ะพะฟะธัะฐัััั ะฒ ัะพะผ ัะธัะปะต ะธ ะฝะฐ ััะฐัะธััะธัะตัะบะธะต ะดะฐะฝะฝัะต. \n\n ะะพัััะฟะฝัะต ะบะพะผะฐะฝะดั: \n/cut - ะฝะฐัะฐัั ะพะณัะฐะฝะบั \n/help - ะฒัะทะฒะฐัั ััะพ ะพะบะฝะพ\n/start - ะทะฐะฟัััะธัั ะฑะพัะฐ\n ะะพะผะฝะธัะต ััะพ ะฑะพั ะฟะพะบะฐ ัะฐะฑะพัะฐะตั ะฑะตะท ัะพััะธะฝะณะฐ ัะฐะบ ััะพ ะฐะบัะธะฒะตะฝ ะปะธัั ะฟะพะบะฐ ัะฐะฑะพัะฐะตั ะผะพะน ะฝะพัั. \n\n ะะปั ะทะฐะฒะตััะตะฝะธั ะพะณัะฐะฝะบะธ ะฝะต ะทะฐะฑัะฒะฐะนัะต ะฝะฐะถะธะผะฐัั ะบะฝะพะฟะบั FINISH")     
        

def process_step(message):
    global fetranit, FT1, FT2, FT3, FT1_check, FT2_check, FT3_check, data, notgran, chance, alt_chance, chance_comp, n
    chat_id = message.chat.id
    if message.text=='ะขะะ?1 โ':
        bot.send_message(message.from_user.id, "good")
        change(message, 1, 1)
        if FT1_check > 0:
            cut(message,1)
        else:
            cut(message,3)
    elif message.text=='ะขะะ?1 โ':
        bot.send_message(message.from_user.id, "not good")
        change(message, 1, 0)
        if FT1_check > 0:
            cut(message,0)
        else:
            cut(message,3)
    elif message.text=='ะขะะ?2 โ':
        bot.send_message(message.from_user.id, "good")
        change(message, 2, 1)
        if FT2_check > 0:
            cut(message,1)
        else:
            cut(message,3)
    elif message.text=='ะขะะ?2 โ':
        bot.send_message(message.from_user.id, "not good")
        change(message, 2, 0)
        if FT2_check > 0:
            cut(message,0)
        else:
            cut(message,3)
    elif message.text=='ะขะะ?3 โ':
        bot.send_message(message.from_user.id, "good")
        change(message, 3, 1)
        if FT3_check > 0:
            cut(message,1)
        else:
            cut(message,3)
    elif message.text=='ะขะะ?3 โ':
        bot.send_message(message.from_user.id, "not good")
        change(message, 3, 0)
        if FT3_check > 0:
            cut(message,0)
        else:
            cut(message,3)
    elif message.text=='FINISH':
        

        print (len(data))
        if len(data) == 30:
            add_data(data)
            bot.send_message(message.from_user.id, "Thank's for using this bot! \n You can always try again! \n try to use /cut command to start a new cut")
        else:
            bot.send_message(message.from_user.id, "If you make it through the end it will help us to eans stats and make this bot better :)\n Also use /cut command to start a new cut")

        normal_chance = [0.75, 0.65, 0.55, 0.45, 0.35, 0.25]            
        data = []
        notgran = 30
        n=0;
        chance_comp = 0.75; 
        chance = 0.75;
        alt_chance = 0.75;
        FT1_check = 11;
        FT2_check = 11;
        FT3_check = 11;
        
        FT1 = "๐ถ๐ถ๐ถ๐ถ๐ถ ๐ถ๐ถ๐ถ๐ถ๐ถ\n"
        FT2 = "๐ถ๐ถ๐ถ๐ถ๐ถ ๐ถ๐ถ๐ถ๐ถ๐ถ\n"
        FT3 = "๐ถ๐ถ๐ถ๐ถ๐ถ ๐ถ๐ถ๐ถ๐ถ๐ถ\n"
        fetranit = FT1 + FT2 + FT3 
        print("ะพััะฐะฑะพัะฐะป")
    else:
        bot.send_message(message.from_user.id, "something got wrong")
        
bot.polling(none_stop=True, interval=0)

