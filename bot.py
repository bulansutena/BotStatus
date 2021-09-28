
import pytz
import logging
import asyncio
from time import sleep
from datetime import datetime as dt
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.errors.rpcerrorlist import MessageNotModifiedError, FloodWaitError
from decouple import config
from telethon.sessions import StringSession
from telethon import TelegramClient

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

try:
    appid = config("APP_ID")
    apihash = config("API_HASH")
    session = config("SESSION", default=None)
    chnl_id = config("CHANNEL_ID", cast=int)
    msg_id = config("MESSAGE_ID", cast=int)
    botlist = config("BOTS")
    bots = botlist.split()
    session_name = str(session)
    user_bot = TelegramClient(StringSession(session_name), appid, apihash)
    print("Started")
except Exception as e:
    print(f"ERROR\n{str(e)}")

async def BotzHub():
    async with user_bot:
        while True:
            print("[INFO] starting to check uptime..")
            try:
                await user_bot.edit_message(
                    int(chnl_id),
                    msg_id,
                    "**Status 📈 Bot SF Corp 🤖 :**\n\n`Sedang dalam pengecekan...`",
                )
            except MessageNotModifiedError:
                pass
            c = 0
            edit_text = "**Status 📈  🤖 :**\n(Update Setiap 1 Jam)\n\n"
            for bot in bots:
                try:
                    print(f"[INFO] checking @{bot}")
                    snt = await user_bot.send_message(bot, "/start")
                    await asyncio.sleep(10)

                    history = await user_bot(
                        GetHistoryRequest(
                            peer=bot,
                            offset_id=0,
                            offset_date=None,
                            add_offset=0,
                            limit=1,
                            max_id=0,
                            min_id=0,
                            hash=0,
                        )
                    )

                    msg = history.messages[0].id
                    if snt.id == msg:
                        print(f"@{bot} is down.")
                        edit_text += f"🤖 @{bot}\n📊 Status: `DOWN` ❌\n\n"
                    elif snt.id + 1 == msg:
                        edit_text += f"🤖 @{bot} \n📊 Status: `UP` ✅\n\n"
                    await user_bot.send_read_acknowledge(bot)
                    c += 1
                except FloodWaitError as f:
                    print(f"Floodwait!\n\nSleeping for {f.seconds}...")
                    sleep(f.seconds + 10)
            await user_bot.edit_message(int(chnl_id), int(msg_id), edit_text)
            k = pytz.timezone("Asia/Jakarta")
            month = dt.now(k).strftime("%B")
            day = dt.now(k).strftime("%d")
            year = dt.now(k).strftime("%Y")
            t = dt.now(k).strftime("%H:%M:%S")
            edit_text += f"\n**Terakhir Check ⏳ Pada** :\n`[UTC+7] {day} {month} {year} - {t} WIB`"
            await user_bot.edit_message(int(chnl_id), int(msg_id), edit_text)
            print(f"Checks since last restart - {c}")
            print("Tidur for 1 Jam.")
            await asyncio.sleep(1 * 60 * 60)

user_bot.loop.run_until_complete(BotzHub())
