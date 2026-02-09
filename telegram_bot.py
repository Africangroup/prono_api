import pandas as pd
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8280231709:AAG_McGLnUJ0WQp0K5zMtNqMQP8Ia9smWRs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot Prono actif\n"
        "Commande : /signal"
    )

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    df = pd.read_csv("data/live_training.csv")
    row = df.tail(1)

    minute = int(row["minute"].values[0])
    proba = round(row["proba_goal"].values[0], 2)
    xg = round(row["xg_total"].values[0], 2)
    shots = int(row["shots_total"].values[0])

    message = (
        f"⚽ SIGNAL LIVE\n\n"
        f"⏱ Minute : {minute}\n"
        f"📊 Proba but : {proba}\n"
        f"📈 xG : {xg}\n"
        f"🎯 Tirs : {shots}\n"
    )

    if minute >= 60 and proba >= 0.60:
        message += "\n🔥 BET POSSIBLE"
    else:
        message += "\n⛔ PAS DE BET"

    await update.message.reply_text(message)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("🤖 Bot Telegram lancé")
    app.run_polling()

if __name__ == "__main__":
    main()
