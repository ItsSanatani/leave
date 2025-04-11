import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

app = Client("LeaveBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

SESSIONS = []

@app.on_message(filters.command("addsession") & filters.user(OWNER_ID))
async def add_session(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /addsession <SESSION_STRING>")
    session_str = message.command[1]
    if session_str in SESSIONS:
        return await message.reply("Session already added.")
    SESSIONS.append(session_str)
    await message.reply("Session added.")

@app.on_message(filters.command("removesession") & filters.user(OWNER_ID))
async def remove_session(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /removesession <SESSION_STRING>")
    session_str = message.command[1]
    try:
        SESSIONS.remove(session_str)
        await message.reply("Session removed.")
    except ValueError:
        await message.reply("Session not found.")

@app.on_message(filters.command("sessionstats") & filters.user(OWNER_ID))
async def session_stats(_, message: Message):
    await message.reply(f"Total sessions: {len(SESSIONS)}")

@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID))
async def leave_group(_, message: Message):
    if len(message.command) < 2 or not message.command[1].isdigit():
        return await message.reply("Usage: /leavegroup <count>")
    count = int(message.command[1])
    if not SESSIONS:
        return await message.reply("No sessions added.")
    
    result = "**Leaving Groups Report:**\n"
    for idx, sess_str in enumerate(SESSIONS, start=1):
        left = 0
        try:
            user = Client(sess_str, api_id=API_ID, api_hash=API_HASH, in_memory=True)
            await user.start()
            async for dialog in user.get_dialogs():
                if dialog.chat.type in ["group", "supergroup"]:
                    try:
                        await user.leave_chat(dialog.chat.id)
                        left += 1
                        if left >= count:
                            break
                    except Exception as e:
                        result += f"Session {idx}: Error leaving {dialog.chat.title} – {e}\n"
            await user.stop()
            result += f"Session {idx}: Left {left} groups.\n"
        except Exception as e:
            result += f"Session {idx}: Failed – {e}\n"
    await message.reply(result)

app.run()
