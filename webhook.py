import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Webhook работает! 🚀")


# ------ Обработчик Telegram-update ------
async def telegram_update(request: web.Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response(text="ok")


# ------ Healthcheck ------
async def health(request: web.Request):
    return web.Response(text="OK")


# ------ Startup ------
async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)


# ------ Shutdown ------
async def on_shutdown(app: web.Application):
    await bot.delete_webhook()


# ------ Создание и запуск приложения ------
def create_app():
    app = web.Application()

    app.router.add_post("/", telegram_update)
    app.router.add_get("/", health)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == "__main__":
    web.run_app(
        create_app(),
        host="0.0.0.0",
        port=int(os.getenv("PORT", 10000))
    )
