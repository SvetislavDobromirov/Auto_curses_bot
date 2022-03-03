from yookassa import Configuration, Payment
from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentTypes
from aiogram.utils import executor


import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from datetime import datetime, timedelta
import datetime
import database
#import time
import time_check
import texts
import settings
import keyboards
import datetime
import list_video
import logging

global dict_of_users
global admin_list
admin_list = (658697862,)


async def log(text):
    
    time = time_check.time_now()
    text = f"{time} {text}\n"
    with open("log.txt", "a") as file:
        file.write(text)




#setup YOUKASSA    
Configuration.account_id = settings.YOUKASSA_account_id
Configuration.secret_key = settings.YOUKASSA_secret_key

#create Aiogram dispatcher
bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    #checking user for registration
    #If User not registered, reg him.
    if check_new_user(chat_id) == False:
        await new_user_act(message)
        
    #IF status ACTIVE, then show when will be awaking.
    #Else, offer to follow..
    else:
        if await check_status(chat_id) == "ACTIVE":
            time = dict_of_users[chat_id][5]
            set_x = dict_of_users[chat_id][6]
            text = texts.when_class_text(time, set_x)
            await bot.send_message(chat_id, f"Привет!\n{text}")
        elif await check_status(chat_id) == "NEW":
            text = texts.offer_follow_text
            await bot.send_message(chat_id, text)
        elif await check_status(chat_id) == "TRY":
            time = dict_of_users[chat_id][5]
            set_x = dict_of_users[chat_id][6]
            text = texts.when_class_text(time, set_x)
            await bot.send_message(chat_id, text)
        

            

async def new_user_act(message):
    chat_id = message.chat.id
    msg_id = message.message_id
    await bot.send_message(chat_id, texts.greeting_text)
    add_new_user(message)
    text = texts.offer_test_class_text
    await bot.send_message(chat_id, text, reply_markup = keyboards.try_class_keyboard)
    asyncio.create_task(delete_try_class(chat_id, msg_id))

async def delete_try_class(chat_id, message_id):
    global dict_of_users
    #print("Поток delete сreated")
    day_today = datetime.datetime.today().weekday()
    flag = True
    status = ""
    while day_today == datetime.datetime.today().weekday() and status != "TRY":
        await asyncio.sleep(300)
        status = dict_of_users[chat_id][3]
    if status != "TRY":
        try:
            await delete_message(chat_id, message_id)
        except:
        #90A
           text = "Ошибка удаления сообщения. Код: 90A"
           log(text)
        
@dp.message_handler(commands = ['info'])
async def info(message: types.Message):
    chat_id = message.chat.id
    if check_new_user(chat_id) == False:
        await new_user_act(message)
    
    list_info = (dict_of_users[chat_id][3], dict_of_users[chat_id][4],
                 dict_of_users[chat_id][5], dict_of_users[chat_id][6])
    text = texts.create_info_message(list_info)
    await bot.send_message(chat_id, text)

@dp.message_handler(commands = ['follow'])
async def follow(message: types.Message):
    chat_id = message.chat.id
     #If User not registered, reg him.
    if check_new_user(chat_id) == False:
        await new_user_act(message)
    
    status = await check_status(chat_id)
    if status == "ACTIVE":
        days_left = dict_of_users[chat_id][4]
        await bot.send_message(chat_id, f"Осталось {days_left} занятий.")
        #!!! TIME WITH NEXT CLASS
    elif status == "NEW" and "set" not in dict_of_users[chat_id][6]:
        text = texts.schedule_text
        await bot.send_message(chat_id, text)
        text = ("Обрати внимание, что выбрать расписание можно только один раз.")
        await bot.send_message(chat_id, text, reply_markup = keyboards.set_mode_keyboard)
    elif status  == "NEW" and "set" in dict_of_users[chat_id][6]:
        
        await offer_pay(chat_id)
    elif status == "TRY":
        text = "Подписка на занятия будет доступна после пробного занятия."
        await bot.send_message(chat_id, text)
            #Set schedule alrady done.

            
@dp.message_handler(commands = ['set_time'])
async def set_time(message: types.Message):
    chat_id = message.chat.id
     #If User not registered, reg him.
    if check_new_user(chat_id) == False:
        await new_user_act(message)
    
    global dict_of_users
    chat_id = message.chat.id
    status = await check_status(chat_id)
    
    if status == "ACTIVE":
        time = dict_of_users[chat_id][5]
        if time == 0:
            text = (f'СИСТЕМНАЯ ОШИБКА. Вы еще не настроили утреннее время.\n Пора подписаться?')
            #Keyboard "Yes" and function about payments'
            keyboard = keyboards.follow_keyboard

        else:
            text = (f'Настроенное время: {time}\n')
                  
            #Keyboard: "Choose_set_time" and starting tree with setting time
            keyboard = keyboards.choose_set_time_keyboard
        
        await bot.send_message(chat_id, text) 
        text = 'Настройка времени\n'
        await bot.send_message(chat_id, text, reply_markup = keyboard)
    
    elif status == "NEW":
        await bot.send_message(chat_id, "Чтобы перейти к настройке времени, сперва нужно подписаться. Нажмите /follow или выберите соответствуюзий пункт в меню.")    
    
    elif status == "TRY":
        await bot.send_message(chat_id, "Чтобы перейти к настройке времени, сперва нужно подписаться. Нажмите /follow или выберите соответствуюзий пункт в меню.")    
    
@dp.message_handler(commands = ['contacts'])
async def contacts(message: types.Message):
    chat_id = message.chat.id
    if check_new_user(chat_id) == False:
        await new_user_act(message)
    text = texts.contact_text
    await bot.send_message(chat_id, text)


#CALLBACK

                           
@dp.callback_query_handler()
async def callback(callback_query: types.CallbackQuery):
    global dict_of_users
    chat_id = callback_query.message.chat.id
    #DELETE BUTTONS
    try:
        await bot.delete_message(chat_id, message_id=callback_query.message.message_id)
    except:
        #180A
        text = "Ошибка удаления файла. Код: 180А"
    #ALL BUTTONS AND TEXTS DIFFERENT BOT_SEND
    
    
    #print(callback_query)
    data = callback_query.data
    #print(data)
    #print(f"{await check_status(chat_id)}")
    if 'settime' in data:
        flag = 0
        time = ""
        #pressed Button_set_time
        for el in data:
            
            if el == "_":
                flag = 1
            elif flag ==1:
                time = f"{time}{el}"
        change_time(chat_id, time)
        #print(dict_of_users[chat_id])
        await bot.send_message(chat_id, f"Время {time} успешно установлено.")
        time = dict_of_users[chat_id][5]
        set_x = dict_of_users[chat_id][6]
        text = texts.when_class_text(time, set_x)
        
        await bot.send_message(chat_id, text)
        
    elif data == "start":
        if dict_of_users[chat_id][3] == "TRY":
            dict_of_users[chat_id][3] = "NEW"
            temp_list = dict_of_users[chat_id]
            await update_info(temp_list)
            
            message_id=callback_query.message.message_id
            asyncio.create_task(send_class(chat_id, message_id))
            #ОТПРАВИТЬ ЗАНЯТИЕ
        result = time_check.hour_2_check(dict_of_users[chat_id][5])
        if dict_of_users[chat_id][3] == "ACTIVE" and result == False:
            await bot.send_message(chat_id, "Время, отведенное на занятие сегодня истекло. Ыы можете изменить время на более подходящее.")
        elif dict_of_users[chat_id][3] == "ACTIVE" and result == True:
            if "lite" in dict_of_users[chat_id][6]:
                await minus_class(chat_id)
                
            message_id=callback_query.message.message_id
            asyncio.create_task(send_class(chat_id, message_id))

        
            
            #check dict for "lite" in mode, if yes, minus session
            #catch ID
            #start send_async
        #Check hour + 2 
                
    elif data == "time_good":
        time = dict_of_users[chat_id][5]
        set_x = dict_of_users[chat_id][6]
        text = when_class_text(time, set_x)
        await bot.send_message(chat_id, f"Здорово!\n{text}")
        
    elif data == "start_time_setting":
        _set_time = start_time_setting(chat_id)
        await _set_time.keyboard_hours()
        
    elif 'setmode' in data  and "set" not in dict_of_users[chat_id][6]:
        #print(callback_query)
        if data == "setmode_3":
            mode = "set3"
            dict_of_users[chat_id][6] = "set3"
            days = 3
            text = texts.create_text_good_choose(days)
            await bot.send_message(chat_id, text)
        elif data == "setmode_5":
            mode = "set5"
            dict_of_users[chat_id][6] = "set5"
            days = 5
            text = texts.create_text_good_choose(days)
            await bot.send_message(chat_id, text)
        elif data == "setmode_7":
            mode = "set7"
            dict_of_users[chat_id][6] = "set7"
            days = 7
            text = texts.create_text_good_choose(days)
            await bot.send_message(chat_id, text)
            
        #Rewrite MODE in database    
        first_name = dict_of_users[chat_id][1]
        last_name = dict_of_users[chat_id][2]
        status = dict_of_users[chat_id][3]
        days = dict_of_users[chat_id][4]
        time = dict_of_users[chat_id][5]
        database.update_status(chat_id, first_name, last_name, status, days, time, mode)
        await offer_pay(chat_id)
        
        
    elif 'setmode' in data  and "set" in dict_of_users[chat_id][6]:
        
        
        await bot.send_message(chat_id, "Выбор расписания уже сделан.")
            
    elif 'cl' in data:
        text = texts.agreement_text
        await bot.send_message(chat_id, text)       
        if data == "cl_5":
            summ_for_payment = 1300
            q_cl = 5
            set_mode = ""
            
           
        elif data == "cl_30":
            summ_for_payment = 6900
            q_cl = 30
            set_mode = ""
            
        elif data == "cl_90":
            summ_for_payment = 13500
            q_cl = 90
            set_mode = ""
            
        elif data == "cll_5":
            summ_for_payment = 1500
            q_cl = 5
            set_mode = "_lite"
            
           
        elif data == "cll_30":
            summ_for_payment = 7500
            q_cl = 30
            set_mode = "_lite"
            
            
        elif data == "cll_90":
            summ_for_payment = 14900
            q_cl = 90
            set_mode = "_lite"
        if "lite" in set_mode:
            description = "Предоплата за f{q_cl} занятий Йога Пробуждения без возможности переноса занятий."
        else:
            description = "Предоплата за f{q_cl} занятий Йога Пробуждения с возможностью переноса занятий."

        #ЗАТЫЧКА!!!!
        #summ_for_payment = 100
        ####
            
        payment = Payment.create({
        "amount": {
            "value": f"{summ_for_payment}",
            "currency": "RUB"
        },
         "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/yoga_time_awakening_bot"
        },
        "capture": True,
        "description": f"{description}",
        "metadata": {
        "order_id": "0"
        }})
        ###ЗАТЫЧКА!!!
        #payment_url = payment.confirmation.confirmation_url
        payment_url = "vk.com"

        inline_button_url = InlineKeyboardButton('Перейти на страницу оплаты.', url=payment_url)
        inline_keyboard_url = InlineKeyboardMarkup().add(inline_button_url)

        text = ('Остался последний шаг!\n'
        'Переходите на страницу оплаты, чтобы пройти новый путь!\n')
                          
        photo_url = "https://ibb.co/2h6XHkL"

        await bot.send_photo(chat_id,photo=photo_url,caption=text,reply_markup=inline_keyboard_url)
    
        
        task = asyncio.create_task(check_pay(chat_id, payment.id, q_cl, set_mode))
        
    elif data == "try":
       
        dict_of_users[chat_id][3] = "TRY"
        dict_of_users[chat_id][5] = "06:00"
        temp_list = dict_of_users[chat_id]
        await update_info(temp_list)
        text = texts.info_about_try_text
        await bot.send_message(chat_id, text)
####КОПИЯ СТАРТ###        
@dp.message_handler()
async def start(message: types.Message):
    chat_id = message.chat.id
    #checking user for registration
    #If User not registered, reg him.
    if check_new_user(chat_id) == False:
        await new_user_act(message)
        
    #IF status ACTIVE, then show when will be awaking.
    #Else, offer to follow..
    
    if await check_status(chat_id) == "ACTIVE":
        time = dict_of_users[chat_id][5]
        set_x = dict_of_users[chat_id][6]
        text = texts.when_class_text(time, set_x)
        await bot.send_message(chat_id, f"Привет!\n{text}")
    elif await check_status(chat_id) == "NEW":
        text = texts.offer_follow_text
        await bot.send_message(chat_id, text)
    elif await check_status(chat_id) == "TRY":
        time = dict_of_users[chat_id][5]
        set_x = dict_of_users[chat_id][6]
        text = texts.when_class_text(time, set_x)
        await bot.send_message(chat_id, text)      
####         
        
async def offer_pay(chat_id):
    text = texts.price_part1_text
    await bot.send_message(chat_id, text)
    
    text = texts.price_part2_text
    await bot.send_message(chat_id, text, reply_markup = keyboards.classes_keyboard)
       

async def check_pay(chat_id, payment_id,q_classes, set_mode):
    global dict_of_users
    confirm = False
    wait = 0
    
    while confirm == False:
        print ("416 str")
        #Запрашиваем статус платежа
        payment = Payment.find_one(payment_id)
        status = payment.status
        
        #ЗАТЫЧКА!
        await asyncio.sleep(5)
        status = "succeeded"
        ##############
        
        if status == "succeeded":
           
            await bot.send_message(chat_id, "Платеж проведен успешно.")
            #ЗАПРОС ИЗ PAYMENT СУММЫ?
            await got_payment(chat_id, q_classes)
            mode = f"{dict_of_users[chat_id][6]}{set_mode}"
            dict_of_users[chat_id][6] = mode
            dict_of_users[chat_id][5] = "7:30"
            dict_of_users[chat_id][3] = "ACTIVE"
            temp_list = dict_of_users[chat_id]
            await update_info(temp_list) #update database
            confirm = True
            # here place with offer set_time, if time not set
            time = dict_of_users[chat_id][5]
            
            if time == 0:
                _set_time = start_time_setting(chat_id)
                await _set_time.keyboard_hours()
                
            elif ":" in time:
                text = ( f"Время занятий: {time}.\n"
                        "Чтобы изменить время, нажмите /set_time или выберите соответствующий пункт в меню.")
                await bot.send_message(chat_id, text)
                pass
            #Дальнешие действия после подтверждения платежа
        elif status == "canceled":
            
            
            await bot.send_message(chat_id, "Ошибка платежа. Повторите попытку.")
            confirm = True
        
        
        await asyncio.sleep(5)
        wait = wait + 5
        if wait > 600:
            
            
            await bot.send_message(chat_id, "Время платежа истекло.")
            confirm = True
       
            
            

async def got_payment(chat_id, q_classes):
    global dict_of_users
    #NOT ASYNC!!!
    plus_days(chat_id, q_classes)

    #Send congratulations to user
    classes = dict_of_users[chat_id][4]
    text = (f"Поздравляю! Платеж совершен успешно! Занятий осталось: {classes}.")
    await bot.send_message(chat_id, text)

    #Send Admin's notification
    name = dict_of_users[chat_id][1]
    if dict_of_users[chat_id][2] != None:
            name = f"{name} {dict_of_users[chat_id][2]}"
    if "lite" in dict_of_users[chat_id][6]:
            sett = "lite"
    else:
        sett = "hardcore"
    text = f"Пользователь по имени {name} совершил покупку {q_classes} занятий в режиме {sett}."
    await system_message_admin(text)

    #create dict_class and new user to file
    dict_class = list_video.load_dict()
    dict_class[chat_id] = 1
    list_video.write_dict(dict_class)

    
#____________________________________________________________________
# Check user on registration. Return True or False
# If user found = True, Else = False

#Прибавляет дни подписки после оплаты
def plus_days(chat_id, q_classes):
    global dict_of_users

    #DICT = dict[chat_id]:[chat_id][name][last_name][[status][days_left][time][mode]
    
    
    chat_id = dict_of_users[chat_id][0]
    first_name = dict_of_users[chat_id][1]
    last_name = dict_of_users[chat_id][2]
    

    #Увеличение количества дней в базе данных
    status = 'ACTIVE'
    time  = dict_of_users[chat_id][5]
    
    mode = dict_of_users[chat_id][6]
    
    database.update_status(chat_id, first_name, last_name, status, q_classes, time, mode)
    #Обновление словаря
    dict_of_users = database.create_dict_list_allinfo()

async def minus_class(chat_id):
    global dict_of_users
    temp_list = dict_of_users[chat_id]
    temp_list[4] = temp_list[4] - 1
    if temp_list[4] <= 0:
        await bot.send_message(chat_id, "Сожалею, но подписка на занятия закончилась. Чтобы продолжить заниматься, нажмите /follow или выбери соответствущий пункт меню.")
        temp_list[3] = "NEW"
    dict_of_users[chat_id] = temp_list
    await update_info(temp_list)
     
async def system_message_admin(text):
    global admin_list
    for el in admin_list:
        await bot.send_message(el, text)   

class start_time_setting():
    def __init__(self, chat_id):
        self.chat_id = chat_id
        
    async def keyboard_hours(self):
        await bot.send_message(self.chat_id, "Выберите походящее время.", reply_markup = keyboards.hours_keyboard)
    async def setup_hours(self):
        pass
async def check_status(chat_id):
    global dict_of_users
    status = dict_of_users[chat_id][3]
    return status
    
    
def change_time(chat_id, time):
    global dict_of_users
    first_name = dict_of_users[chat_id][1]
    last_name = dict_of_users[chat_id][2]
    status = dict_of_users[chat_id][3]
    days = dict_of_users[chat_id][4]
    mode = dict_of_users[chat_id][6]

    #Update database
    database.update_status(chat_id, first_name, last_name, status, days, time, mode)
    #Update dict
    dict_of_users = database.create_dict_list_allinfo()
    pass

def check_new_user(chat_id):
    result = database.check_user(chat_id)
    return result
    
# Add new user in database and in local dictionary
#LIST FOR WRITE = list= [chat_id][name][last_name][[status][days_left]
def add_new_user(message):
    global dict_of_users
    
    chat_id = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    status = 'NEW'
    day = 0
    time = 0
    mode = ""
    dict_of_users[chat_id] = [chat_id, first_name, last_name, status, day, time, mode]
    list_for_write = [chat_id, first_name, last_name, status, day, time, mode]

    #Write to database
    database.write(list_for_write)
    #Update dict_of_user
    #dict_of_users = database.create_dict_list_allinfo()
    

# If info updated(status, days...) update database and local dictionary
async def update_info(temp_list):
     database.update_status(temp_list[0], temp_list[1], temp_list[2], temp_list[3], temp_list[4], temp_list[5], temp_list[6])
 
    

#___ASYNC___

async def send_classes():
    global dict_of_users
    iteration = False
    while True:
        print("Цикл_потока")
        for el in dict_of_users.keys():
            chat_id = dict_of_users[el][0]
            
            status = await check_status(chat_id)
                 
            if status == "TRY" and time_check.time_check(dict_of_users[chat_id][5]) == True:
                
                text = ("Доброе утро! Готовы сделать первый шаг?\n Тогда нажимайте на кнопку и вперед!")
                await bot.send_message(chat_id, text, reply_markup =keyboards.start_keyboard)
                iteration == True
                
            if status == "TRY" and time_check.time_check("10:01"):
                dict_of_users[chat_id][3] = "NEW"
                temp_list = dict_of_users[chat_id]
                await update_info(temp_list)
            
            if status == "ACTIVE":
               
                time_for_check = dict_of_users[chat_id][5]### AWAIT minute
                if time_check.time_check(time_for_check) == True:
                   
                    schedule = dict_of_users[chat_id][6]
                    day_week = datetime.datetime.today().weekday()
                    set_5_day_list = (0,1,2,3,4)
                    set_3_day_list = (1,3,5)
                    #"""ЭМУЛЯЦИЯ"""
                    #set_5_day_list = (0,1,2,3,4)
                    #set_3_day_list = (0,3,5)
                    
                    iteration = True
                    
                    if "set3" in schedule and day_week in set_3_day_list:
                        #print("set3 in schedule")
                        if "lite" in schedule:
                            text = ("Доброе утро!) Готовы приступить к занятию?\n"
                                    "Можно начать в течении двух часов.\n")
                            await bot.send_message(chat_id, text, reply_markup =keyboards.start_keyboard)
                            
                        elif schedule == "set3":
                            text = ("Доброе утро!) Готовы приступить к занятию?\n"
                                    "Видео доступно в течении двух часов\n"
                                    "Если вы пропустите занятие, оно сгорит")
                            await minus_class(chat_id)
                            await bot.send_message(chat_id, text, reply_markup =keyboards.start_keyboard)
                        
                        #ChecK_mode
                        #If check_mode hard - create_task - send_1()
                        #If check_mode easy - send button and create waiting function to delete button
                        #-- Then create_task - send_1
                        
                        
                    elif "set5" in schedule and day_week in set_5_day_list:
                        if "lite" in schedule:
                            text = ("Доброе утро!) Готовы приступить к занятию?\n"
                                    "Можно начать в течении двух часов.\n")
                            await bot.send_message(chat_id, text, reply_markup =keyboards.start_keyboard)
                            
                        elif schedule == "set5":
                            text = ("Доброе утро!) Готовы приступить к занятию?\n"
                                    "Видео доступно в течении двух часов\n"
                                    "Если вы пропустите занятие, оно сгорит")
                            await minus_class(chat_id)
                            await bot.send_message(chat_id, text,reply_markup = keyboards.start_keyboard)
                        
                        
                    elif "set7" in schedule:
                        if "lite" in schedule:
                            text = ("Доброе утро!) Готовы приступить к занятию?\n"
                                    "Можно начать в течении двух часов.\n")
                            await bot.send_message(chat_id, text, reply_markup =keyboards.start_keyboard)
                            
                        elif schedule == "set7":
                            text = ("Доброе утро!) Готовы приступить к занятию?\n"
                                    "Видео доступно в течении двух часов\n"
                                    "Если вы пропустите занятие, оно сгорит")
                            await minus_class(chat_id)
                            await bot.send_message(chat_id, text,reply_markup = keyboards.start_keyboard)
       
            
        if iteration == True:
            await asyncio.sleep(15)
        await asyncio.sleep(55)


                        
                    
async def check_last_day(chat_id):
    global dict_of_users
    temp_list = dict_of_users[chat_id]
    if temp_list[4] <= 0:
        await bot.send_message(chat_id, "Сожалею, но подписка на занятия закончилась. Чтобы продолжить заниматься, нажми /follow или выбери соответствущий пункт меню.")
        temp_list[3] = "NEW"
    dict_of_users[chat_id] = temp_list
    await update_info(temp_list)
                
            
async def send_class(chat_id, message_id):
    global dict_of_users
   
    
    #print(f"Status before f(good_awaking) = {dict_of_users[chat_id][3]}")
    text = texts.good_awaking_text(dict_of_users[chat_id][3])
    await bot.send_message(chat_id, text)
    message_id = message_id +1
    status = dict_of_users[chat_id][3]
    if status == "NEW":
        link = list_video.vid[0]
    elif status == "ACTIVE":
        dict_class = list_video.load_dict()
        vinum = dict_class[chat_id] # current video for if
        if vinum > list_video.vi:
            while (vinum > list_video.vi):
                vinum = vinum - list_video.vi
        link = list_video.vid[vinum]
        vinum = vinum + 1
        dict_class[chat_id] = vinum
        list_video.write_dict(dict_class)
    else:
        print ("719 main wrong-status")
    await bot.send_message(chat_id, "Если видео не разворачивается на весь экран, рекомендую для просмотра видео перейти на youtobe")
    await bot.send_message(chat_id, link)

    
    message_id = message_id +1
    time_sec = 0
    if dict_of_users[chat_id][3] == "NEW":
        goal_time = 14400
    else: goal_time = 3600
    while time_sec < goal_time:
        time_sec = time_sec + 60
        await asyncio.sleep(60)
    
    try:
        await bot.delete_message(chat_id, message_id)
    except:
        #680A
        text = "Ошибка удаления файла. Код: 680A"
        log(text)
    await asyncio.sleep(1)
    try:
        await bot.delete_message(chat_id, message_id=message_id-1)
    except:
        #680B
        text = "Ошибка удаления файла. Код: 680B"
        log(text)

    time = dict_of_users[chat_id][5]
    set_x = dict_of_users[chat_id][6]
    text_when = when_class_text(time, set_x)
    if dict_of_users[chat_id][3] == "NEW":
        text = ("Время, отведенное на пробное занятие закончилось.\n"
                "Чтобы подписаться, нажмите /follow или выберете соответствующий пункт меню.")
    else: text = f"Время, отведеннон на занятие, закончилось.\n{text_when}"
    await bot.send_message(chat_id, text)
    await bot.send_message(chat_id, (f"Хотите поделиться опытом, оставить отзыв или "
                                    "пообщаться с единомышленниками?\n"
                                     "Присоединяйтесь к чату) https://t.me/YogaTime_chat\n"))
    
    await check_last_day(chat_id)

    

    
    



#Start async tasks
async def start_async(x):
    asyncio.create_task(send_classes())


#__RUN___
if __name__ == '__main__':
    logging.basicConfig(filename='example.log', level=logging.DEBUG)
    #logging.debug('This message should go to the log file')
    #logging.info('So should this')
    #logging.warning('And this, too')
        
    #Download dictionary with users
    #DICT = dict[chat_id]:[chat_id][name][last_name][[status][days_left][time][mode]
    dict_of_users = database.create_dict_list_allinfo()
    #print(dict_of_users)
    
    executor.start_polling(dp, skip_updates=True, on_startup=start_async)
