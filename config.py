IAM_TOKEN = "t1.9euelZqLx8-Xy8yLlZaYl8rOlsqRlO3rnpWak5CajcaXmJCVjIqejomXlcvl9PdGCmVP-e8MM3eA3fT3BjliT_nvDDN3gM3n9euelZrPjYvOzI2MlMuZnZDOzJnJye_8xeuelZrPjYvOzI2MlMuZnZDOzJnJyb3rnpWanY6NncaWzpuUjMeJl4qczJq13oac0ZyQko-Ki5rRi5nSnJCSj4qLmtKSmouem56LntKMng.X2wgT1KTNJ5FO2mBKVZCN_eBluNmZltQoE8YKBqTaBqXDDnUF9mMqAbTanm4pQRL_Xxk_ZX0BgFeIn8CVcZgDw"
FOLDER_ID = 'b1g0ekt4tgcnufeo84p3'
GPT_MODEL = 'yandexgpt-lite'
TEMPERATURE = 0.6
MAX_TOKENS = 40

CONTINUE_STORY = 'Продолжи сюжет в 1-3 предложения и оставь интригу. Не пиши никакой пояснительный текст от себя'
END_STORY = 'Напиши завершение истории c неожиданной развязкой. Не пиши никакой пояснительный текст от себя'

SYSTEM_PROMPT = ('Ты пишешь историю с пользователем. От пользователя ты получаешь:'
                 ' Имя главного персонажа, Жанр и место действия'
                 'Если добавляешь диалоги начинай их с новой строки и отделяй знаком тире'
                 'не пиши пояснительного текста')
HEADER = {'Authorization': f'Bearer {IAM_TOKEN}', 'Content-type': 'application/json'}
MAX_SESSIONS = 4
TOKEN = "6569851786:AAEX6BpoCrlguxu4T1CgForFdWc_1veMi90"
DB_NAME = 'bot.sqlite'
DB_TABLE_USERS_NAME = "users"
LOGS_PATH = "logs.log"
URL = f"https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
