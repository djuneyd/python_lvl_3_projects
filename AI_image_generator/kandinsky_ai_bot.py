from telebot import TeleBot
from telebot import types
from config import *
from logic import Text2ImageAPI

import base64
from PIL import Image
from io import BytesIO
import time

bot = TeleBot(TOKEN)

bot = TeleBot(TOKEN)
c1 = types.BotCommand(command='start', description='Start the Bot')
c2 = types.BotCommand(command='genim', description='Generate an image')
bot.set_my_commands([c1,c2])

@bot.message_handler(commands=['help', 'start'])
def start_command(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(0.5)
    bot.send_message(message.chat.id, '''I am a bot that generates images with the help of strong AI. To try my power on your own:
                     
/genim - after executing this command, enter your promt and wait.🧠
/help - if you need to remember my pupose.🙄''')

@bot.message_handler(commands=['genim'])
def generate_image(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(0.5)
    bot.send_message(message.chat.id, 'Send your promt:')
    bot.register_next_step_handler(message, generation_with_promt) # connecting to next step (capturing users message content)

def generation_with_promt(message):
    global api
    promt_text = message.text
    user_id = message.chat.id

    bot.send_chat_action(message.chat.id, 'typing') # typing animation
    time.sleep(0.5)
    bot.send_message(message.chat.id, 'Generating an image...')  # informing user about generation process
    bot.send_chat_action(message.chat.id, 'typing') # typing animation
    # connecting to ai and generating
    model_id = api.get_model()
    uuid = api.generate(promt_text, model_id)
    images = api.check_generation(uuid)[0]
    base64_string = images  # здесь должна быть ваша строка Base64
    # decoging image
    decoded_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(decoded_data))
    # sending to user
    # WE DONT SAVE IMAGE ON PC, WE JUST KEEP IT IN VARIABLE
    bot.delete_message(message.chat.id, message.message_id+1) # deleting message "generating image..."
    bot.send_photo(user_id, image)



if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', AI_KEY_1, AI_KEY_2) # we should write all actions above infinity polling because it enters infinite cycle
    bot.infinity_polling()