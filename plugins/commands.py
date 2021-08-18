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
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
import signal
from utils import USERNAME, FFMPEG_PROCESSES, mp
from config import Config
import os
import sys
import subprocess
import asyncio
from signal import SIGINT
U=USERNAME
CHAT=Config.CHAT
msg=Config.msg
HOME_TEXT = "<b>سڵآو, [{}](tg://user?id={})\n\nمن 24×7 بێ وەستانی ڕادیۆ/مۆسیقاژەنم.\n\nلێدان /helpبۆ وردەکاری زیاتر...</b>"
HELP = """
**User Commands:**
▷/play **[song name]/[yt link]**: Reply to an audio file.
▷/dplay **[song name]:** Play music from Deezer.
▷/player:  Show current playing song.
▷/help: Show help for commands.
▷/playlist: Shows the playlist.

**Admin Commands:**
▷/skip **[n]** ...  Skip current or n where n >= 2
▷/join: Join voice chat.
▷/leave: Leave current voice chat
▷/vc: Check which VC is joined.
▷/stop: Stop playing.
▷/radio: Start Radio.
▷/stopradio: Stops Radio Stream.
▷/replay: Play from the beginning.
▷/clean: Remove unused RAW PCM files.
▷/pause: Pause playing.
▷/resume: Resume playing.
▷/volume: Change volume(0-200).
▷/mute: Mute in VC.
▷/unmute: Unmute in VC.
▷/restart: Restarts the Bot.
"""



@Client.on_message(filters.command(['start', f'start@{U}']))
async def start(client, message):
    buttons = [
        [
        InlineKeyboardButton("🔥 Source Code 🔥", url='https://github.com/bnyaminali/vcplay'),
    ],
    [
        InlineKeyboardButton('👥 Group', url='https://t.me/iZaute/5'),
        InlineKeyboardButton('Channel 📢', url='https://t.me/iZaute/6'),
    ],
    [
        InlineKeyboardButton('🆘 Help & Commands 🆘', callback_data='help'),

    ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await message.delete()



@Client.on_message(filters.command(["help", f"help@{U}"]))
async def show_help(client, message):
    buttons = [
        [
            InlineKeyboardButton("🔥 Source Code 🔥", url='https://github.com/bnyaminali/vcplay'),
        ],
        [
            InlineKeyboardButton('👥 Group', url='https://t.me/iZaute/5'),
            InlineKeyboardButton('Channel 📢', url='https://t.me/iZaute/6'),
        ],
        [
            InlineKeyboardButton('🔰 How to Deploy 🔰', url='https://t.me/c/1481808444/131'),
        
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        HELP,
        reply_markup=reply_markup
        )
    await message.delete()
@Client.on_message(filters.command(["restart", f"restart@{U}"]) & filters.user(Config.ADMINS))
async def restart(client, message):
    await message.reply_text("🔄 Restarting...")
    await message.delete()
    process = FFMPEG_PROCESSES.get(CHAT)
    if process:
        try:
            process.send_signal(SIGINT)
        except subprocess.TimeoutExpired:
            process.kill()
    os.execl(sys.executable, sys.executable, *sys.argv)

