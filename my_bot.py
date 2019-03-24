import discord
import os
from discord.ext import commands
from discord import Game
import asyncio
import random
import requests
import youtube_dl

discord.opus.load_opus

token = '' # insert secret token here

# all commands must start with !
bot = commands.Bot(command_prefix='!')

@bot.command()
async def test(ctx):
    await ctx.send('I heard you! {0}'.format(ctx.author))

# dice roll game
@bot.command(description='Rolls a die with a specified number of sides. Default sides is 6.',
             brief='Roll a die')
async def roll(ctx, sides=6):
    await ctx.send(ctx.message.author.mention + ' rolled a {}!'.format(random.randint(1,int(sides))))

# change bot status in server
@bot.command(name='botstatus')
async def setBotStatus(ctx, gameTitle):
    await bot.change_presence(activity=Game(name=gameTitle))


global musicQueue
musicQueue = []

# bot joins user's current voice channel and plays requested audio
@bot.command(name='play')
async def music(ctx, url=None):
    voice_client = bot.voice_clients

    # check if there is a voice_client created already, otherwise creates a new one
    if not voice_client:
        author = ctx.message.author
        voice_channel = author.voice.channel
        vc = await voice_channel.connect()
    else:
        vc = voice_client[0]

    # music queue
    musicQueue.append(url)

    # extracts info from youtube url
    opts = {}
    with youtube_dl.YoutubeDL(opts) as ydl:
        song_info = ydl.extract_info(musicQueue[0], download=False)

    # finds audio url with highest average bit rate
    seq = [x.get('abr') for x in song_info['formats'] if x.get('abr') is not None]
    maxAbrIndex = seq.index(max(seq))

    # plays the audio
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song_info['formats'][maxAbrIndex]['url']), volume=0.1)
    vc.play(source)

# end current song
@bot.command()
async def stop(ctx):
    voice_client = bot.voice_clients
    if voice_client:
        if voice_client[0].is_playing() == True:
            await voice_client[0].pause()

# pauses current song
@bot.command()
async def pause(ctx):
    voice_client = bot.voice_clients
    if voice_client:
        if voice_client[0].is_playing() == True:
            await voice_client[0].pause()

# resumes current song
@bot.command()
async def resume(ctx):
    voice_client = bot.voice_clients
    if voice_client:
        if voice_client[0].is_paused() == True:
            await voice_client[0].resume()

# bot leaves current voice channel
@bot.command()
async def dc(ctx):
    voice_client = bot.voice_clients
    if voice_client:
        await voice_client[0].disconnect()

# bot shuts down
@bot.command()
async def die(ctx):
    await bot.logout()

bot.run(token)