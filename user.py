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
from config import Config
from pyrogram import Client
from config import Config
REPLY_MESSAGE=Config.REPLY_MESSAGE
if REPLY_MESSAGE is not None:
    USER = Client(
        Config.SESSION,
        Config.API_ID,
        Config.API_HASH,
        plugins=dict(root="userplugins")
        )
else:
    USER = Client(
        Config.SESSION,
        Config.API_ID,
        Config.API_HASH
        )
USER.start()
