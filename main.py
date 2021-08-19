"""
VC Music Player, Telegram Voice Chat Userbot
Copyright (C) 2021  BnyaminAli

ئەم بەرنامەیە سۆفتوێرێکی ئازادە: دەتوانیت دووبارە دابەشی بکەیتەوە و/یان هەمواری بکەیتەوە
ئەو بەپێی مەرجەکانیGNU Affero مۆڵەتی گشتی وەک بڵاو کراوەتەوە لەلایەن
دامەزراوەی سۆفتوێری ئازاد، یان ڤێرژنی 3 ی مۆڵەتەکە، یان
(لە بژاردەی خۆت)و هەر وەشانێکی دواتر.

ئەم بەرنامەیە بەهیوای ئەوەی سوودبەخش بێت دابەشدەکرێت
بەڵام بەبێ هیچ گەرەنتییەک بە بێ تەنانەت گەرەنتی تێلێکراوی
بازرگانێتی یان لەشجوانی بۆ مەبەستێکی تایبەت.  ببینە
مۆڵەتی گشتی گشتی گنو ئافەرۆ بۆ وردەکاری زیاتر.
پێویست بوو کۆپیەک لە مۆڵەتی گشتی گنو ئافەرۆت وەرگرتبا
لەگەڵ ئەم بەرنامەیەدا  ئەگەر نا، ببینە <https://www.gnu.org/licenses/>
"""
from pyrogram import Client, idle
import os
from config import Config
from utils import mp
from pyrogram.raw import functions, types

CHAT=Config.CHAT
bot = Client(
    "مۆسیقاژەن",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")
async def main():
    async with bot:
        await mp.start_radio()

bot.run(main())
bot.start()
bot.send(
    functions.bots.SetBotCommands(
        commands=[
            types.BotCommand(
                command="start",
                description="بپشکنە ئەگەر بۆتەکە زیندوو بێت"
            ),
            types.BotCommand(
                command="help",
                description="نامەی یارمەتی نیشان دەدات"
            ),
            types.BotCommand(
                command="play",
                description="گۆرانی لە youtube/audiofile پەخش بکە"
            ),
            types.BotCommand(
                command="dplay",
                description="گۆرانی لە دێزیرەوە پەخش بکە"
            ),
            types.BotCommand(
                command="player",
                description="پیشاندانی گۆرانی لێدراوی ئێستا لەگەڵ کۆنترۆڵەکان"
            ),
            types.BotCommand(
                command="playlist",
                description="لیستی پەخشکردنەکە پیشان دەدات"
            ),
            types.BotCommand(
                command="skip",
                description="لە گۆرانی ئێستا بپەڕە"
            ),
            types.BotCommand(
                command="join",
                description="داخڵی ڤۆیس چات بە"
            ),
            types.BotCommand(
                command="leave",
                description="ڤۆیس چات جێبێڵە"
            ),
            types.BotCommand(
                command="vc",
                description="پشکنینی داخڵ بوونی ڤۆیسچات"
            ),
            types.BotCommand(
                command="stop",
                description="وەستاندن"
            ),
            types.BotCommand(
                command="radio",
                description="دەستپێکردنی ڕادیۆ / لایڤ ستریم"
            ),
            types.BotCommand(
                command="stopradio",
                description="ڕاگرتنی ڕادیۆ / لایڤ ستریم"
            ),
            types.BotCommand(
                command="replay",
                description="دووبارە کردنەوە لە سەرەتاوە"
            ),
            types.BotCommand(
                command="clean",
                description="فایلەکانی RAW پاک دەکاتەوە"
            ),
            types.BotCommand(
                command="pause",
                description="وەستاندنی گۆرانیەکە"
            ),
            types.BotCommand(
                command="resume",
                description="دەستپێکردنەوەی گۆرانی ڕاوەستاو"
            ),
            types.BotCommand(
                command="mute",
                description="بەدەنگ بوون لە ڤۆیس"
            ),
            types.BotCommand(
                command="volume",
                description="دانانی قەبارەی دەنگ لە نێوان 0-200"
            ),
            types.BotCommand(
                command="unmute",
                description="لادانی بێدەنگی لە ڤۆیس"
            ),
            types.BotCommand(
                command="restart",
                description="دەستپێکردنەوەی بۆتەکە"
            )
        ]
    )
)

idle()
bot.stop()
