import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

TOKEN = "7898891497:AAHe2velplZq73bfMtEaKReIZoAWlsL6Vgk"
ADMIN_ID = 5073544572
FREE_LIMIT = 3
user_queries = {}

logging.basicConfig(level=logging.INFO)

WELCOME_TEXT = """👋 Привет! Я OSINT-Бот.

🔍 Я могу:
📞 /phone +998901234567 — найти данные по номеру
📧 /email test@mail.com — проверить email
👤 /nick nickname — найти ник
🌐 /ip 8.8.8.8 — геолокация по IP
📲 /social +998... — соцсети по номеру
🧾 /whois domain.com — whois-домен

🔓 3 бесплатных запроса.
💸 За реальную информацию — купи доступ!"""

BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📞 Телефон", callback_data="phone")],
    [InlineKeyboardButton("📲 Соцсети", callback_data="social")],
    [InlineKeyboardButton("🌐 IP", callback_data="ip")],
    [InlineKeyboardButton("📧 Email", callback_data="email")],
    [InlineKeyboardButton("🧾 Whois", callback_data="whois")],
    [InlineKeyboardButton("💰 Купить доступ", url="https://t.me/s_ruslan01")]
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=BUTTONS)

def check_limit(user_id):
    if user_id not in user_queries:
        user_queries[user_id] = 1
        return True
    elif user_queries[user_id] < FREE_LIMIT:
        user_queries[user_id] += 1
        return True
    return False

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not check_limit(user_id):
        return await update.message.reply_text("🔒 Бесплатные запросы закончились. Купи доступ.")
    if not context.args:
        return await update.message.reply_text("📞 Введи номер, например: /phone +998901234567")
    number = context.args[0]
    if user_queries[user_id] <= FREE_LIMIT:
        fake_ip = f"192.168.{random.randint(0,255)}.{random.randint(0,255)}"
        fake_city = random.choice(["Tashkent", "Moscow", "Berlin", "Istanbul"])
        await update.message.reply_text(
            f"📞 Номер: {number}\n🌍 Примерный IP: {fake_ip}\n🏙️ Город: {fake_city}\n⚠️ Хочешь реальные данные? Купи доступ."
        )

async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📧 Утечек не найдено (в демо-режиме). За реальные данные купи доступ.")

async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("🌐 Введи IP адрес.")
    ip = context.args[0]
    await update.message.reply_text(f"🌐 IP: {ip}\n🏙️ Город: Ташкент\n🛰️ Провайдер: Uztelecom (демо)")

async def nick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👤 Поиск ника (заглушка). В полной версии покажем, где найден.")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 BTC: нет доступа к blockchain API (заглушка).")

async def whois(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧾 Whois: информация временно недоступна (заглушка).")

async def social(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📲 В демо-режиме не отображаются соцсети. Купи доступ для реального пробива.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("phone", phone))
app.add_handler(CommandHandler("email", email))
app.add_handler(CommandHandler("ip", ip))
app.add_handler(CommandHandler("nick", nick))
app.add_handler(CommandHandler("btc", btc))
app.add_handler(CommandHandler("whois", whois))
app.add_handler(CommandHandler("social", social))

print("✅ Бот запущен")
app.run_polling()
