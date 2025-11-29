import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Бот работает через webhook! 🚀")


async def webhook_handler(request: web.Request):
    try:
        data = await request.json()
        update = types.Update(**data)
        await dp.feed_update(bot, update)
    except Exception as e:
        print("WEBHOOK ERROR:", e)

    return web.Response(text="OK", status=200)


def create_app():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, webhook_handler)
    return app


app = create_app()


if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
