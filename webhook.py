import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Бот работает через webhook! 🚀")

async def webhook_handler(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response()

async def on_startup(app):
    webhook_url = os.getenv("WEBHOOK_URL")
    await bot.set_webhook(webhook_url)

def create_app():
    app = web.Application()
    app.router.add_post("/", webhook_handler)
    app.on_startup.append(on_startup)
    return app

# ⬇️ Обязательно! Gunicorn ищет ЭТО
app = create_app()
