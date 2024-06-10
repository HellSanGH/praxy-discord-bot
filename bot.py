###########################################################################################################################
'''
██████╗░██████╗░░█████╗░██╗░░██╗██╗░░░██╗
██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝╚██╗░██╔╝
██████╔╝██████╔╝███████║░╚███╔╝░░╚████╔╝░
██╔═══╝░██╔══██╗██╔══██║░██╔██╗░░░╚██╔╝░░
██║░░░░░██║░░██║██║░░██║██╔╝╚██╗░░░██║░░░
╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░
'''

import discord
from discord.ext import commands
from discord import app_commands
import time
import re
import os
import json
from math import *
from pytube import YouTube
from moviepy.editor import *
from dotenv import load_dotenv
from pathlib import Path

import requests
import shutil
import interactions

from collections import deque
import asyncio

from bin.modules import aigen
from bin.modules import mcskinretriever
from bin.modules import lovecalc
from bin.modules import helpcmd

###########################################################################################################################
# Constants
counting = 853

last_id = 0
COOLDOWN_AMOUNT = 3.0
last_executed = time.time()

dotenv_path = Path('bin/.env')
load_dotenv(dotenv_path=dotenv_path)
bot_token = os.getenv('BOT_TOKEN')

default_color = 0x30b521

default_embed_thumbnail = "https://media.discordapp.net/attachments/1178067146908123267/1178373863843823746/HC.png?ex=65b682ae&is=65a40dae&hm=ad9b8f9a149e201c4302720cf864084dccabdb54214f6ff98a5cae42c7c30721&=&format=webp&quality=lossless&width=603&height=603" # Replace with "" for no thumbnail
default_embed_displaytime = False
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
#Functions & Class

# Global Variables management
def get_last_id():
    global last_id
    return last_id
def set_last_id(new):
    global last_id
    last_id = new

def get_counting():
    global counting
    return counting
def set_counting(new):
    global counting
    counting = new
###########################################################################################################################
def read():
    f = open('data.json')
    data = json.load(f)
    f.close()
    return data['src_data']
###########################################################################################################################
def assert_cooldown():
    global last_executed
    if last_executed + COOLDOWN_AMOUNT < time.time():
        last_executed = time.time()
        return True
    return False
###########################################################################################################################
class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()
    def add_button(self, url, label):
        button = discord.ui.Button(label=label, url=url)
        self.add_item(button)
        
def embed_default_builder(interaction, embed):
    global default_embed_thumbnail
    global default_embed_displaytime
    if default_embed_thumbnail :
        embed.set_thumbnail(url=default_embed_thumbnail)
    if default_embed_displaytime:
        embed.set_footer(text=f"Command requested by {interaction.user} at {time.ctime()}")
    return embed


def get_music_list():
    music_directory = "musics"
    music_list = []
    for filename in os.listdir(music_directory):
        if filename.endswith(".mp3"):
            music_list.append(filename[:-4].lower())
    print("[PNH Logs] Music list : ",music_list)
    return music_list

###########################################################################################################################
# Discord initialisation
intents = discord.Intents.all()
intents.messages = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

###########################################################################################################################
#Tree Commands

###########################################################################################################################
# HELP
###########################################################################################################################
@tree.command(name="help", description="Help for the entirety of the available bot commands.")
async def help(interaction):
    embed = discord.Embed(
        title="Help command",
        description="__Commands__ \n**help** : Display this message.\
            \n**lovecalc @1 @2** : Calculate the love between two people (with accuracy :D)\
            \n**minecraftuser <user>**: Retrieve information on a Minecraft user by their username.\
            \n> __Music commands:__\
            \n**play <music>** : Play a music in the General Voice Channel.\
            **disconnect** : Disconnects the bot from VC.\
            \nYou can also use <@1186799421636231208> + message to chat with me !\
            \nNot much else for now <a:RotatingSkull:1145453604086485075>",
        color=default_color
    )
    embed = embed_default_builder(interaction, embed)
    await interaction.response.send_message(embed=embed)

###########################################################################################################################
# PLAY (music)

music_queue = deque()
last_play_channel_id = None

@tree.command(name="play", description="Plays a music that is in the list of available musics.")
async def play(interaction, music_name: str):
    global last_play_channel_id
    voice_client = interaction.guild.voice_client

    if not interaction.user.voice or not interaction.user.voice.channel:
        embed = discord.Embed(description="You are not connected to a voice channel.", color=default_color)
        await interaction.response.send_message(embed=embed)
        return

    user_voice_channel = interaction.user.voice.channel
    if voice_client and voice_client.is_connected():
        bot_voice_channel = voice_client.channel
        if user_voice_channel != bot_voice_channel:
            embed = discord.Embed(description="You are not in the same voice channel as the bot.", color=default_color)
            await interaction.response.send_message(embed=embed)
            return
    else:
        await user_voice_channel.connect()
        voice_client = interaction.guild.voice_client


    if voice_client.is_playing() and music_name.lower() in get_music_list():
        music_queue.append(music_name.lower().capitalize())
        queue_message = format_queue()
        embed = discord.Embed(
            description=f"**{music_name.lower().capitalize()}** has been added to the queue.\n\n{queue_message}",
            color=default_color
        )
        await interaction.response.send_message(embed=embed)
        return
    if music_name.lower() not in get_music_list():
        embed = discord.Embed(
            description=f"**Could not find \"{music_name.lower().capitalize()}\"**. You may choose musics through {get_music_list()}.",
            color=default_color
        )
        await interaction.response.send_message(embed=embed)


    await start_playing(interaction, music_name)


async def on_music_end(interaction):
    global last_play_channel_id, music_queue
    voice_client = interaction.guild.voice_client



    # Start playing the next music in the queue
    if music_queue:
        print("there's a queue and next music is ", music_queue[0])
        voice_client.stop()
        await start_playing(interaction, music_queue.popleft())
    else:
        # If the queue is empty, send a message indicating that to the channel where /play was invoked
        last_channel = interaction.guild.get_channel(last_play_channel_id)
        if last_channel:
            embed = discord.Embed(
                title="Queue Empty",
                description="There are no more songs in the queue.",
                color=default_color
            )
            await last_channel.send(embed=embed)

async def start_playing(interaction, music_name):
    global last_play_channel_id, music_queue
    voice_client = interaction.guild.voice_client

    file_path = f"musics/{music_name.lower().capitalize()}.mp3"
    audio_source = discord.FFmpegPCMAudio(file_path)
        
    if not voice_client or not voice_client.is_connected():
        await interaction.user.voice.channel.connect()
        voice_client = interaction.guild.voice_client

    voice_client.play(audio_source)
    if music_queue:
        music_queue.pop()
    queue_message = format_queue()
    now_playing = f"🎵 **Now Playing** 🎵 | {music_name.lower().capitalize()}\n{queue_message}"
    embed = discord.Embed(
        description=now_playing,
        color=default_color
    )
    print("EEE")

    await interaction.response.send_message(embed=embed)
    last_play_channel_id = interaction.channel_id
    await on_music_end(interaction)


# Command to skip music
@tree.command(name="skip", description="Skips the current music and plays the next one in the queue.")
async def skip(interaction):
    voice_client = interaction.guild.voice_client


    if not interaction.user.voice or not interaction.user.voice.channel:
        embed = discord.Embed(
            description="You are not connected to a voice channel.",
            color=default_color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    user_voice_channel = interaction.user.voice.channel
    if not voice_client or not voice_client.is_connected():
        embed = discord.Embed(
            description="The bot is not connected to a voice channel.",
            color=default_color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    bot_voice_channel = voice_client.channel
    if user_voice_channel != bot_voice_channel:
        embed = discord.Embed(
            description="You are not in the same voice channel as the bot.",
            color=default_color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if voice_client.is_playing():
        voice_client.stop()
        if music_queue:
            await start_playing(interaction, music_queue[0])
        else:
            embed = discord.Embed(
                description="⏭️ **Skipped** the current music. There are no more songs in the queue.",
                color=default_color
            )
            await interaction.response.send_message(embed=embed)
            return
    else:
        embed = discord.Embed(
            description="There are no songs to skip.",
            color=default_color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

def format_queue():
    if not music_queue:
        return "The queue is empty."
    queue_message = "\n".join([f"> {music}" for music in music_queue])
    return f"**Queue:**\n{queue_message}"


###########################################################################################################################
# DISCONNECT
###########################################################################################################################
@tree.command(name="disconnect", description="Disconnects the bot from the voice channel if it's connected.")
async def disconnect(interaction):
    voice_client = interaction.guild.voice_client

    if not voice_client or not voice_client.is_connected():
        embed = discord.Embed(
            description="The bot is not connected to a voice channel.",
            color=default_color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    await voice_client.disconnect()

    embed = discord.Embed(
        description="The bot has been disconnected from the voice channel.",
        color=default_color
    )
    await interaction.response.send_message(embed=embed)


###########################################################################################################################
# Lovecalc
@tree.command(name="lovecalc", description="Calculate the love between two users (with accuracy fr fr)")
async def love_calc(interaction, user1: str, user2: str):
    try: #Retrieve the user ids
        int(user1[2:len(user1)-1]) 
        int(user2[2:len(user2)-1])
    except :
        await interaction.response.send_message("Please provide 2 valid users.", ephemeral=True)
        return
    if not re.match(r'<@\d+>', user1) or not re.match(r'<@\d+>', user2):
        await interaction.response.send_message("Please provide 2 valid users.", ephemeral=True)
        return
    love, comment = lovecalc.lovecalc(user1, user2)
    embed = discord.Embed(
        title="Lovecalc \<3",
        description=f"I'd estimate the love between {user1} and {user2} to be {love}%...\n{comment}",
        color=default_color
    )
    embed = embed_default_builder(interaction, embed)
    await interaction.response.send_message(embed=embed)
    
###########################################################################################################################
# Minecraft User
@tree.command(name="minecraftuser", description="Receive information on a minecraft user")
async def minecraftuser(interaction: discord.Interaction, username: str):
    retrieve = mcskinretriever.retrieve_mc_skin(username)
    if retrieve:
        embed, is_capeof = mcskinretriever.embed_builder_mc(retrieve, interaction.user)
        download_url = retrieve[3]
        name = retrieve[2]
        view = ButtonView()
        view.add_button(download_url, "Download Skin")
        namemc_link = f"https://namemc.com/profile/{name}"
        view.add_button(namemc_link, "NameMC Page")
        if is_capeof:
            view.add_button(f"http://s.optifine.net/capes/{name}.png", "Optifine Cape")
        await interaction.response.send_message(embed=embed, view=view)
    else:
        await interaction.response.send_message(content=f"Username '{username}' was not found. This may be due to the rate limit of the Mojang API.", ephemeral=True)

###########################################################################################################################
###########################################################################################################################
###########################################################################################################################


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print("[PNH Log] "+str(message)+" "+str(message.content))
###########################################################################################################################
    if message.content.startswith("<@1186799421636231208>") and len(message.content)>23:
        aireply = aigen.aigen(message.content[23:])
        await message.channel.send(aireply)
###########################################################################################################################
    # Instant Replies
    if "💀" in message.content or "☠️" in message.content:
        emoji_skull = '\U0001F480'
        await message.add_reaction(emoji_skull)
###########################################################################################################################
    # Persistent message in counting
    if message.channel.id == 996713647386673182 and assert_cooldown(): 
        current = get_counting()
        last = get_last_id()
        if last != 0:
            try:
                msg = await message.channel.fetch_message(last)
                await msg.delete()
            except discord.errors.NotFound:
                pass
        sent = await message.channel.send("**Counting channel :** When in doubt, just count. Try not making me lose my count \:D Warning : Deleting count messages = ban from counting. Current count : "+str(current + 1))
        set_last_id(sent.id)
###########################################################################################################################



@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.id == 960057732260560926:
            await tree.sync(guild=guild)
            print(f'Synced commands for guild: {guild.name}')
            break
    print('We have logged in as {0.user}'.format(bot))



bot.run(bot_token)