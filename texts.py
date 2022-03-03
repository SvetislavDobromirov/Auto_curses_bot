import datetime
import time_check

def create_text_info(days, time):
    text = (f"Days left: {days}"
            f"Time set: {time}")
    return text


greeting_text = ("Добро пожаловать в пространство, которое изменит вашу жизнь.\n"
                "Ежедневная утренняя йога сделает тело гибким и здоровым, а день - особенным!\n"
                "Приятной практики.🙏"
                 )


offer_test_class_text = ("Если вы хотите получить пробное занятие завтра в 6:00, нажмите 'Пробное занятие'.\n"
                         "Предложение действует только сегодня.")

offer_follow_text =("Чтобы продолжить занятия "
                    "нажмите кнопку /follow или выберите пункт в меню, чтобы выбрать вариант подписки.\n\n"
                    "Чтобы узнать стоимость вариантов подписки нажмите /info , либо сразу перейдите к подписке /follow.\n")

schedule_text = ("Для оформления подписки, сначала определимся, сколько раз в неделю вам будет удобно заниматься.\n"

                "1. 'Три дня' - занятия во вторник, четверг и субботу.\n"
                "2. 'Пять дней' - занятия по будням.\n"
                "3. 'Каждый день' - ежедневные занятия.\n"
                )

def create_text_good_choose(days):
    if days == 3:
        n_d = "дня"
    else:
        n_d = "дней"
    text = (f"Заниматься {days} {n_d} в неделю - прекрасный выбор!\n"
            "Сейчас можно выбрать нужное количество занятий." )
    return text

price_part1_text = ("   Я прекрасно знаю, что заставить себя регулярно заниматься не так просто."
                    " Поэтому каждое занятие будет доступно в течении двух часов после установленного вами времени."
                    " Если вы не явитесь на занятие, оно сгорит. Таким образом это дисциплинирует вас.\n"
                    "Но для совсем ленивых кошечек и котиков есть возможность неограниченных заморозок занятий."
                    " В этом случае занятия сгорать не будут. Такие виды подписки помечены ❄." )

price_part2_text = ("Стоимость пакетов занятий:\n"
                    "5 занятий  - 1300 р  или  1500 р ❄ \n"
                    "30 занятий - 6900 р  или  7500 р ❄\n"
                    "90 занятий - 13500 р или 14900 р ❄\n"
                    "Стоимость актуальна до 01.06.2022.\n"
                    )
agreement_text = ("    Продолжая оплату, вы соглашаетесь на покупку выбранного курса. "
                "Занятия будут присылаться согласно выбранному расписанию и времени. "
                "Выбор времени занятия будет доступен после оплаты.\n"

                "Данный Бот подключен к платежной системе ЮKassa. После перехода по ссылке 'Перейти на страницу оплаты'"
                " вы перейдете на сайт оплаты системы Юкасса. Все данные отправляются в зашифрованном виде и "
                "обрабатываются непосредственно платежной системой. Больше о безопасности платежей можно почитать тут"
                "→ (https://yookassa.ru/docs/support/security)\n"
                "Если вам необходимо будет отменить оплату, обратитесь к администратору в резделе /contacts "
                "или по кнопке в соответствующем пункте меню.")
set_time_text =("Выберете время в которое хотите получать занятия.\n"
                " Время можно изменить по ссылке /set_time или по кнопке в соответсвующем пунтке меню.")

def good_awaking_text(flag):
    if flag == "ACTIVE":
        min_text = "60 минут"
    elif flag == "NEW":
        min_text = "4 часа"
    else: print("ОШИБКА! textsA69")
        
    good_awaking = ("Приятного пробуждения!\n Перед занятием рекомендуется выпить стакан теплой воды.\n"
                    f"Занятие будет доступно {min_text}.")
    return good_awaking


info_about_try_text = ("Пробное занятие будет отправлено вам завтра в 6:00."
                       " Оно будет доступно в течении четырех часов. В 10:00 занятие будет удалено.")


def when_class_text(time, set_x):
    if "set3" in set_x:
        day_list = (1,3,5)
    elif "set5" in set_x:
        day_list = (0,1,2,3,4)
    elif "set7" in set_x:
        day_list = (0,1,2,3,4,5,6)
    else:
        day_list = ()
        day_num = 8

    
   
    day_today = datetime.datetime.today().weekday()

    if day_today in day_list:
        result = time_check.time_comparison(time)
        if result == "future":
            day_num = 7
        if result == "past":
            if day_today+1 in day_list:
                day_num = 8
            elif day_today == 6 or day_today == 4 or day_today == 5:
                day_num = 0
                
            elif "set3" in set_x:
                day_num = day_today+2
    else:
        day_num = 0  #### ощибка!!!
    
    if day_num == 0:
        day = "в понедельник"
    elif day_num == 1:
        day = "во вторник"
    elif day_num == 2:
        day = "в среду"
    elif day_num == 3:
        day = "в четверг"
    elif day_num == 4:
        day = "в пятницу"
    elif day_num == 5:
        day = "в субботу"
    elif day_num == 6:
        day = "в восскресенье"
    elif day_num == 7:
        day = "сегодня"
    elif day_num == 8:
        day = "завтра"
    
    text = f"Следующее занятие {day} в {time}."
    return text

def create_info_message(list_info):
    status = list_info[0]
    days = list_info[1]
    time = list_info[2] 
    set_x = list_info[3]
    if status == "ACTIVE":
        days_text = f"Занятий осталось {days}.\n\n"
    else: days_text = ""
    price = f"{price_part2_text}\n\n"
    if "set" in set_x or status == "TRY":
        next_class = f"{when_class_text(time, set_x)}\n\n"
    else: next_class = ""       
    table_menu = ("Команды для управления ботом, доступные в меню:\n"
                "/start - Начать\n"
                "/follow - Подписаться\n"
                "/set_time - Настроить время занятия\n"
                "/info - Информация\n"
                "/contacts - Контакты\n\n\n")


                  
    link_contacts = "Чтобы связаться с нами, нажмите /contacts или выберете соответствующий пункт в меню."
    text = f"{days_text}{next_class}{price}{table_menu}{link_contacts}"
    return text

contact_text = (
    
    "Главная йогиня:\n\n"
    "Харитинова Надежда\n"
    "тел. +7 903 790-84-23\n"
    "instagramm: \n"
    "Email:\n")
    
