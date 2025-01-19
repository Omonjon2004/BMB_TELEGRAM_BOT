import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand

TOKEN ="8032664939:AAFkHCPf091X-nWi8ytkZcDGnIkjl0ER9m4"
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.bot.set_my_commands([
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="help", description="Yordam olish")
    ])
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")




@dp.message(Command(commands="help",prefix='/'))
async def help_handler(message: Message) -> None:
    await message.answer("Yordam kerak bo'lsa tayyorman ")

@dp.message()
async def echo_handler(message: Message) -> None:
    await message.copy_to(chat_id=message.from_user.id)

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())