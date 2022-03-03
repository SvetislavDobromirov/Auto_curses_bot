from yookassa import Configuration, Payment
from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentTypes
from aiogram.utils import executor

"""
#---Logging
import logging
global a
logging.basicConfig(filename='logs.log', filemode='a', format=f'%(asctime)s - %(message)s') 
def logs(info):
    global a
    logging.warning(f"{a}. {info}")
    a = a+1
#---Logging
"""

import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from datetime import datetime, timedelta
import database
from threading import Thread
import time
import time_check
import texts

global dict_of_users
dict_of_users = dict()

private_channel_id = -1001719626487 #

Configuration.account_id = 862996
Configuration.secret_key = "live_gBoCvpBgqbQnhBX1qqpGQ1ls7HtELIg0GBXOLF87AAw"


summ_for_payments = 500.00


BOT_TOKEN = '2132311402:AAGssUUNOY4n7XTCXaR7Yg0p0h5kD36TzM4'
#TEST# PAYMENTS_PROVIDER_TOKEN = '381764678:TEST:31789'
PAYMENTS_PROVIDER_TOKEN = '390540012:LIVE:21183'

#Для отправки системных сообщений админу(ам) кортеж
admin_list = (658697862, 385899565) 

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)




#Кнопка оплатить
inline_button = InlineKeyboardButton('Вперед', callback_data='pay_button')
inline_keyboard = InlineKeyboardMarkup().add(inline_button)




check_time = "10:00"


three_days = texts.three_days
one_day = texts.one_day
zero_days = texts.zero_days


            
           

        
    
@dp.message_handler(content_types=types.ContentType.TEXT)
async def cmd_start_text(message: types.Message):
    text = message.text
    if text == 'start' or text == 'старт' or text == 'начать':
        a = check_new_user(message)#True- найден, False - создан новый
        if a == False:#Пользователь не найден, зарегистрирован, отсылается приветственное сообщение
            await bot.send_message(message.chat.id, texts.start_text_NEW)
        elif a == True:#Пользователь найден, отсылаются подходящие сообщения
            await message_for_command_start(message)
    else:
        await bot.send_message(message.chat.id, "Чтобы начать выберете пункт меню или введите start")
    
    
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    a = check_new_user(message)#True- найден, False - создан новый
    if a == False:#Пользователь не найден, зарегистрирован, отсылается приветственное сообщение
        await bot.send_message(message.chat.id, texts.start_text_NEW)
    elif a == True:#Пользователь найден, отсылаются подходящие сообщения
        await message_for_command_start(message)
        
        


@dp.message_handler(commands=['subplus', 'subnew'])
async def payment(message: types.Message):
    #Отправляем информацию о платеже + кнопка
    info_payment_text = texts.info_payment_text
    await bot.send_message(message.chat.id, info_payment_text,
                           reply_markup=inline_keyboard)
    await asyncio.sleep(1)

@dp.message_handler(commands=['check'])
async def check(message: types.Message):
    await system_message_admin('Проверка всех собщений.')
    await asyncio.sleep(1)

    lis=([texts.start_text_END, texts.start_text_NEW,
    texts.start_text_ACTIVE,
    texts.info_text_ACTIVE("Тест", 10),
    texts.info_payment_text,
    texts.info_text("Test"),
    texts.three_days,
    texts.one_day,
    texts.zero_days
          ])

    for el in lis:
        await system_message_admin(el)
        await asyncio.sleep(1)
    
    

                           
@dp.callback_query_handler()
async def process_callback_button1(callback_query: types.CallbackQuery):

    chat_id = callback_query.message.chat.id
    
#Создаем платеж
    payment = Payment.create({
        "amount": {
            "value": f"{summ_for_payments}",
            "currency": "RUB"
        },
         "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/otkrovenieN_bot"
        },
        "capture": True,
        "description": "Месячная подписка на канал Откровение",
        "metadata": {
        "order_id": "0"
        }})

   

    #Запрашиваем URL оплаты
    payment_url = payment.confirmation.confirmation_url
    
    #Создаем Кнопку-ссылку
    inline_button_url = InlineKeyboardButton('Перейти на страницу оплаты', url=payment_url)
    inline_keyboard_url = InlineKeyboardMarkup().add(inline_button_url)

    
    #Создаем сообщение-кнопку для платежа

    text = ('Остался последний шаг!\n'
        'Переходи на страницу оплаты, чтобы присоединиться к нам!\n')
                          
    photo_url = 'https://i.ibb.co/ZBLKjNQ/Whats-App-Image-2021-12-20-at-19-27-21.jpg'

    #После нажатия на кнопку, переходит
    await bot.send_photo(chat_id,photo=photo_url,caption=text,reply_markup=inline_keyboard_url)
    
    

       #Создаем потоковое задание на проверку платежа.
        #передаем
    print("Платежный поток создан")
    asyncio.create_task(check_pay(chat_id, payment.id))


async def check_pay(chat_id, payment_id):
    confirm = False
    wait = 0

    while confirm == False:
        #Запрашиваем статус платежа
        payment = Payment.find_one(payment_id)
        status = payment.status
        
        if status == "succeeded":
           
           
            
            await bot.send_message(chat_id, "Платеж проведен успешно")
            await got_payment(chat_id)
            confirm = True
            
            #Дальнешие действия после подтверждения платежа
        elif status == "canceled":
            
            
            print("Ошибка платежа. Повторите попытку.")
            await bot.send_message(chat_id, "Ошибка платежа. Повторите попытку.")
            confirm = True
            
        await asyncio.sleep(5)
        wait = wait + 5
        if wait > 600:
            
            
            await bot.send_message(chat_id, "Время платежа истекло")
            print("Время платежа истекло")
            confirm = True
            
        
       

async def got_payment(chat_id):

    #chat_id,
    
    global dict_of_users
    #Работа с базой данных
    #Добавить 30 дней.
    print(f"Платеж от пользователя {chat_id} подтвержден")

    #Продлевает подписку и изменяет статус на ACTIVE
    plus_days(chat_id, 31) 


    
        #Пригласительная ссылка
        #Сообщение о количестве оставшихся дней
    #Сообщение админу
    
    

    # Оплата подтверждена. Высылается уникальная ссылка
    channel_id = -1001719626487 #ID канала
    expire_date = datetime.now() + timedelta(days=1)
    link = await bot.create_chat_invite_link(channel_id, expire_date.timestamp, 1)
    privat_link = link.invite_link
    print(privat_link)  # https://t.me/.....


    
    #Отправка уведомления об оставшихся днях пользователю
    days = dict_of_users[chat_id][4]
    text = (f"До конца подписки осталось дней: {days}.")
    
    await bot.send_message(chat_id,
                           'Поздравляю! Держи приватную ссылку на канал!\n\n'
                           f'{privat_link}\n\n{text}\n'
                           f"Благодарю тебя!"
                           
                           )   

    #Сообщение Администратору об оплате

    name = dict_of_users[chat_id][1]
    if dict_of_users[chat_id][2] != None:
            name = f"{name} {dict_of_users[chat_id][2]}"
    text = f"Пользователь по имени {name} совершил оплату на сумму {summ_for_payments} рублей"
    await system_message_admin(text)
    ###

#Инфо
@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    chat_id = message.chat.id #For Check Status and days

    first_name = message.chat.first_name
    

    
    #Блок проверки нового пользователя
    a = check_new_user(message)#True- найден, False - создан новый
    if a == False:#Пользователь не найден, зарегистрирован, отсылается приветственное сообщение
        await bot.send_message(message.chat.id, texts.start_text_NEW)
    elif a == True:#Пользователь найден. Проверка статуса
        print("А-11")
        global dict_of_users
        status = dict_of_users[chat_id][3]
        print(dict_of_users[chat_id])
        
        if status == 'NEW' or status == 'END':
            print ("A-13")
            text = texts.info_text(first_name)
            await bot.send_message(chat_id, text)
            
            
        elif status == 'ACTIVE':
            print("A-12")
            days = dict_of_users[chat_id][4]
            text = texts.info_text_ACTIVE(first_name, days)
            await bot.send_message(chat_id, text)
        

    


#Пригласительная самоссылка на бота
@dp.message_handler(commands=['link'])
async def invite_bot_link(message: types.Message):
    link = "https://t.me/otkrovenieN_bot"
    text = ("Пригластельная ссылка на бота:\n"
            f"{link}")
    await bot.send_message(message.chat.id, text)

#контакты
@dp.message_handler(commands=['cont'])
async def contacta(message: types.Message):
    link = ("Контакты: \n"
            "Наталия Старченкова\n"
            "n_starchenkova@bk.ru\n"
            "тел. +7 985 467-75-17\n"
            
            
            "Алиса Бондарева\n"
            "alisabondareva06@gmail.com\n"
            "тел. +79150474325\n\n"
            
            "Пользовательское соглашение доступно по ссылке /agreed)")
            
    text = (f"{link}")
    await bot.send_message(message.chat.id, text)

#Пользовательское соглашение
@dp.message_handler(commands=['agreed'])
async def contacta(message: types.Message):
    msg_doc = 'BQACAgIAAxkBAAIDy2HB2P0rrUAZJC37Au62pBmeJ1F1AAKUEgACYG0QSsVBAAFWtuX3viME'
    await bot.send_document(message.chat.id, msg_doc)

#Помошь
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    text = ("1. Если вы оплатили, но не успели подписаться на канал, перейдите по ссылке /link_repeate \n"
            "2. Если у вас проблема с оплатой, напиши в службу техподдержки https://t.me/massage_svet\n"
            )
    await bot.send_message(message.chat.id, text )

#Повторная отправка ссылки активному пользователю
@dp.message_handler(commands=['link_repeate'])
async def link_repeate(message: types.Message):
    global dict_of_users
    chat_id = message.chat.id
    if dict_of_users[chat_id][3] == 'ACTIVE' or dict_of_users[chat_id][3] == 'ADMIN':

        chat_id = -1001719626487 #ID канала
        expire_date = datetime.now() + timedelta(days=1)
        link = await bot.create_chat_invite_link(chat_id, expire_date.timestamp, 1)
        privat_link = link.invite_link
        await bot.send_message(message.chat.id, f"Твоя личная ссылка на канал:\n{privat_link}")
        
    else:
        await bot.send_message(message.chat.id, "Чтобы получить ссылку на канал, нажми в меню: Подписаться")

#Хэндлер, реагирует на пустое сообщение, и проверяет пользователя на регистрацию
@dp.message_handler()
async def check_user(message: types.Message):
    print(f"Free....... {message}")
    a = check_new_user(message)#True- найден, False - создан новый
    if a == False:#Пользователь не найден, зарегистрирован, отсылается приветственное сообщение
        await bot.send_message(message.chat.id, texts.start_text_NEW)
    elif a == True:#Пользователь найден, отсылаются подходящие сообщения
        print("TRUE WORK")
        await message_for_command_start(message)

#-------------------------------------------------------Функции


#Проверяет нового пользователя.
    #Создает нового пользоватя.
        #Заносит нового пользователя в базу.
            #Заносит нового пользователя в словарь
                #Возвращает либо True, либо False
def check_new_user(message):
    global dict_of_users
    
    if message.chat.id in dict_of_users.keys():
        print(f"Пользователь найден")
        return True
        #Если старенький, если новенький...

        
    else:
        print(f"Пользователь не найден")
        info_logs = f"Новый пользователь: ID = {message.chat.id}"
        logs(info_logs)
        #Создаем нового пользователя
    #создаем нового пользователя
    ##Запись в БД
    chat_id = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    day = 0
    status = 'NEW'
    list_for_write = [chat_id, first_name, last_name, status, day]
    database.write(list_for_write)
    ###Обновление глобального словаря
    dict_of_users = database.create_dict_list_allinfo()
    
    info_logs = f"Новый ользователь зарегистрирован: ID = {message.chat.id}"
    logs(info_logs)
    
    return False
    #Приветствуем нового пользователя


async def message_for_command_start(message):
        global dict_of_users
        
        if dict_of_users[message.chat.id][3] == 'ACTIVE':
            await bot.send_message(message.chat.id, texts.start_text_ACTIVE)

        elif dict_of_users[message.chat.id][3] == 'END':
            await bot.send_message(message.chat.id, texts.start_text_END)





#Прибавляет дни подписки после оплаты
def plus_days(chat_id, days):
    global dict_of_users
    
    
    chat_id = dict_of_users[chat_id][0]
    first_name = dict_of_users[chat_id][1]
    last_name = dict_of_users[chat_id][2]

    #Увеличение количества дней в словаре
    day_old = dict_of_users[chat_id][4]
    day_new = day_old + days
    

    #Увеличение количества дней в базе данных
    status = 'ACTIVE'
    database.update_status(chat_id, first_name, last_name, status, day_new)
    #Обновление словаря
    dict_of_users = database.create_dict_list_allinfo()

    

#Функция вычитания для из подписки
def minus_day():

    for el in dict_of_users:
        user_info_list = dict_of_users[el]
        #Если есть смысл вычитать день, то вычитаем день, и записываем
        if user_info_list[4] > 0:
            
            chat_id = user_info_list[0]
            name = user_info_list[1]
            last_name = user_info_list[2]
            status = user_info_list[3]

            user_info_list[4] = user_info_list[4]-1
            days = user_info_list[4]

            #Сначала отнимаем все дни в активном списке
            print(dict_of_users[el])
            dict_of_users[el] = user_info_list
            print(dict_of_users[el])
              

            #Потом перезаписываем количество дней в базе данных
            database.update_status(chat_id, name, last_name, status, days)

# Функция 3.1.0
async def status_follow():
    #Cистемные сообщения за 3, 1 и 0 дней подписки
        #Если 0 дней подписки, то Удяляем из чата
    global dict_of_users
    print("Enter")
    for el in dict_of_users:
        user_info_list = dict_of_users[el]
        chat_id = user_info_list[0]
        name = user_info_list[1]

        # Если 3, 1 или ноль дней до подписки
        if user_info_list[4] == 3:
            #keyboard_follow = keyboards.keyboard_follow()
            if user_info_list[3] =='ACTIVE':
                await bot.send_message(chat_id, f"{three_days}") 
                
            #send_message(chat_id)
            print("Three_days")
            
            pass
        
        elif user_info_list[4] == 1:
            #keyboard_follow = keyboards.keyboard_follow()
            if user_info_list[3] == 'ACTIVE':
                await bot.send_message(chat_id, f"{one_day}")
            pass
        
        elif user_info_list[4] == 0:

        
            if user_info_list[3] == 'ACTIVE':
                #Отправляем сообщение, что пока, друг.
                    #Изменение статуса в БД
                await bot.send_message(chat_id, f"{zero_days}")
                last_name = user_info_list[2]
                database.update_status(chat_id, name, last_name, 'END', 0)
                    #Изменение статуса в словаре(загрузка словаря)
                dict_of_users = database.create_dict_list_allinfo()

                
                #Баним и удаляем пользователя из приватного чата.
                await bot.ban_chat_member(private_channel_id, chat_id)
                await bot.unban_chat_member(private_channel_id, chat_id)
                #СИСТЕМНОЕ СООБЩЕНИЕ
                text = (f"У пользователя:\n"
                        f"ID: {chat_id}\n"
                        f"Имя: {name}\n"
                        f"Фамилия: {user_info_list[2]}\n"
                        f"Закончилась подписка!\n"
                        f"Пользователь УДАЛЕН из канала\n")
                await system_message_admin(text)
                #
            elif user_info_list[3] == 'END':
                pass
            elif user_info_list[3] == 'NEW':
                pass
            
            #!!! Изменение статусов на END, если не NEW

            
            pass


#Функция отправки системных сообщений админ листу
async def system_message_admin(text):
    for el in admin_list:
        await bot.send_message(el, text)
        

#----------------------------------Потоковая ассинхронность

async def every_day_check():
    while True:
            #Тестовая проверка статуса из потока

        
            await asyncio.sleep(45)
        
            a = time_check.time_check(check_time)
            if a == True:
                minus_day()
                await status_follow()
                await asyncio.sleep(85200)#задержка на 23.6 часов
                pass
            else:
                pass    

async def start_async(x):
    asyncio.create_task(every_day_check())

#------------------------------------------------------СТАРТ

if __name__ == '__main__':
        
    #Загрузка словаря с пользователями
    dict_of_users = database.create_dict_list_allinfo()
    
    executor.start_polling(dp, skip_updates=True, on_startup=start_async)

    """
    q = 0
    
    for key in dict_of_users.keys():
        q = q+1
        print(f"{q}. {dict_of_users[key]}")
    """

