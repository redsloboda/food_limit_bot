import telebot
from telebot import types

#1999997919:AAHzruS9TCWHTelSHnW1_G1qmwTjBXAQWdk

bot = telebot.TeleBot("1999997919:AAHzruS9TCWHTelSHnW1_G1qmwTjBXAQWdk", parse_mode=None)
weight = float(0)
height = float(0)
age = float(0)
index = float(0)
gender = ''
user_result = None


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Привет, тебе нужно ответить на пару вопросов, чтобы я помог тебе расчитать твой дневной калораж!\n\n'
                                      '➡️ Используй  /reg  для расчета суточной нормы калорий.\n\n'
                                      '➡️Используй /info , чтобы узнать больше о правильном питании.')


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Итак, сколько ты весишь?(кг)\n\n(это останется между нами)")
        bot.register_next_step_handler(message, reg_weight)
    elif message.text == '/info':
        bot.send_message(message.chat.id, '[Краткий курс о правльном: ](https://7spsy.com/blog/zdorovo-est-nauchim-pravilnomu-pishchevomu-povedeniyu/)', parse_mode='Markdown')
        bot.send_message(message.chat.id, '[Рацион правильного питания: ](https://miin.ru/blog/ratsion-pravilnogo-pitaniya//)', parse_mode='Markdown')
        bot.send_message(message.chat.id, '[Варианты меню: ](https://pohudejkina.ru/dieta-po-kaloriyam.html#varianty-menyu/)', parse_mode='Markdown')
        bot.send_message(message.chat.id, '[Приложение для расчета калорий продуктов: ](https://apps.apple.com/ru/app/calorie-counter-by-fatsecret/id347184248/)',parse_mode='Markdown')
    elif message.text == 'Привет':
        bot.reply_to(message, 'Привет , используй /reg или /info !')




def reg_weight(message):
    global weight
    while weight == 0:
        try:
            weight = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Вводите цифрами!")
    bot.send_message(message.from_user.id, "Какой у вас рост?(см)")
    bot.register_next_step_handler(message, reg_height)


def reg_height(message):
    global height
    while height == 0:
        try:
            height = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Вводите цифрами!")
    bot.send_message(message.from_user.id, "Сколько вам лет?")
    bot.register_next_step_handler(message, reg_age)


def reg_age(message):
    global age

    while age == 0:
        try:
            age = int(message.text)
        except Exception:
            bot.send_message(message.from_user.id, "Вводите цифрами!")
        bot.send_message(message.from_user.id, "Какой у вас уровень активности? Выберите пункт\n\n"
                                               "1️⃣ 1,2 – минимальная активность, сидячая работа, не требующая значительных физических нагрузок\n\n"
                                               "2️⃣ 1,375 – слабый уровень активности: интенсивные упражнения не менее 20 минут один-три раза в неделю\n\n"
                                               "3️⃣ 1,55 – умеренный уровень активности: интенсивная тренировка не менее 30-60 мин три-четыре раза в неделю\n\n"
                                               "4️⃣ 1,7 – тяжелая или трудоемкая активность: интенсивные упражнения и занятия спортом 5-7 дней в неделю. \n\n"
                                               "5️⃣ 1,9 – экстремальный уровень: включает чрезвычайно активные и/или очень энергозатратные виды деятельности: занятия спортом с почти ежедневным графиком и несколькими тренировками в течение дня; очень трудоемкая работа, например, сгребание угля или длительный рабочий день на сборочной линии.\n")
        bot.register_next_step_handler(message, reg_index)
        bot.send_message(message.from_user.id, "Выберите пункт цифрой(!) : ")

def reg_index(message):
    global index

    if int(message.text) == 1:
        index += 1.2
    elif int(message.text) == 2:
        index += 1.375
    elif int(message.text) == 3:
        index += 1.55
    elif int(message.text) == 4:
        index += 1.7
    elif int(message.text) == 5:
        index += 1.9
    bot.send_message(message.from_user.id, "Вы мужчина или женщина?")
    bot.register_next_step_handler(message, reg_gender)

def reg_gender(message):
    global gender
    gender = message.text



    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Ты - ' + gender + '\nТебе ' + str(age) + ' лет\nТвой рост: ' + str(height) + '\nТвой вес: ' + str(weight) + '\nТвой индекс: ' +str(index) + '?'
    bot.send_message(message.from_user.id, text = question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id,calculation())
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Попробуем еще раз!")


def calculation():
    global weight, height, index, gender, age, user_result

    if gender == 'мужчина' or 'Мужчина':
        user_result = int((10 * weight + 6.25 * height - 5 * age + 5) * index)
    elif gender == 'женщина' or 'Женщина':
        user_result = int((10 * weight + 6.25 * height - 5 * age - 161) * index)

    answer = 'Твоя дневная норма: ' + str(user_result) + '\n\nЕсли хочешь узнать больше о правильном питании - \nИспользуй /info'
    return answer





bot.polling()