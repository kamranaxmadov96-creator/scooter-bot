import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = "7983640437:AAFiMA0Qsu799KlxQGHqUDc7ybjRpvs5Des"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Бот работает! 🚀")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
