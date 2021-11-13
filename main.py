from typing import ContextManager
import discord
from discord.ext import commands
import os
import time

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
    source.volume(0.5)
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

token = os.getenv("DiscordBot")
bot.run(token)