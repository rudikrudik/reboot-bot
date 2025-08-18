import asyncio
import json
import os

from reboot_pos_linux import linux_pos
from reboot_pos_windows import windows_pos
from telebot.async_telebot import AsyncTeleBot, types
from kasse import pos_dict, accept_dict
from ping import ping
from pos_status import ping_status, reboot_status, pos_program_status
from logger import logger
from admin_notification import admin_notify
from kasse import chat_dict


bot = AsyncTeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
async def pos_reboot(message):
    if message.chat.id in accept_dict:
        log_message = f"Пользователь {accept_dict[message.chat.id]} написал: '{message.text}'"
        await logger(log_message)
        await admin_notify(bot, log_message)

        try:
            pos = int(message.text.replace("/", ""))
            if pos in pos_dict:
                system, ip = pos_dict[pos]
                await bot.reply_to(message, f"Проверка кассы {pos} на доступность для перезагрузки")
                response_pos = await ping(ip)
                if response_pos:
                    keyboard = types.InlineKeyboardMarkup()
                    reboot_cd = json.dumps({"action": "reboot", "value": pos})
                    cancel_cd = json.dumps({"action": "cancel", "value": pos})
                    btn_reboot = types.InlineKeyboardButton(text="Перезагрузить",
                                                            callback_data=reboot_cd)
                    btn_cancel = types.InlineKeyboardButton(text="Отменить",
                                                            callback_data=cancel_cd)
                    keyboard.add(btn_reboot, btn_cancel)

                    await bot.reply_to(message, f"Касса {pos} доступна для перезагрузки, перезагрузить?",
                                       reply_markup=keyboard)
                else:
                    await bot.reply_to(message, f"Касса {pos} не доступна для перезагрузки")
            else:
                await bot.reply_to(message, f"Кассы с номером {pos} нет в системе")

        except ValueError as error:
            await bot.reply_to(message, "Проверьте правильность написания номера кассы")
            await logger(str(error))
    else:
        log_message = f"Не авторизованный пользователь {message.chat.id} написал '{message.text}'"
        await logger(log_message)
        await admin_notify(bot, log_message)


# Reboot
@bot.callback_query_handler(func=lambda call: json.loads(call.data).get("action") == "reboot")
async def reboot_action(call):
    system, ip = pos_dict[json.loads(call.data).get("value")]
    pos = json.loads(call.data).get("value")
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    log_message = f'Перезагружаем кассу №{pos}'

    await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                text=log_message)
    await logger(log_message)
    await admin_notify(bot, log_message)

    if system == "linux":
        await linux_pos(ip, "/usr/bin/sudo /sbin/reboot")

        if await ping_status(ip, 200):
            log_message = f"Статус перезагрузки: касса {pos} Перезагружается"
            await logger(log_message)
            await admin_notify(bot, log_message)
            await bot.reply_to(message, log_message)

            await asyncio.sleep(1)
            result_reboot = await reply_reboot(bot, message, ip, pos, 100)
            if result_reboot:
                await asyncio.sleep(60)
                await reply_start(bot, message, ip, pos, 100, "linux")
        else:
            log_message = f"Ошибка. Касса {pos} не перезагружена."
            await bot.reply_to(message, log_message)
            await logger(log_message)
            await admin_notify(bot, log_message)

    if system == "windows":
        await windows_pos(ip, "shutdown", "/r /f /t 5")

        if await ping_status(ip, 200):
            log_message = f"Статус перезагрузки: касса {pos} Перезагружается"
            await logger(log_message)
            await admin_notify(bot, log_message)
            await bot.reply_to(message, log_message)

            await asyncio.sleep(1)
            result_reboot = await reply_reboot(bot, message, ip, pos, 100)
            if result_reboot:
                await asyncio.sleep(120)
                await reply_start(bot, message, ip, pos, 100, "windows")
        else:
            log_message = f"Ошибка. Касса {pos} не перезагружена."
            await bot.reply_to(message, log_message)
            await logger(log_message)
            await admin_notify(bot, log_message)


# Cancel
@bot.callback_query_handler(func=lambda call: json.loads(call.data).get("action") == 'cancel')
async def cansel_action(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                text='Отмена действия')


async def reply_reboot(bot_reply: AsyncTeleBot, message, ip_host, pos_number, count) -> bool:
    if await reboot_status(ip_host, count):
        log_message = f"Касса {pos_number} перезагружена. Загружается кассовая программа"
        flag = True

    else:
        log_message = f"Ошибка, касса №{pos_number} не загрузилась"
        flag = False

    await bot_reply.reply_to(message, log_message)
    await logger(log_message)
    await admin_notify(bot, log_message)

    return flag


async def reply_start(bot_reply: AsyncTeleBot, message, ip_host, pos_number, count, system) -> None:
    if await pos_program_status(ip_host, count, system):
        log_message = f"Кассовая программа на кассе №{pos_number} загружена. Проверьте работу"

    else:
        log_message = f"Ошибка, кассовая программа на кассе №{pos_number} не загружена"

    await bot_reply.reply_to(chat_dict["work_chat"], log_message)
    await bot_reply.reply_to(message, log_message)
    await logger(log_message)
    await admin_notify(bot, log_message)


async def main():
    await logger(f"Start program on {os.getenv('STAGE')}")
    await bot.infinity_polling()


if __name__ == '__main__':
    asyncio.run(main())
