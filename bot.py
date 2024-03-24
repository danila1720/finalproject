from telebot import TeleBot, types
import database as db
from gpt import GPT
import strings

gpt = GPT(system_content="")
bot = TeleBot(strings.TOKEN)


def create_keyboard(buttons_list):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, strings.COMMANDS['start'])


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, strings.COMMANDS['help'])


@bot.message_handler(commands=['genre'])
def character(message):
    if db.is_value_in_table(strings.DB_TABLE_USERS_NAME, 'user_id', message.from_user.id):
        db.delete_user(message.from_user.id)
    bot.send_message(message.chat.id, "Вот вам на выбор несколько персонажей", reply_markup=create_keyboard(
        ['Сэр Макс', "Сэр Мелифаро", "Сэр Джуффин Халли", "Леди Меламори Блим"]))
    bot.register_next_step_handler(message, genre)


def genre(message):
    db.insert_row(values=(message.chat.id, message.text, "нет", "нет", "нет"))
    bot.send_message(message.chat.id, "хорошо теперь выбор жанра",
                     reply_markup=create_keyboard(["Фантастика", "Детектив", "Комедия"]))
    bot.register_next_step_handler(message, environment)


def environment(message):
    db.update_row_value(user_id=message.from_user.id, column_name="genre", new_value=message.text)
    bot.send_message(message.chat.id, "А теперь выбор окружения",
                     reply_markup=create_keyboard(["Город Ехо", "Город Кеттари", "Трактир Середина Леса"]))
    bot.register_next_step_handler(message, generation)
def generation(message):
    db.update_row_value(user_id=message.from_user.id, column_name="environment", new_value=message.text)
    person = db.get_data_for_user(user_id=message.from_user.id)['person']
    okruzhenie = db.get_data_for_user(user_id=message.from_user.id)['environment']
    zhanr = db.get_data_for_user(user_id=message.from_user.id)['genre']
    bot.send_message(message.chat.id, "Хорошо теперь все готово для генерации сценария.Ожидайте")
    gpt.system_content = f"Ты пишешь сценарий о том что происходило с {person} в {okruzhenie}, в жанре {zhanr}, на русском языке"
    gpt.assistant_content = "Хорошо вот вам сценарий:"
    json = gpt.make_promt(user_request="напиши сценарий")
    resp = gpt.send_request(json)
    response = gpt.process_resp(message=message, response=resp)
    if not response[0]:
        bot.send_message(message.chat.id, "Не удалось выполнить запрос...")

    bot.send_message(message.chat.id, response[1])
    db.update_row_value(message.from_user.id,"script", response[1])

db.prepare_db(True)
bot.polling()