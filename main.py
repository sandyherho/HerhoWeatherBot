from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from weather import get_forecasts

# pengecekan pesan bay --> polling
updater = Updater(token="621603636:AAEVtXeRzaOqH8fhvlZypmhWjj9_GPXP_cU")

# mengijinkan registrasu handler -> command, text, video, audio etc
dispatcher = updater.dispatcher


# mendefinisikan callback function

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hai, Selamat datang di HerhoWeatherBot! \n Kirimkan perintah /info untuk mengetahui info cuaca terkini di wilayah anda!")


# membuat perintah handler
start_handler = CommandHandler("start", start)

# menambahkan perintah handler ke dispatcher
dispatcher.add_handler(start_handler)

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text.upper())

# membuat text handler
echo_handler = MessageHandler(Filters.text, echo)

dispatcher.add_handler(echo_handler)

def option(bot, update):
    button = [
        [InlineKeyboardButton("Pilihan 1", callback_data="1"),
         InlineKeyboardButton("Pilihan 2", callback_data="2")],
        [InlineKeyboardButton("Pilihan 3", callback_data="3")]
    ]
    reply_markup = InlineKeyboardMarkup(button)

    bot.send_message(chat_id=update.message.chat_id,
                     text="Pilih salah satu...",
                     reply_markup=reply_markup)


option_handler = CommandHandler("pilihan", option)
dispatcher.add_handler(option_handler)


def get_location(bot, update):
    button = [
        [KeyboardButton("Bagikan lokasi", request_location=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(button)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Apakah anda keberatan membagikan lokasi anda saat ini?",
                     reply_markup=reply_markup)


get_location_handler = CommandHandler("info", get_location)
dispatcher.add_handler(get_location_handler)


def location(bot, update):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    forecasts = get_forecasts(lat, lon)
    bot.send_message(chat_id=update.message.chat_id,
                     text=forecasts,
                     reply_markup=ReplyKeyboardRemove())


location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler)

# memulai polling
updater.start_polling()
