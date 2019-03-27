import discord
import os
from discord.ext import commands
from discord import Game
import asyncio
import random
import requests
import youtube_dl

from playlist import Playlist
from song import Song

discord.opus.load_opus

token = '' # insert secret token here

# all commands must start with !
bot = commands.Bot(command_prefix='!')
musicQueue = Playlist(bot=bot)

# dice roll game
@bot.command(description='Rolls a die with a specified number of sides. Default sides is 6.',
             brief='Roll a die')
async def roll(ctx, sides=6):
    await ctx.send(ctx.message.author.mention + ' rolled a {}!'.format(random.randint(1,int(sides))))

# change bot status in server
@bot.command(name='botstatus')
async def setBotStatus(ctx, gameTitle):
    await bot.change_presence(activity=Game(name=gameTitle))

# moves bot to user's current voice channel
@bot.command()
async def move(ctx):
    voice_client = bot.voice_clients
    author = ctx.message.author
    voice_channel = author.voice.channel
    await voice_client[0].move_to(voice_channel)

# bot joins user's current voice channel and plays requested audio
@bot.command(name='play')
async def music(ctx, url=None):
    # initialize list of voice clients
    voice_client = bot.voice_clients

    # grab location of user sending command
    author = ctx.message.author
    voice_channel = author.voice.channel

    # connects or moves the bot according to current user and bot location
    if not voice_client:
        vc = await voice_channel.connect()
        voice_client = bot.voice_clients
    else:
        vc = voice_client[0]
        if (vc.is_connected() is True) and (vc.channel != voice_channel):
            await vc.move_to(voice_channel)
        elif (vc.is_connected() is False):
            vc = await voice_channel.connect()
            voice_client = bot.voice_clients

    # adds requested song if it is not currently in the playlist
    isAdded = musicQueue.add(url)
    if isAdded == 'not added':
        await ctx.send('Song is already in playlist')
    elif isAdded == 'added':
        if vc.is_playing() is False:
            sound = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(musicQueue.nextSong().source), volume=0.1)
            vc.play(sound)
        else:
            await ctx.send('Song added to playlist')

# lists current playlist
@bot.command()
async def playlist(ctx):
    if not musicQueue.queue:
        await ctx.send('Playlist is empty')
    else:
        await ctx.send('Playlist:')
        for i, song in enumerate(musicQueue.queue):
            await ctx.send('{}. {}'.format(i, song.title))

# skips current song and plays the next song in the playlist
@bot.command(aliases=['nextsong','next','skip'])
async def playnextsong(ctx):
    voice_client = bot.voice_clients
    vc = voice_client[0]
    if vc.is_playing() is True:
        if not musicQueue.queue:
            await ctx.send('Playlist is empty')
        else:
            vc.stop()
            sound = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(musicQueue.nextSong().source), volume=0.1)
            vc.play(sound)

# end current song
@bot.command()
async def stop(ctx):
    voice_client = bot.voice_clients
    if voice_client:
        vc = voice_client[0]
        if vc.is_playing() is True:
            vc.stop()

# pauses current song
@bot.command()
async def pause(ctx):
    voice_client = bot.voice_clients
    if voice_client:
        vc = voice_client[0]
        if vc.is_playing() is True:
            vc.pause()

# resumes current song
@bot.command()
async def resume(ctx):
    voice_client = bot.voice_clients
    if voice_client:
        vc = voice_client[0]
        if vc.is_paused() is True:
            vc.resume()

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