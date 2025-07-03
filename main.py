import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = os.environ.get('TOKEN')
AUTHORIZED_USER_ID = int(os.environ.get('AUTHORIZED_USER_ID'))
CHANNEL_ID = os.environ.get('CHANNEL_ID')

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == AUTHORIZED_USER_ID:
        update.message.reply_text("Bot attivo. Usa /send con 4 numeri: entry1 entry2 stop tp")
    else:
        update.message.reply_text("Non sei autorizzato a usare questo bot.")

def send(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != AUTHORIZED_USER_ID:
        update.message.reply_text("Non sei autorizzato a usare questo comando.")
        return

    args = context.args
    if len(args) != 4:
        update.message.reply_text("Devi fornire 4 numeri: entry1 entry2 stop tp")
        return

    try:
        entry1 = round(float(args[0]), 1)
        entry2 = round(float(args[1]), 1)
        stop = round(float(args[2]), 1)
        tp = round(float(args[3]), 1)
    except ValueError:
        update.message.reply_text("Assicurati che tutti i valori siano numeri validi.")
        return

    if entry1 < entry2:
        direction = "BUY XAUUSD"
    elif entry1 > entry2:
        direction = "SELL XAUUSD"
    else:
        direction = "No trade (range neutro)"

    entry_range = f"{int(entry1)}-{int(entry2)}"

    message = (
        f"🚨 {direction} {entry_range} 🚨\n\n"
        f"🎯 TP {tp}\n\n"
        f"⛔ SL {stop}\n\n"
        f"‼️ Usa i lotti consigliati ‼️"
    )

    try:
        context.bot.send_message(chat_id=CHANNEL_ID, text=message)
        update.message.reply_text("Segnale inviato con successo!")
    except Exception as e:
        update.message.reply_text(f"Errore nell'invio: {e}")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("send", send))

    updater.start_polling()
    print("Bot avviato...")
    updater.idle()

if __name__ == "__main__":
    main()
