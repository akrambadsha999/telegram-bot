import os
import telebot
import qrcode
from io import BytesIO

BOT_TOKEN = os.getenv("BOT_TOKEN")
UPI_ID = "akrambadsha999@okhdfcbank"
DOWNLOAD_LINK = "https://jarmod.com"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_qr(message):
    upi_link = f"upi://pay?pa={UPI_ID}&pn=QRPayment&am=99&cu=INR"
    qr = qrcode.make(upi_link)
    bio = BytesIO()
    qr.save(bio, format='PNG')
    bio.seek(0)
    bot.send_photo(message.chat.id, bio, caption="""
📲 *Pay ₹99 using this QR Code*

After paying, reply with `Done` to get your download link.
""", parse_mode='Markdown')

@bot.message_handler(func=lambda msg: msg.text.lower() == "done")
def send_link(message):
    bot.send_message(message.chat.id, f"✅ Payment confirmed!\n🔗 Here is your link:\n{DOWNLOAD_LINK}")

bot.polling()
