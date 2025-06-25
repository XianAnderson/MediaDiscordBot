print("🛠️ Starting Discord bot...")

import os
import docker
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("AUTHORIZED_CHANNEL_ID"))
TARGET_CONTAINER = os.getenv("TARGET_CONTAINER")

ALLOWED_USERS = [
    406303869384130562, 247935882118692864
]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print(f"🔧 Channel ID: {CHANNEL_ID}")
    print(f"🔧 Allowed Users: {ALLOWED_USERS}")
    print(f"🔧 Target Container: {TARGET_CONTAINER}")

@bot.event
async def on_message(message):
    print(f"📨 {message.author} said: {message.content} in #{message.channel.name}")
    await bot.process_commands(message)

@bot.command(name="restart")
async def restart_container(ctx):
    if ctx.channel.id != CHANNEL_ID:
        return

    if ctx.author.id not in ALLOWED_USERS:
        await ctx.send("🚫 You are not authorized to use this command.")
        return

    await ctx.send("🔄 Restarting container...")
    try:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        client.containers.get(TARGET_CONTAINER).restart()
        await ctx.send(f"✅ Container `{TARGET_CONTAINER}` restarted.")
    except Exception as e:
        await ctx.send(f"❌ Failed to restart container: {e}")
        print(f"❌ Docker SDK error: {e}")

bot.run(TOKEN)
