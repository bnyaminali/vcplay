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
import os
from youtube_dl import YoutubeDL
from config import Config
from pyrogram import Client, filters, emoji
from pyrogram.methods.messages.download_media import DEFAULT_DOWNLOAD_DIR
from pyrogram.types import Message
from utils import mp, RADIO, USERNAME, FFMPEG_PROCESSES
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch
from pyrogram import Client
from aiohttp import ClientSession
import signal
import re
U=USERNAME
LOG_GROUP=Config.LOG_GROUP
ADMIN_ONLY=Config.ADMIN_ONLY
DURATION_LIMIT = Config.DURATION_LIMIT
ARQ_API=Config.ARQ_API
session = ClientSession()
arq = ARQ("https://thearq.tech",ARQ_API,session)
playlist=Config.playlist
msg = Config.msg
ADMINS=Config.ADMINS
CHAT=Config.CHAT
LOG_GROUP=Config.LOG_GROUP
playlist=Config.playlist

import os
from youtube_dl import YoutubeDL
from config import Config
from pyrogram import Client, filters, emoji
from pyrogram.methods.messages.download_media import DEFAULT_DOWNLOAD_DIR
from pyrogram.types import Message
from utils import mp, RADIO, USERNAME, FFMPEG_PROCESSES
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch
from pyrogram import Client
from aiohttp import ClientSession
import subprocess
from signal import SIGINT
import re
U=USERNAME
EDIT_TITLE=Config.EDIT_TITLE
LOG_GROUP=Config.LOG_GROUP
ADMIN_ONLY=Config.ADMIN_ONLY
DURATION_LIMIT = Config.DURATION_LIMIT
ARQ_API=Config.ARQ_API
session = ClientSession()
arq = ARQ("https://thearq.tech",ARQ_API,session)
playlist=Config.playlist
msg = Config.msg
ADMINS=Config.ADMINS
CHAT=Config.CHAT
LOG_GROUP=Config.LOG_GROUP
playlist=Config.playlist

async def is_admin(_, client, message: Message):
    admins = await mp.get_admins(CHAT)
    if message.from_user is None and message.sender_chat:
        return True
    if message.from_user.id in admins:
        return True
    else:
        return False

admin_filter=filters.create(is_admin)   



@Client.on_message(filters.command(["play", f"play@{U}"]) & (filters.chat(CHAT) | filters.private) | filters.audio & filters.private)
async def yplay(_, message: Message):
    if ADMIN_ONLY == "Y":
        admins = await mp.get_admins(CHAT)
        if message.from_user.id not in admins:
            m=await message.reply_sticker("CAADBQAD7gIAAq-1OVf2ov3Ge_ngpxYE")
            await mp.delete(m)
            await mp.delete(message)
            return
    type=""
    yturl=""
    ysearch=""
    if message.audio:
        type="audio"
        m_audio = message
    elif message.reply_to_message and message.reply_to_message.audio:
        type="audio"
        m_audio = message.reply_to_message
    else:
        if message.reply_to_message:
            link=message.reply_to_message.text
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex,link)
            if match:
                type="youtube"
                yturl=link
        elif " " in message.text:
            text = message.text.split(" ", 1)
            query = text[1]
            regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
            match = re.match(regex,query)
            if match:
                type="youtube"
                yturl=query
            else:
                type="query"
                ysearch=query
        else:
            d=await message.reply_text("تۆ هیچت پێنەداوم تا بیژەنم بکەم. فایلێکی دەنگیم بۆ بنێرە یان وەڵامم بدەرەوە /play بۆ فایلێکی دەنگی.")
            await mp.delete(d)
            await mp.delete(message)
            return
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    group_call = mp.group_call
    if type=="audio":
        if round(m_audio.audio.duration / 60) > DURATION_LIMIT:
            d=await message.reply_text(f"❌ دەنگ درێژترە لە {DURATION_LIMIT} خولەک(ەکان) ڕێ پێنەدراوە، دەنگی دابینکراو بریتیە لە {round(m_audio.audio.duration/60)} خولەک(s)")
            await mp.delete(d)
            await mp.delete(message)
            return
        if playlist and playlist[-1][2] \
                == m_audio.audio.file_id:
            d=await message.reply_text(f"{emoji.ROBOT} پێشتر زیادکرا لە لیستی پەخشکردن")
            await mp.delete(d)
            await mp.delete(message)
            return
        data={1:m_audio.audio.title, 2:m_audio.audio.file_id, 3:"تیلیگرام", 4:user}
        playlist.append(data)
        if len(playlist) == 1:
            m_status = await message.reply_text(
                f"{emoji.INBOX_TRAY} داگرتن و پرۆسە..."
            )
            await mp.download_audio(playlist[0])
            if 1 in RADIO:
                if group_call:
                    group_call.input_filename = ''
                    RADIO.remove(1)
                    RADIO.add(0)
                process = FFMPEG_PROCESSES.get(CHAT)
                if process:
                    try:
                        process.send_signal(SIGINT)
                    except subprocess.TimeoutExpired:
                        process.kill()
                    except Exception as e:
                        print(e)
                        pass
                    FFMPEG_PROCESSES[CHAT] = ""
            if not group_call.is_connected:
                await mp.start_call()
            file=playlist[0][1]
            group_call.input_filename = os.path.join(
                _.workdir,
                DEFAULT_DOWNLOAD_DIR,
                f"{file}.raw"
            )

            await m_status.delete()
            print(f"- دەست بکە بە پەخشکردن: {playlist[0][1]}")
        if not playlist:
            pl = f"{emoji.NO_ENTRY} لیستی پەخشی بەتاڵ"
        else:   
            pl = f"{emoji.PLAY_BUTTON} **ڤ**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**داواکراوە لەلایەن:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        if EDIT_TITLE:
            await mp.edit_title()
        for track in playlist[:2]:
            await mp.download_audio(track)
        if message.chat.type == "تایبەت":
            await message.reply_text(pl)        
        elif LOG_GROUP:
            await mp.send_playlist()
        elif not LOG_GROUP and message.chat.type == "سوپەرگروپ":
            k=await message.reply_text(pl)
            await mp.delete(k)


    if type=="youtube" or type=="query":
        if type=="youtube":
            msg = await message.reply_text("⚡️ **گۆرانی یوتیوب..**")
            url=yturl
        elif type=="query":
            try:
                msg = await message.reply_text("⚡️ **گۆرانیی یوتیوب...**")
                ytquery=ysearch
                results = YoutubeSearch(ytquery, max_results=1).to_dict()
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:40]
            except Exception as e:
                await msg.edit(
                    "گۆرانی نەدۆزرایەوە.\ninline مۆد تاقی بکەوە.."
                )
                print(str(e))
                return
        else:
            return
        ydl_opts = {
            "geo-bypass": True,
            "nocheckcertificate": True
        }
        ydl = YoutubeDL(ydl_opts)
        info = ydl.extract_info(url, False)
        duration = round(info["duration"] / 60)
        title= info["title"]
        if int(duration) > DURATION_LIMIT:
            k=await message.reply_text(f"❌ ڤیدیۆکان درێژترە لە {DURATION_LIMIT} خولەک(ەکان) رێگەپێدراو نین، ڤیدیۆی دابینکراو بریتیە لە {duration} minute(s)")
            await mp.delete(k)
            await mp.delete(message)
            return

        data={1:title, 2:url, 3:"youtube", 4:user}
        playlist.append(data)
        group_call = mp.group_call
        client = group_call.client
        if len(playlist) == 1:
            m_status = await msg.edit(
                f"{emoji.INBOX_TRAY} داگرتن و پرۆسە..."
            )
            await mp.download_audio(playlist[0])
            if 1 in RADIO:
                if group_call:
                    group_call.input_filename = ''
                    RADIO.remove(1)
                    RADIO.add(0)
                process = FFMPEG_PROCESSES.get(CHAT)
                if process:
                    try:
                        process.send_signal(SIGINT)
                    except subprocess.TimeoutExpired:
                        process.kill()
                    except Exception as e:
                        print(e)
                        pass
                    FFMPEG_PROCESSES[CHAT] = ""
            if not group_call.is_connected:
                await mp.start_call()
            file=playlist[0][1]
            group_call.input_filename = os.path.join(
                client.workdir,
                DEFAULT_DOWNLOAD_DIR,
                f"{file}.raw"
            )

            await m_status.delete()
            print(f"- دەست بکە بە پەخشکردن: {playlist[0][1]}")
        else:
            await msg.delete()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} لیستی پەخشکراو بەتاڵە"
        else:
            pl = f"{emoji.PLAY_BUTTON} **لیستی پەخشکراو**:\n" + "\n".join([
                f"**{i}**. **🎸{x[1]}**\n   👤**داواکارە لە لایەن:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        if EDIT_TITLE:
            await mp.edit_title()
        for track in playlist[:2]:
            await mp.download_audio(track)
        if message.chat.type == "تایبەت":
            await message.reply_text(pl)
        if LOG_GROUP:
            await mp.send_playlist()
        elif not LOG_GROUP and message.chat.type == "سوپەر گرووپ":
            k=await message.reply_text(pl)
            await mp.delete(k)
    await mp.delete(message)
            
        
   
@Client.on_message(filters.command(["dplay", f"dplay@{U}"]) & (filters.chat(CHAT) | filters.private))
async def deezer(_, message):
    if ADMIN_ONLY == "Y":
        admins = await mp.get_admins(CHAT)
        if message.from_user.id not in admins:
            k=await message.reply_sticker("CAADBQAD7gIAAq-1OVf2ov3Ge_ngpxYE")
            await mp.delete(k)
            await mp.delete(message)
            return
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if " " in message.text:
        text = message.text.split(" ", 1)
        query = text[1]
    else:
        k=await message.reply_text("You Didn't gave me anything to play use /dplay <song name>")
        await mp.delete(k)
        await mp.delete(message)
        return
    user=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    group_call = mp.group_call
    msg = await message.reply("⚡️ **Fetching Song From Deezer...**")
    try:
        songs = await arq.deezer(query,1)
        if not songs.ok:
            k=await msg.edit(songs.result)
            await mp.delete(k)
            await mp.delete(message)
            return
        url = songs.result[0].url
        title = songs.result[0].title

    except:
        k=await msg.edit("هیج ئەنجامێک نەدۆزراوە")
        await mp.delete(k)
        await mp.delete(message)
        return
    data={1:title, 2:url, 3:"deezer", 4:user}
    playlist.append(data)
    group_call = mp.group_call
    client = group_call.client
    if len(playlist) == 1:
        m_status = await msg.edit(
            f"{emoji.INBOX_TRAY} داگرتن و پرۆسە..."
        )
        await mp.download_audio(playlist[0])
        if 1 in RADIO:
            if group_call:
                group_call.input_filename = ''
                RADIO.remove(1)
                RADIO.add(0)
            process = FFMPEG_PROCESSES.get(CHAT)
            if process:
                try:
                    process.send_signal(SIGINT)
                except subprocess.TimeoutExpired:
                    process.kill()
                except Exception as e:
                    print(e)
                    pass
                FFMPEG_PROCESSES[CHAT] = ""
        if not group_call.is_connected:
            await mp.start_call()
        file=playlist[0][1]
        group_call.input_filename = os.path.join(
            client.workdir,
            DEFAULT_DOWNLOAD_DIR,
            f"{file}.raw"
        )
        await m_status.delete()
        print(f"- پەخشکردن: {playlist[0][1]}")
    else:
        await msg.delete()
    if not playlist:
        pl = f"{emoji.NO_ENTRY} لیستی پەخشی بەتاڵ"
    else:
        pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
            f"**{i}**. **🎸{x[1]}**\n   👤**داواکراوەلە لایەن:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
    if message.chat.type == "private":
        await message.reply_text(pl)
    if EDIT_TITLE:
            await mp.edit_title()
    for track in playlist[:2]:
        await mp.download_audio(track)
    if LOG_GROUP:
        await mp.send_playlist()
    elif not LOG_GROUP and message.chat.type == "supergroup":
        k=await message.reply_text(pl)
        await mp.delete(k)
    await mp.delete(message)



@Client.on_message(filters.command(["player", f"player@{U}"]) & (filters.chat(CHAT) | filters.private))
async def player(_, m: Message):
    if not playlist:
        k=await m.reply_text(f"{emoji.NO_ENTRY} No songs are playing")
        await mp.delete(k)
        await mp.delete(m)
        return
    else:
        pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
            f"**{i}**. **🎸{x[1]}**\n   👤**داواکراوەلە لایەن:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
    if m.chat.type == "private":
        await m.reply_text(
            pl,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="replay"),
                        InlineKeyboardButton("⏯", callback_data="pause"),
                        InlineKeyboardButton("⏩", callback_data="skip")
                    
                    ],

                ]
                )
        )
    else:
        if msg.get('playlist') is not None:
            await msg['playlist'].delete()
        msg['playlist'] = await m.reply_text(
            pl,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔄", callback_data="replay"),
                        InlineKeyboardButton("⏯", callback_data="pause"),
                        InlineKeyboardButton("⏩", callback_data="skip")
                    
                    ],

                ]
                )
        )
    await mp.delete(m)

@Client.on_message(filters.command(["skip", f"skip@{U}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def skip_track(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply("Nothing Playing")
        await mp.delete(k)
        await mp.delete(m)
        return
    if len(m.command) == 1:
        await mp.skip_current_playing()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} لیستی پەخشی بەتاڵ"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
            f"**{i}**. **🎸{x[1]}**\n   👤**داواکراوەلە لایەن:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
        if m.chat.type == "private":
            await m.reply_text(pl)
        if EDIT_TITLE:
            await mp.edit_title()
        if LOG_GROUP:
            await mp.send_playlist()
        elif not LOG_GROUP and m.chat.type == "supergroup":
            k=await m.reply_text(pl)
            await mp.delete(k)
    else:
        try:
            items = list(dict.fromkeys(m.command[1:]))
            items = [int(x) for x in items if x.isdigit()]
            items.sort(reverse=True)
            text = []
            for i in items:
                if 2 <= i <= (len(playlist) - 1):
                    audio = f"{playlist[i].audio.title}"
                    playlist.pop(i)
                    text.append(f"{emoji.WASTEBASKET} {i}. **{audio}**")
                else:
                    text.append(f"{emoji.CROSS_MARK} {i}")
            k=await m.reply_text("\n".join(text))
            await mp.delete(k)
            if not playlist:
                pl = f"{emoji.NO_ENTRY} لیستی پەخشی بەتاڵ"
            else:
                pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                    f"**{i}**. **🎸{x[1]}**\n   👤**داواکراوەلە لایەن:** {x[4]}"
                    for i, x in enumerate(playlist)
                    ])
            if m.chat.type == "private":
                await m.reply_text(pl)
            if EDIT_TITLE:
                await mp.edit_title()
            if LOG_GROUP:
                await mp.send_playlist()
            elif not LOG_GROUP and m.chat.type == "supergroup":
                k=await m.reply_text(pl)
                await mp.delete(k)
        except (ValueError, TypeError):
            k=await m.reply_text(f"{emoji.NO_ENTRY} Invalid input",
                                       disable_web_page_preview=True)
            await mp.delete(k)
    await mp.delete(m)


@Client.on_message(filters.command(["join", f"join@{U}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def join_group_call(client, m: Message):
    group_call = mp.group_call
    if group_call.is_connected:
        k=await m.reply_text(f"{emoji.ROBOT} Already joined voice chat")
        await mp.delete(k)
        await mp.delete(m)
        return
    await mp.start_call()
    chat = await client.get_chat(CHAT)
    k=await m.reply_text(f"Succesfully Joined Voice Chat in {chat.title}")
    await mp.delete(k)
    await mp.delete(m)


@Client.on_message(filters.command(["leave", f"leave@{U}"]) & admin_filter)
async def leave_voice_chat(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Not joined any Voicechat yet.")
        await mp.delete(k)
        await mp.delete(m)
        return
    playlist.clear()
    if 1 in RADIO:
        await mp.stop_radio()
    group_call.input_filename = ''
    await group_call.stop()
    k=await m.reply_text("Left the VoiceChat")
    await mp.delete(k)
    await mp.delete(m)


@Client.on_message(filters.command(["vc", f"vc@{U}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def list_voice_chat(client, m: Message):
    group_call = mp.group_call
    if group_call.is_connected:
        chat_id = int("-100" + str(group_call.full_chat.id))
        chat = await client.get_chat(chat_id)
        k=await m.reply_text(
            f"{emoji.MUSICAL_NOTES} **Currently in the voice chat**:\n"
            f"- **{chat.title}**"
        )
    else:
        k=await m.reply_text(emoji.NO_ENTRY
                                   + "Didn't join any voice chat yet")
    await mp.delete(k)
    await mp.delete(m)


@Client.on_message(filters.command(["stop", f"stop@{U}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def stop_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Nothing playing to stop.")
        await mp.delete(k)
        await mp.delete(m)
        return
    if 1 in RADIO:
        await mp.stop_radio()
    group_call.stop_playout()
    k=await m.reply_text(f"{emoji.STOP_BUTTON} Stopped playing")
    playlist.clear()
    await mp.delete(k)
    await mp.delete(m)


@Client.on_message(filters.command(["replay", f"replay@{U}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def restart_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Nothing playing to replay.")
        await mp.delete(k)
        await mp.delete(m)
        return
    if not playlist:
        k=await m.reply_text("لیستی پەخشی بەتاڵ.")
        await mp.delete(k)
        await mp.delete(m)
        return
    group_call.restart_playout()
    k=await m.reply_text(
        f"{emoji.COUNTERCLOCKWISE_ARROWS_BUTTON}  "
        "Playing from the beginning..."
    )
    await mp.delete(k)
    await mp.delete(m)


@Client.on_message(filters.command(["pause", f"pause@{U}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def pause_playing(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Nothing playing to pause.")
        await mp.delete(k)
        await mp.delete(m)
        return
    mp.group_call.pause_playout()
    k=await m.reply_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Paused",
                               quote=False)
    await mp.delete(k)
    await mp.delete(m)



@Client.on_message(filters.command(["resume", f"resume@{U}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def resume_playing(_, m: Message):
    if not mp.group_call.is_connected:
        k=await m.reply_text("Nothing paused to resume.")
        await mp.delete(k)
        await mp.delete(m)
        return
    mp.group_call.resume_playout()
    k=await m.reply_text(f"{emoji.PLAY_OR_PAUSE_BUTTON} Resumed",
                               quote=False)
    await mp.delete(k)
    await mp.delete(m)

@Client.on_message(filters.command(["clean", f"clean@{U}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def clean_raw_pcm(client, m: Message):
    download_dir = os.path.join(client.workdir, DEFAULT_DOWNLOAD_DIR)
    all_fn: list[str] = os.listdir(download_dir)
    for track in playlist[:2]:
        track_fn = f"{track[1]}.raw"
        if track_fn in all_fn:
            all_fn.remove(track_fn)
    count = 0
    if all_fn:
        for fn in all_fn:
            if fn.endswith(".raw"):
                count += 1
                os.remove(os.path.join(download_dir, fn))
    k=await m.reply_text(f"{emoji.WASTEBASKET} Cleaned {count} files")
    await mp.delete(k)
    await mp.delete(m)


@Client.on_message(filters.command(["mute", f"mute@{U}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def mute(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Nothing playing to mute.")
        await mp.delete(k)
        await mp.delete(m)
        return
    group_call.set_is_mute(True)
    k=await m.reply_text(f"{emoji.MUTED_SPEAKER} Muted")
    await mp.delete(k)
    await mp.delete(m)

@Client.on_message(filters.command(["unmute", f"unmute@{U}"]) & admin_filter & (filters.chat(CHAT) | filters.private))
async def unmute(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Nothing playing to mute.")
        await mp.delete(k)
        await mp.delete(m)
        return
    group_call.set_is_mute(False)
    k=await m.reply_text(f"{emoji.SPEAKER_MEDIUM_VOLUME} Unmuted")
    await mp.delete(k)
    await mp.delete(m)


@Client.on_message(filters.command(['volume', f'volume@{U}']) & admin_filter & (filters.chat(CHAT) | filters.private))
async def set_vol(_, m: Message):
    group_call = mp.group_call
    if not group_call.is_connected:
        k=await m.reply_text("Not yet joined any VC.")
        await mp.delete(k)
        await mp.delete(m)
        return
    if len(m.command) < 2:
        k=await m.reply_text('You forgot to pass volume (1-200).')
        await mp.delete(k)
        await mp.delete(m)
        return
    await group_call.set_my_volume(int(m.command[1]))
    k=await m.reply_text(f"Volume set to {m.command[1]}")
    await mp.delete(k)
    await mp.delete(m)

@Client.on_message(filters.command(["playlist", f"playlist@{U}"]) & (filters.chat(CHAT) | filters.private))
async def show_playlist(_, m: Message):
    if not playlist:
        k=await m.reply_text(f"{emoji.NO_ENTRY} No songs are playing")
        await mp.delete(k)
        await mp.delete(m)
        return
    else:
        pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
            f"**{i}**. **🎸{x[1]}**\n   👤**داواکراوەلە لایەن:** {x[4]}"
            for i, x in enumerate(playlist)
            ])
    if m.chat.type == "private":
        await m.reply_text(pl)
    else:
        if msg.get('playlist') is not None:
            await msg['playlist'].delete()
        msg['playlist'] = await m.reply_text(pl)
    await mp.delete(m)

admincmds=["join", "unmute", "mute", "leave", "clean", "vc", "pause", "resume", "stop", "skip", "radio", "stopradio", "replay", "restart", "volume", f"volume@{U}", f"join@{U}", f"unmute@{U}", f"mute@{U}", f"leave@{U}", f"clean@{U}", f"vc@{U}", f"pause@{U}", f"resume@{U}", f"stop@{U}", f"skip@{U}", f"radio@{U}", f"stopradio@{U}", f"replay@{U}", f"restart@{U}"]

@Client.on_message(filters.command(admincmds) & ~admin_filter & (filters.chat(CHAT) | filters.private))
async def notforu(_, m: Message):
    k=await m.reply("تۆ کێی؟?.")
    await mp.delete(k)
    await mp.delete(m)
allcmd = ["play", "player", f"play@{U}", f"player@{U}"] + admincmds

@Client.on_message(filters.command(allcmd) & ~filters.chat(CHAT) & filters.group)
async def not_chat(_, m: Message):
    buttons = [
        [
            InlineKeyboardButton('🔺 Heroku', url='https://youtu.be/FKaAU4Pr2bw'),
            InlineKeyboardButton('Qovery 🔺', url='https://youtu.be/KC4YdpDGQKg'),
        ],
        [
            InlineKeyboardButton('🆘 Help & Commands 🆘', callback_data='help'),       
        ],
        [
            InlineKeyboardButton('👨‍💻 Developer', url='https://t.me/bny0min'),
            InlineKeyboardButton('Channel 📢', url='https://t.me/mad_tk')
        ]
        ]
    k=await m.reply("<b>You can't use this bot in this group, for that you have to make your own bot from the [Soure Code 👈](https://github.com/bnyaminali/vcplay) below.</b>", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(buttons))
    await mp.delete(m)
