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
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import mp, RADIO, USERNAME
from config import Config
from config import STREAM
CHAT=Config.CHAT
ADMINS=Config.ADMINS

@Client.on_message(filters.command(["radio", f"radio@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT) | filters.private))
async def radio(client, message: Message):
    if 1 in RADIO:
        k=await message.reply_text("Kindly stop existing Radio Stream /stopradio")
        await mp.delete(k)
        await mp.delete(message)
        return
    await mp.start_radio()
    k=await message.reply_text(f"رادیۆ دەستی پێکرد: <code>{STREAM}</code>")
    await mp.delete(k)
    await mp.delete(message)

@Client.on_message(filters.command(['رەگرتنی رادیۆ', f"stopradio@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT) | filters.private))
async def stop(_, message: Message):
    if 0 in RADIO:
        k=await message.reply_text("Kindly start Radio First /radio")
        await mp.delete(k)
        await mp.delete(message)
        return
    await mp.stop_radio()
    k=await message.reply_text("پەخشی رادیۆ کۆتای هات.")
    await mp.delete(k)
    await mp.delete(message)
