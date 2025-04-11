import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, OWNER_ID
from sessions import add_session_string, remove_session_string, get_all_sessions

bot = Client("BotSession", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
user = Client(SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

@bot.on_message(filters.command("addsession") & filters.private)
async def add_session_handler(_, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Unauthorized!")
    
    try:
        session = message.text.split(" ", 1)[1].strip()
    except IndexError:
        return await message.reply("Please provide a session string.")

    if add_session_string(session):
        return await message.reply("✅ Session added successfully.")
    else:
        return await message.reply("⚠️ Session already exists.")

@bot.on_message(filters.command("removesession") & filters.private)
async def remove_session_handler(_, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Unauthorized!")
    
    try:
        session = message.text.split(" ", 1)[1].strip()
    except IndexError:
        return await message.reply("Please provide a session string.")

    if remove_session_string(session):
        return await message.reply("✅ Session removed successfully.")
    else:
        return await message.reply("⚠️ Session not found.")

@bot.on_message(filters.command("sessionstats") & filters.private)
async def session_stats_handler(_, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Unauthorized!")

    sessions = get_all_sessions()
    await message.reply(f"Total Sessions: {len(sessions)}")


@bot.on_message(filters.command("start") & filters.private)
async def start_handler(_, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Unauthorized!")
    await message.reply("Hello! Use /leaveallgroups to leave all groups or /stats to get chat stats.")

@bot.on_message(filters.command("leaveallgroups") & filters.private)
async def leave_groups_handler(_, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Unauthorized!")
    
    await message.reply("Leaving all groups...")
    left_count = 0

    async with user:
        async for dialog in user.get_dialogs():
            chat = dialog.chat
            if chat.type in ["group", "supergroup"]:
                try:
                    await user.leave_chat(chat.id)
                    left_count += 1
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"Error leaving {chat.title}: {e}")
    
    await message.reply(f"Left {left_count} groups.")

@bot.on_message(filters.command("stats") & filters.private)
async def stats_handler(_, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("Unauthorized!")
    
    groups = supergroups = channels = privates = bots = 0

    async with user:
        async for dialog in user.get_dialogs():
            chat = dialog.chat
            if chat.type == "group":
                groups += 1
            elif chat.type == "supergroup":
                supergroups += 1
            elif chat.type == "channel":
                channels += 1
            elif chat.type == "private":
                if chat.is_bot:
                    bots += 1
                else:
                    privates += 1

    await message.reply(
        f"**Stats:**\n"
        f"- Groups: {groups}\n"
        f"- Supergroups: {supergroups}\n"
        f"- Channels: {channels}\n"
        f"- Private Chats: {privates}\n"
        f"- Bots: {bots}"
    )

bot.run()
