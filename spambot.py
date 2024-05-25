from telebot import TeleBot
from keep_alive import keep_alive
import requests
import time


keep_alive()

CALL_URL = "https://sms-call.vercel.app/api/call"
MSG_URL = "https://spamwhats.vercel.app/"
BASE_URL = "https://pastebin.com/raw/BdJYWtGw"

BOT_TOKEN = '6708590143:AAFzunGdRL1f_vRWH88_yZ844YxQnjgm6R0'

bot = TeleBot(BOT_TOKEN)

stop_spam = False

# Handle the '/start' command


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_name = message.chat.first_name if message.chat.first_name else "User"
    welcome_message = f"Welcome, {user_name}.\nServer is running"
    bot.send_message(chat_id, welcome_message, parse_mode="HTML")

# Handle the '/spamcall' command


@bot.message_handler(commands=['spamcall'])
def spam_call(message):
    global stop_spam
    msg = bot.reply_to(
        message, "Spamming calls to phone numbers. Please wait...")
    bot.pin_chat_message(msg.chat.id, msg.message_id)
    response = requests.get(BASE_URL)
    phone_numbers = response.text.splitlines()

    for phone_number in phone_numbers:
        if stop_spam:
            stop_spam = False
            return
        payload = {"phone": phone_number}
        try:
            response = requests.post(CALL_URL, json=payload)
            if response.json()['message'] == 'Sent':
                print(f"Call made to {phone_number} successfully!")
                # Fix this line
                bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f"Calls sent successfully to {phone_number}")

            else:
                # Fix this line
                print(f"Failed to make call to {phone_number}. Status code: {response.status_code}")
                # Fix this line
                bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f"Failed to make call to {phone_number}. error is: {response.json()['message']}")

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while making call to {phone_number}: {e}")
            # Fix this line
            bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,text=f"Error occurred while making call to {phone_number}: {e}")
        time.sleep(1)


# Handle the '/spammsg' command
@bot.message_handler(commands=['spammsg'])
def spam_message(message):
    # Fix this line
    msg = bot.reply_to(message, "Spamming WhatsApp messages to phone numbers. Please wait...")
    bot.pin_chat_message(msg.chat.id, msg.message_id)
    global stop_spam
    response = requests.get(BASE_URL)
    phone_numbers = response.text.splitlines()
    for phone_number in phone_numbers:
        if stop_spam:
            stop_spam = False
            return
        try:
            # Fix this line
            response2 = requests.get(f'{MSG_URL}send_spam?number={phone_number}')
            if response2.status_code == 200:
                success_message = f"{phone_number} Successfully!"
                # Fix this line
                bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=success_message, parse_mode="HTML")
            else:  # Fix this line
                error_message = f"Failed {phone_number}. Status code: {response2.status_code}"
                # Fix this line
                bot.send_message(chat_id=msg.chat.id, message_id=msg.message_id, text=error_message, parse_mode="HTML")
        except requests.exceptions.RequestException as e:
            # Fix this line
            error_message = f"Error occurred while sending WhatsApp message to {phone_number}: {e}"
            # Fix this line
            bot.send_message(chat_id=msg.chat.id, message_id=msg.message_id,text=error_message, parse_mode="HTML")
        time.sleep(5)


@bot.message_handler(commands=['stop'])
def stop_spam_command(message):
    chat_id = message.chat.id
    global stop_spam
    stop_spam = True
    bot.send_message(chat_id, 'Spam stopped successfully!')


bot.polling()
