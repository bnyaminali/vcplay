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
لەگەڵ ئەم بەرنامەیەدا  ئەگەر نا، ببینە <https://snapchat.com/add/bnyaminali>
"""
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, emoji
from utils import mp
from config import Config
playlist=Config.playlist

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


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.from_user.id not in Config.ADMINS and query.data != "help":
        await query.answer(
            "Who the hell you are",
            show_alert=True
            )
        return
    else:
        await query.answer()
    if query.data == "وەڵامدانەوە":
        group_call = mp.group_call
        if not playlist:
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} لیست بەتاڵە"
        else:
            pl = f"{emoji.PLAY_BUTTON} **لیست**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**داواکراوە لە لایەن:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(
                f"{pl}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="وەڵامدانەوە"),
                            InlineKeyboardButton("⏯", callback_data="ڕاگرتن"),
                            InlineKeyboardButton("⏩", callback_data="پەرینەوە")
                            
                        ],
                    ]
                )
            )

    elif query.data == "pause":
        if not playlist:
            return
        else:
            mp.group_call.pause_playout()
            pl = f"{emoji.PLAY_BUTTON} **لیستی**پەخشکردن**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**داواکراوە لەلایەن:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} وەستا\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="وەڵامدانەوە"),
                            InlineKeyboardButton("⏯", callback_data="پەرەپێدان"),
                            InlineKeyboardButton("⏩", callback_data="پەرینەوە")
                            
                        ],
                    ]
                )
            )

    
    elif query.data == "پەرەپێدان":   
        if not playlist:
            return
        else:
            mp.group_call.resume_playout()
            pl = f"{emoji.PLAY_BUTTON} **لیستی**پەخشکردن****:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**داواکراوە لەلایەن:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} پەرەی پێدرا\n\n{pl}",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔄", callback_data="وەڵامدانەوە"),
                            InlineKeyboardButton("⏯", callback_data="وەستا\n\n"),
                            InlineKeyboardButton("⏩", callback_data="پەرینەوە")
                            
                        ],
                    ]
                )
            )

    elif query.data=="پەرینەوە":   
        if not playlist:
            return
        else:
            await mp.skip_current_playing()
            pl = f"{emoji.PLAY_BUTTON} **لیستی**پەخشکردن****:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**داواکراوەلەلایەن:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.edit_message_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} پەڕێندراوە\n\n{pl}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="وەڵامدانەوە"),
                        InlineKeyboardButton("⏯", callback_data="وەستان"),
                        InlineKeyboardButton("⏩", callback_data="پەرینەوە")
                            
                    ],
                ]
            )
        )
        except:
            pass
    elif query.data=="help":
        buttons = [
            [
                InlineKeyboardButton("🔥 Source Code 🔥", url='https://github.com/bnyaminali/vcplay'),
            ],
            [
               InlineKeyboardButton('👥 Group', url='https://t.me/xakchat'),
               InlineKeyboardButton('Channel 📢', url='https://t.me/mad_tk'),
            ],
            [
               InlineKeyboardButton('🔰 How to Deploy 🔰', url='https://t.me/mad_tk'),
        
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            HELP,
            reply_markup=reply_markup

        )

