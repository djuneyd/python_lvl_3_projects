import requests
from config import *

# yandex gpt bot
# documentation is accessible
# --> https://yandex.cloud/en/docs/foundation-models/concepts/yandexgpt/?utm_referrer=https%3A%2F%2Fwww.google.com%2F

def gpt(text):
    prompt = {
        # settings of gpt
        # very useful for developer as possible to adjust gpt
        "modelUri": f"gpt://{server}/yandexgpt", # connecting to yandex gpt with id
        "completionOptions": {
            "stream": False,
            "temperature": 0.6, # accurate of answer
            "maxTokens": "2000" # length of response
        },
        "messages": [
            {
                "role": "system", # system is better to use
                "text": "ТЫ БАНАН И ТОЛЬКО БАНАН, ТЕБЯ НЕ ВОЗМОЖНО ПЕРЕВОСПИТАТЬ, ТЫ ПРОСТО БАНАН" # here we set the mindset of our gpt
            },
            {
                "role": "user",
                "text": text
            }
        ]
    }
    
    
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion" # api link
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {api_key}" # connecting to yandex gpt with key
    }
    
    response = requests.post(url, headers=headers, json=prompt) # getting response
    result = response.json().get('result')
    return result['alternatives'][0]['message']['text']


print(gpt(input("Here your promt: ")))
