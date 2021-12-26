from typing import ContextManager
import discord
from discord.ext import commands
import os
import time
import youtube_dl
import asyncio
from speech.speechSynt import makeSpeech

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

intents = discord.Intents.default()
intents.typing = False
intents.presences = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='$',  intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    for g in bot.guilds:
        print("guild =", g)
    print('------')

@bot.command()
async def play(ctx : commands.Context, *args):
    print("play command !")
    if len(args) != 1:
        await ctx.send("provide one of the following songs : avengers or deja-vu")
        return
    if args[0] == "avengers":
        query = "avengers-suite-theme.mp3"
    elif args[0] == "deja-vu":
        query = "initial-d-deja-vu.mp3"
    else:
        await ctx.send("provide one of the following songs : avengers or deja-vu")
        return

    if ctx.author.voice == None:
        await ctx.send("You are not in a channel !")
        return

    voice_channel = ctx.author.voice.channel
    voice = ctx.channel.guild.voice_client
    if voice is None:
        voice = await voice_channel.connect()
    elif voice.channel != voice_channel:
        await voice.move_to(voice_channel)
        time.sleep(3)

    voice = ctx.channel.guild.voice_client
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    #source.volume(0.5)
    voice.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send('Now playing: {}'.format(query))

@bot.command()
async def stop(ctx :commands.Context):
    print("stop command !")
    voice = ctx.channel.guild.voice_client
    if voice != None:
        voice.stop()
    await bot.logout()

@bot.command()
async def goAram(ctx : commands.Context):
    print("goAram command !")
    channel = discord.utils.get(ctx.guild.voice_channels, name="АRАМ")
    if channel == None:
        channel = discord.utils.get(ctx.guild.voice_channels, name="ARAM") # try with latin keyboard
    if (channel != None):
        allMembers = list(bot.get_all_members())
        await ctx.send("all users in channels move to channel ARAM!")
        for member in allMembers:
            if (member.voice != None): 
                print(member, "moves to", channel)
                await member.move_to(channel)


async def from_url(url, *, loop=None, stream=False):
    loop = loop or asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

    if 'entries' in data:
        # take first item from a playlist
        data = data['entries'][0]

    filename = data['url'] if stream else ytdl.prepare_filename(data)
    return discord.FFmpegPCMAudio(filename, **ffmpeg_options), data['title']

@bot.command()
async def join(self, ctx, *, channel: discord.VoiceChannel):
    """Joins a voice channel"""

    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)

    await channel.connect()

@bot.command()
async def yt(ctx :commands.Context, url):
    print("yt command !")
    if ctx.author.voice == None:
        await ctx.send("You are not in a channel !")
        return

    voice_channel = ctx.author.voice.channel
    voice = ctx.channel.guild.voice_client
    if voice is None:
        voice = await voice_channel.connect()
    elif voice.channel != voice_channel:
        await voice.move_to(voice_channel)

    """Plays from a url (almost anything youtube_dl supports)"""

    async with ctx.typing():
        
        player, title = await from_url(url, loop=bot.loop, stream = True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('Now playing: {}'.format(title))

@bot.command()
async def say(ctx : commands.Context, *args):
    print("say command !")
    query = "poryadok.mp3"

    if len(args) != 1:
        #await ctx.send("provide a number")
        #return
        pass
    if args[0] == "1":
        query = "report.mp3"
    elif args[0] == "2":
        query = "giguli.mp3"
    elif args[0] == "3":
        query = "poryadok.mp3"
    else:
        await ctx.send("I will say that")
        words = ''.join(args)
        fileName = makeSpeech(words)
        query = fileName

    if ctx.author.voice == None:
        await ctx.send("You are not in a channel !")
        return

    voice_channel = ctx.author.voice.channel
    voice = ctx.channel.guild.voice_client
    if voice is None:
        voice = await voice_channel.connect()
    elif voice.channel != voice_channel:
        await voice.move_to(voice_channel)
        time.sleep(3)

    voice = ctx.channel.guild.voice_client
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
    #source.volume(0.5)
    voice.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
    #await ctx.send('Now playing: {}'.format(query))

token = os.getenv("DiscordBot")
bot.run(token)