import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

BOT_TOKEN = "8700552070:AAHe9rDmJgydb9LrZoINKfVICyZef4FrJC0"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Моя подписка", callback_data="subscription")],
        [InlineKeyboardButton(text="🎁 Рефералы", callback_data="referral")]
    ])
    
    await message.answer(
        "🔹 <b>Tamada VPN</b>\n\nДобро пожаловать!",
        reply_markup=keyboard
    )

async def on_startup():
    await bot.set_webhook(f"https://tamada-vpn-bot.onrender.com/webhook")

def main():
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))

if __name__ == "__main__":
    main()