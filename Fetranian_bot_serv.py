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

FT1 = "🔶🔶🔶🔶🔶 🔶🔶🔶🔶🔶\n"
FT2 = "🔶🔶🔶🔶🔶 🔶🔶🔶🔶🔶\n"
FT3 = "🔶🔶🔶🔶🔶 🔶🔶🔶🔶🔶\n"
fetranit = FT1 + FT2 + FT3 

def add_data(data):
    connection = mysql.connector.connect(host='localhost',database='Fetranian_tricks',user='root',password='Extremm0')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO `fetranian_tricks`.`tricks` (T1,T2,T3,T4,T5,T6,T7,T8,T9,T10,T11,T12,T13,T14,T15,T16,T17,T18,T19,T20,T21,T22,T23,T24,T25,T26,T27,T28,T29,T30) VALUES (" + ", ".join(str(x) for x in data) + ");")
    connection.commit()
    print("Отправлено")
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
    #print("число ", data[k-1])
    #print(counter)
        
            
        

def change(message, row, res):
    global fetranit, FT1, FT2, FT3, FT1_check, FT2_check, FT3_check
    if res == 1:
        if row == 1:
            FT1 = FT1.replace('🔶','💎', 1)
            FT1_check = FT1_check - 1
        elif row == 2:
            FT2 = FT2.replace('🔶','💎', 1)
            FT2_check = FT2_check - 1
        elif row == 3:
            FT3 = FT3.replace('🔶','💎', 1)
            FT3_check = FT3_check - 1
    elif res == 0:
        if row == 1:
            FT1 = FT1.replace('🔶','🔷', 1)
            FT1_check = FT1_check - 1
        elif row == 2:
            FT2 = FT2.replace('🔶','🔷', 1)
            FT2_check = FT2_check - 1
        elif row == 3:
            FT3 = FT3.replace('🔶','🔷', 1)
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
        bot.send_message(message.from_user.id, "Осталось огранить " + str(notgran) + " раз" + "\n Шанс успешной огранки " + str(round(chance*100))+"%" + "\n Математический шанс успешной огранки " + str(round(alt_chance*100, 2))+"%")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add('ТИР1 ✅', 'ТИР1 ❌')
        keyboard.add('ТИР2 ✅', 'ТИР2 ❌')
        keyboard.add('ТИР3 ✅', 'ТИР3 ❌')
        keyboard.add("FINISH")
        msg = bot.reply_to(message, fetranit, reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_step)

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Как многие знают, вероятность выпадения \"Орла\" при броске монетки составляет около 50%. Но если мы говорим о шансе выпадения двух \"Орлов\" в подряд, то этот шанс меняется в меньшую сторону. \n \n Этот бот позволяет высчитывать шанс удачной огранки фетранитов по схожему принципу исходя из вероятности совершения последовательных удачных или неудачных ударов молоточком. \n \n Для начала огранки введите команду \" /cut \". \n Для просмотра вcех доступных команд введите команду \" /help \"")
    if message.text == "/cut":
        bot.send_message(message.from_user.id, "Привет!") 
        cut(message, 3)
    if message.text == "/help":
        bot.send_message(message.from_user.id, "Если бот дал осечку или вы нашли ошибку, то пишите мне, его создателю. Мой ник в ТГ - @Ka_strazh, мой ник в игре - Эриабет. \n\n В будущем бот пополнится новой функцией предсказывающей наилучшее решение исходя из множества попыток огранки и будет опираться в том числе и на статистические данные. \n\n Доступные команды: \n/cut - начать огранку \n/help - вызвать это окно\n/start - запустить бота\n Помните что бот пока работает без хостинга так что активен лишь пока работает мой ноут. \n\n Для завершения огранки не забывайте нажимать кнопку FINISH")     
        

def process_step(message):
    global fetranit, FT1, FT2, FT3, FT1_check, FT2_check, FT3_check, data, notgran, chance, alt_chance, chance_comp, n
    chat_id = message.chat.id
    if message.text=='ТИР1 ✅':
        bot.send_message(message.from_user.id, "good")
        change(message, 1, 1)
        if FT1_check > 0:
            cut(message,1)
        else:
            cut(message,3)
    elif message.text=='ТИР1 ❌':
        bot.send_message(message.from_user.id, "not good")
        change(message, 1, 0)
        if FT1_check > 0:
            cut(message,0)
        else:
            cut(message,3)
    elif message.text=='ТИР2 ✅':
        bot.send_message(message.from_user.id, "good")
        change(message, 2, 1)
        if FT2_check > 0:
            cut(message,1)
        else:
            cut(message,3)
    elif message.text=='ТИР2 ❌':
        bot.send_message(message.from_user.id, "not good")
        change(message, 2, 0)
        if FT2_check > 0:
            cut(message,0)
        else:
            cut(message,3)
    elif message.text=='ТИР3 ✅':
        bot.send_message(message.from_user.id, "good")
        change(message, 3, 1)
        if FT3_check > 0:
            cut(message,1)
        else:
            cut(message,3)
    elif message.text=='ТИР3 ❌':
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
        
        FT1 = "🔶🔶🔶🔶🔶 🔶🔶🔶🔶🔶\n"
        FT2 = "🔶🔶🔶🔶🔶 🔶🔶🔶🔶🔶\n"
        FT3 = "🔶🔶🔶🔶🔶 🔶🔶🔶🔶🔶\n"
        fetranit = FT1 + FT2 + FT3 
        print("отработал")
    else:
        bot.send_message(message.from_user.id, "something got wrong")
        
bot.polling(none_stop=True, interval=0)

