import telebot
from strings import TOKEN
import logging
from ctransformers import AutoTokenizer, AutoModelForCausalLM
import requests

bot = telebot.TeleBot(TOKEN)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)


class GPT:
    def __init__(self, system_content=""):
        self.system_content = system_content
        self.URL = 'http://localhost:1234/v1/chat/completions'
        self.HEADERS = {"Content-Type": "application/json"}
        self.MAX_TOKENS = 300
        self.assistant_content = ""


    def count_tokens(self,prompt):
        model = AutoModelForCausalLM.from_pretrained("10jqk1/mistralai-hf-q8_0.gguf", hf=True)
        tokenizer = AutoTokenizer.from_pretrained(model)
        return len(tokenizer.encode(prompt))


    def process_resp(self, response, message) -> [bool, str]:
        if response.status_code < 200 or response.status_code >= 300:
            self.clear_history()
            return (False, bot.send_message(message.chat.id, f"Ошибка: {response.status_code}"),
                    logging.warning(f"ошибка: {response.status_code}"))

        try:
            full_response = response.json()
        except:
            self.clear_history()
            return (False, bot.send_message(message.chat.id, "Ошибка получения JSON"),
                    logging.warning(f"Ошибка получения JSON"))

        try :
            result = full_response['choices'][0]['message']['content']

        except:
            self.clear_history()
            return (False, bot.send_message(message.chat.id, f"Ошибка: {full_response}"),
                    logging.warning(f"Ошибка: {full_response}"))



        if result == "" or result is None:
            self.clear_history()
            return True, bot.send_message(message.chat.id, "Объяснение закончено.")

        self.save_history(result)
        return True, self.assistant_content

    def make_promt(self, user_request):
        json = {
            "messages": [
                {"role": "system", 'content': self.system_content},
                {"role": "user", "content": user_request},
                {"role": "assistant", "content": self.assistant_content}
            ],
            "temperature": 1.2,
            "max_tokens": self.MAX_TOKENS,
        }
        return json

    def send_request(self, json):
        resp = requests.post(url=self.URL, headers=self.HEADERS, json=json)
        return resp

    def save_history(self, content_response):
        self.assistant_content += content_response

    def clear_history(self):
        self.assistant_content = "Для того что бы приготовить это нам надо: "

