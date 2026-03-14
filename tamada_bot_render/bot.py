import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os

BOT_TOKEN = "8700552070:AAHe9rDmJgydb9LrZoINKfVICyZef4FrJC0"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} запустил бота")
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("👤 Моя подписка", callback_data="subscription"),
        InlineKeyboardButton("🎁 Рефералы", callback_data="referral"),
        InlineKeyboardButton("ℹ️ Информация", callback_data="info"),
        InlineKeyboardButton("🆘 Поддержка", callback_data="support")
    )
    
    await message.answer(
        "🔹 <b>Tamada VPN</b>\n"
        "Ваш удобный VPN прямо в Telegram\n\n"
        "Добро пожаловать! Используйте кнопки ниже:",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@dp.callback_query_handler(lambda c: True)
async def process_callback(call: types.CallbackQuery):
    logger.info(f"Нажата кнопка: {call.data}")
    await call.answer()
    
    if call.data == "subscription":
        await call.message.edit_text(
            f"🔹 <b>Моя подписка</b>\n\n"
            f"👤 ID: {call.from_user.id}\n\n"
            f"<b>Статус:</b> ✅ Активна\n"
            f"<b>До конца:</b> 1 дн.\n"
            f"<b>Устройства:</b> 0/3",
            parse_mode='HTML'
        )
    elif call.data == "referral":
        ref_link = f"https://t.me/{(await call.bot.me).username}?start={call.from_user.id}"
        await call.message.edit_text(
            f"🔹 <b>Рефералы</b>\n\n"
            f"Ваша ссылка:\n<code>{ref_link}</code>",
            parse_mode='HTML'
        )
    elif call.data == "info":
        await call.message.edit_text(
            "🔹 <b>О Tamada VPN</b>\n\n"
            "✅ Безлимитный трафик\n"
            "✅ Высокая скорость\n"
            "✅ 3 устройства",
            parse_mode='HTML'
        )
    elif call.data == "support":
        await call.message.edit_text(
            "🔹 <b>Поддержка</b>\n\n"
            "По всем вопросам: @tamada_support",
            parse_mode='HTML'
        )
    
    # Кнопка назад
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("◀️ Назад", callback_data="back_to_main")
    )
    await call.message.edit_reply_markup(keyboard)

@dp.callback_query_handler(lambda c: c.data == "back_to_main")
async def back_to_main(call: types.CallbackQuery):
    await call.answer()
    await cmd_start(call.message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    executor.start_webhook(
        dispatcher=dp,
        webhook_path='/webhook',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=port
    )