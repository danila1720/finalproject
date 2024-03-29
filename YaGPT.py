import requests
from config import URL, FOLDER_ID, GPT_MODEL, CONTINUE_STORY, END_STORY, SYSTEM_PROMPT, HEADER, MAX_TOKENS, TEMPERATURE
import database as db
from config import TOKEN
from telebot import TeleBot

bot = TeleBot(TOKEN)


def ask_gpt(collection, user_id):
    headers = HEADER
    data = {"modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
            "completionOptions": {"stream": False, "temperature": TEMPERATURE, "maxTokens": MAX_TOKENS}, "messages": []}

    for row in collection:
        content = row['content']

        if db.get_data_for_user(user_id=user_id)['mode'] == 'continue' and row['role'] == 'user':
            content += "\n" + CONTINUE_STORY
        elif db.get_data_for_user(user_id=user_id)['mode'] == 'end' and row['role'] == 'user':
            content += "\n" + END_STORY

        data["messages"].append({"role": row["role"], "text": content})

    try:
        response = requests.post(URL, headers=headers, json=data)
        if db.get_data_for_user(user_id)['debug'] == 'Да':
            bot.send_message(user_id, f"{response.status_code}")

        if response.status_code != 200:
            result = f"Status code {response.status_code}"
            return result
        result = response.json()['result']['alternatives'][0]['message']['text']
    except Exception as e:
        result = "Произошла непредвиденная ошибка. Подробности см. в журнале."
    return result


def create_system_prompt(user_id):
    prompt = SYSTEM_PROMPT
    prompt += f"Напиши начало истории в жанре: {db.get_data_for_user(user_id=user_id)['genre']}."
    prompt += f"Главным героем этой истории будет: {db.get_data_for_user(user_id=user_id)['person']}."
    prompt += f"Вот где начинается эта история:{db.get_data_for_user(user_id=user_id)['environment']}."
    return prompt
