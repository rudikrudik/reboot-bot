from telebot.async_telebot import AsyncTeleBot
from logger import logger
from kasse import admin_list


async def admin_notify(bot: AsyncTeleBot, message: str) -> None:
    for id_user, name in admin_list:
        try:
            await bot.send_message(id_user, message)
        except BaseException as error:
            await logger(f"Error {error}")
