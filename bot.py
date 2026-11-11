import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, """Доступные команды:  - `/start` - начать работу с ботом и получить приветственное сообщение. \n
    - `/help` - получить список доступных команд.\n
    - `/show_city <city_name>` - отобразить указанный город на карте.\n
    - `/remember_city <city_name>` - сохранить город в список избранных.\n
    - `/show_my_cities` - показать все сохраненные города.")\n
        # Допиши команды бота \n """)


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split()[-1]
    user_id = message.chat.id
    manager.create_grapf(f"{user_id}.png", [city_name])
    with open(f"{user_id}.png", 'rb') as image:
        bot.send_photo(message.chat.id, image)

@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    cities = manager.select_cities(message.chat.id)
    user_id = message.chat.id
    manager.create_grapf(f"{user_id}.png", cities)
    with open(f"{user_id}.png", 'rb') as image:
        bot.send_photo(message.chat.id, image)

@bot.message_handler(commands=['draw_distance'])
def draw_distance(message):
    user_id = message.chat.id
    cities = manager.select_cities(user_id)
    city1, city2 = cities[:2]
    manager.draw_distance(f"{user_id}.png", city1, city2)
    with open(f"{user_id}.png", 'rb') as image:
        bot.send_photo(message.chat.id, image)

if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
