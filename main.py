import telebot
from telebot import types
import keep_alive  # for replit uptime

# === CONFIGURATION ===
TOKEN = '8116660085:AAFirHpV_moSg7JONgPYQwfpdxJvcKOnoVA'
ADMIN_ID = 6114292071  # Replace with your admin ID
GROUP_ID = -1002789009352  # Replace with your group ID
AMOUNT = 99
QR_CODE_PATH = 'qr.png'

apps = {
    "PhonePe": "https://www.mediafire.com/ak/file",
    "GPay": "https://www.mediafire.com/ak/file",
    "Paytm": "https://www.mediafire.comak/file",
    "FamPay": "https://www.mediafire.com/PrinceAkramKhan.apk/file",
    "BHIM": "https://www.mediafire.com/ak/file"
}

user_choices = {}
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    for name in apps:
        markup.add(types.InlineKeyboardButton(name, callback_data=name))
    bot.send_message(message.chat.id, "🪙 Choose a payment method:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def payment_option(call):
    user_choices[call.from_user.id] = call.data
    with open(QR_CODE_PATH, 'rb') as photo:
        caption = f"💵 Send ₹{AMOUNT} to this UPI.\nThen send screenshot here."
        bot.send_photo(call.message.chat.id, photo, caption=caption)

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    bot.reply_to(message, "📩 Screenshot received. Wait for verification.")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.forward_message(GROUP_ID, message.chat.id, message.message_id)

@bot.message_handler(func=lambda m: m.reply_to_message and m.chat.id in [GROUP_ID, ADMIN_ID])
def handle_reply(message):
    original = message.reply_to_message
    user_id = original.forward_from.id if original.forward_from else None
    if not user_id:
        return
    if any(w in message.text.lower() for w in ['done', 'success', 'approved']):
        choice = user_choices.get(user_id, 'PhonePe')
        link = apps.get(choice, apps['PhonePe'])
        bot.send_message(user_id, f"✅ Payment approved. Download your app here:\n{link}")
    elif any(w in message.text.lower() for w in ['fail', 'rejected']):
        bot.send_message(user_id, "❌ Payment rejected. Try again.")

keep_alive.keep_alive()
print("🤖 Bot is running...")
bot.infinity_polling()
