

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

yes_button = InlineKeyboardButton('Настроить время', callback_data='start_time_setting')
choose_set_time_keyboard = InlineKeyboardMarkup(row_width=2).add(yes_button)
choose_set_time_keyboard.add(InlineKeyboardButton('Время меня устраивает', callback_data='time_good'))
# = InlineKeyboardMarkup().add(yes_button)
#choose_set_time_keyboard = InlineKeyboardMarkup().add(right_time_button)


follow_button = InlineKeyboardButton("Хочу присоединиться!", callback_data = "want_follow")
follow_keyboard = InlineKeyboardMarkup().add(follow_button)


h50 = InlineKeyboardButton('5:00', callback_data='settime_5:00')
h51 = InlineKeyboardButton('5:15', callback_data='settime_5:15')
h52 = InlineKeyboardButton('5:30', callback_data='settime_5:30')
h53 = InlineKeyboardButton('5:45', callback_data='settime_5:45')
hours_keyboard = InlineKeyboardMarkup().row(h50,h51,h52,h53)
h60 = InlineKeyboardButton('6:00', callback_data='settime_6:00')
h61 = InlineKeyboardButton('6:15', callback_data='settime_6:15')
h62 = InlineKeyboardButton('6:30', callback_data='settime_6:30')
h63 = InlineKeyboardButton('6:45', callback_data='settime_6:45')
hours_keyboard = InlineKeyboardMarkup().row(h60,h61,h62,h63)
h70 = InlineKeyboardButton('7:00', callback_data='settime_7:00')
h71 = InlineKeyboardButton('7:15', callback_data='settime_7:15')
h72 = InlineKeyboardButton('7:30', callback_data='settime_7:30')
h73 = InlineKeyboardButton('7:45', callback_data='settime_7:45')
hours_keyboard = InlineKeyboardMarkup().row(h70,h71,h72,h73)
h80 = InlineKeyboardButton('8:00', callback_data='settime_8:00')
h81 = InlineKeyboardButton('8:15', callback_data='settime_8:15')
h82 = InlineKeyboardButton('8:30', callback_data='settime_8:30')
h83 = InlineKeyboardButton('8:45', callback_data='settime_8:45')
hours_keyboard = InlineKeyboardMarkup().row(h80,h81,h82,h83)
h90 = InlineKeyboardButton('9:00', callback_data='settime_9:00')
h91 = InlineKeyboardButton('9:15', callback_data='settime_9:15')
h92 = InlineKeyboardButton('9:30', callback_data='settime_9:30')
h93 = InlineKeyboardButton('9:45', callback_data='settime_9:45')
hours_keyboard = InlineKeyboardMarkup().row(h90,h91,h92,h93)
h100 = InlineKeyboardButton('10:00', callback_data='settime_10:00')

hours_keyboard = InlineKeyboardMarkup().add(h50,h51,h52,h53,h60,h61,h62,h63,h70,h71,h72,h73,h80,h81,h82,h83,h90,h91,h92,h93,h100)                                     


third_days_button = InlineKeyboardButton('3 дня', callback_data = "setmode_3")
five_days_button =  InlineKeyboardButton('5 дней', callback_data = "setmode_5")
every_days_button = InlineKeyboardButton('Каждый день', callback_data = "setmode_7")
set_mode_keyboard = InlineKeyboardMarkup().add(third_days_button, five_days_button, every_days_button)


to_pay = InlineKeyboardButton('Перейти к платежу', callback_data = "go_to_payment")
ready_to_pay_keyboard = InlineKeyboardMarkup().add(to_pay)

cl5 = InlineKeyboardButton('5 занятий', callback_data = "cl_5")
cl30=InlineKeyboardButton('30 занятий', callback_data = "cl_30")
cl90=InlineKeyboardButton('90 занятий', callback_data = "cl_90")
cl5_lite = InlineKeyboardButton('5 занятий❄', callback_data = "cll_5")
cl30_lite =InlineKeyboardButton('30 занятий❄', callback_data = "cll_30")
cl90_lite =InlineKeyboardButton('90 занятий❄', callback_data = "cll_90")
classes_keyboard= InlineKeyboardMarkup().add(cl5, cl30, cl90, cl5_lite, cl30_lite, cl90_lite)

start_button = InlineKeyboardButton("Приступить к занятию!", callback_data = "start")
start_keyboard= InlineKeyboardMarkup().add(start_button)

try_button = InlineKeyboardButton("Пробное занятие", callback_data = "try")
try_class_keyboard= InlineKeyboardMarkup().add(try_button)




