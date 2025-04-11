import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, LOGGER_ID
from pyrogram.enums import ChatType

bot = Client("Bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
SESSIONS = []

# /addsession command
@bot.on_message(filters.command("addsession") & filters.user(OWNER_ID))
async def add_session(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /addsession session_string")
    session = message.command[1]
    if session in SESSIONS:
        return await message.reply("Already added.")
    SESSIONS.append(session)
    await message.reply("Session added.")
    await client.send_message(LOGGER_ID, f"✅ New Session Added!\n\n`{session}`")

# /removesession command
@bot.on_message(filters.command("removesession") & filters.user(OWNER_ID))
async def remove_session(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /removesession session_string")
    session = message.command[1]
    if session in SESSIONS:
        SESSIONS.remove(session)
        await message.reply("Session removed.")
        await client.send_message(LOGGER_ID, f"❌ Session Removed!\n\n`{session}`")
    else:
        await message.reply("Session not found.")

# /sessionstats command
@bot.on_message(filters.command("sessionstats") & filters.user(OWNER_ID))
async def session_stats(client, message: Message):
    await message.reply(f"Total sessions: {len(SESSIONS)}")

# /stats command
@bot.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats_handler(client, message: Message):
    if not SESSIONS:
        return await message.reply("No sessions available.")
    
    msg = await message.reply("Collecting stats, wait...")
    results = []
    
    for session in SESSIONS:
        try:
            user = Client(
                name="temp",
                session_string=session,
                api_id=API_ID,
                api_hash=API_HASH,
            )
            async with user:
                dialogs = user.iter_dialogs()
                count = 0
                async for dialog in dialogs:
                    if dialog.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
                        count += 1
                me = await user.get_me()
                results.append(f"**{me.first_name}**: `{count}` groups")
        except Exception as e:
            results.append(f"**Session Error:** `{e}`")
    
    await msg.edit_text("\n".join(results))

bot.run()
