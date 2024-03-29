from telebot import TeleBot, types
import database as db
import strings
from config import MAX_SESSIONS, TOKEN
from YaGPT import ask_gpt, create_system_prompt
bot = TeleBot(TOKEN)



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

    bot.send_message(message.chat.id, "Вот вам на выбор несколько персонажей", reply_markup=create_keyboard(
        ['Сэр Макс', "Сэр Мелифаро", "Леди Кекки Туотли", "Леди Меламори Блим"]))
    bot.register_next_step_handler(message, genre)


def genre(message):
    if db.is_value_in_table(strings.DB_TABLE_USERS_NAME, 'user_id', message.from_user.id):

        session = db.get_data_for_user(user_id=message.from_user.id)['session']
        if session >= MAX_SESSIONS:
            bot.send_message(message.chat.id, "Вы превисыли кол-во доступных сессий")
        db.update_row_value(user_id=message.from_user.id, column_name='session', new_value= 1+session)
        db.update_row_value(user_id=message.from_user.id, column_name='person', new_value=message.text)
    else:
        db.insert_row(values=(message.from_user.id, message.text, "Нет", "Нет", "continue", "Нет", 0, 'нет', 'нет'))
    bot.send_message(message.chat.id, "хорошо теперь выбор жанра",
                     reply_markup=create_keyboard(["Фантастика", "Детектив", "Комедия"]))
    bot.register_next_step_handler(message, environment)


def environment(message):
    print(db.get_data_for_user(message.from_user.id))
    db.update_row_value(user_id=message.from_user.id, column_name="genre", new_value=message.text)
    bot.send_message(message.chat.id, "А теперь выбор окружения",
                     reply_markup=create_keyboard(["Город Ехо", "Город Кеттари", "Трактир Середина Леса"]))
    bot.register_next_step_handler(message, generation)
def generation(message):
    user_id = message.from_user.id
    db.update_row_value(user_id=message.from_user.id, column_name="environment", new_value=message.text)
    bot.send_message(message.chat.id, "Хорошо теперь все готово для генерации сценария.Ожидайте")

    user_collection = {user_id: [{'role': 'system', 'content': create_system_prompt(user_id)}]}
    result = ask_gpt(user_collection[user_id], user_id)
    db.update_row_value(user_id, 'content', result)
    bot.send_message(user_id, result)

@bot.message_handler(commands=['continue'])
def prodolzhenie(message):
    user_id = message.from_user.id
    session = db.get_data_for_user(user_id=message.from_user.id)['session']
    if session >= MAX_SESSIONS:
        bot.send_message(message.chat.id, "Вы превисыли кол-во доступных сессий")
    db.update_row_value(user_id=message.from_user.id, column_name='session', new_value=1 + session)
    user_collection = {user_id: [{'role': 'system', 'content': create_system_prompt(user_id=message.from_user.id + db.get_data_for_user(user_id=message.from_user.id)['content'])}]}
    result = ask_gpt(user_collection[user_id], user_id)
    db.update_row_value(user_id, 'content', result)
    bot.send_message(user_id, result)

@bot.message_handler(commands=['end'])
def konets(message):
    user_id = message.from_user.id
    session = db.get_data_for_user(user_id=message.from_user_id)['session']
    if session >= MAX_SESSIONS:
        bot.send_message(message.chat.id, "Вы превисыли кол-во доступных сессий")
    db.update_row_value(user_id=message.from_user.id, column_name='session', new_value=1 + session)
    db.update_row_value(user_id, 'mode', 'end')
    user_collection = {user_id: [{'role': 'system', 'content': create_system_prompt(user_id=message.from_user.id + db.get_data_for_user(user_id=message.from_user.id)['content'])}]}
    result = ask_gpt(user_collection[user_id], user_id)
    db.update_row_value(user_id, 'content', result)
    bot.send_message(user_id, result)

@bot.message_handler(commands=['debug'])
def debug(message):
    bot.send_document(message.chat.id, 'logs.log')

@bot.message_handler(commands=['debug-mode'])
def debug_mode(message):
    db.update_row_value(message.chat.id, 'debug', 'Да')
    bot.send_message(message.chat.id, 'Поздравляю вы перешли в debug мод')




db.prepare_db(True)
bot.polling()
