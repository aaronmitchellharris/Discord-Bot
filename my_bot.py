import discord
from discord.ext import commands
from discord import Game
import asyncio
import random
import requests

discord.opus.load_opus

token = 'NTU4ODM1MDM2NjU3Mjg3MTY4.D3coeA.pJy2d-ZdR3fdn06-4zjVUsJhoUo'

bot = commands.Bot(command_prefix='!')


@bot.command()
async def test(ctx):
    await ctx.send('I heard you! {0}'.format(ctx.author))

@bot.command(description='Rolls a die with a specified number of sides. Default sides is 6.',
             brief='Roll a die')
async def roll(ctx, sides=6):
    await ctx.send(ctx.message.author.mention + ' rolled a {}!'.format(random.randint(1,int(sides))))

@bot.command(name='botstatus')
async def setBotStatus(ctx, gameTitle):
    await bot.change_presence(activity=Game(name=gameTitle))


@bot.command(name='play')
async def music(ctx, url=None, vc = None):
    author = ctx.message.author
    voice_channel = author.voice.channel
    await voice_channel.connect()

@bot.command()
async def dc(ctx):
    voice_client = bot.voice_clients
    if voice_client:
        await voice_client[0].disconnect()

@bot.command()
async def die(ctx):
    await bot.logout()

bot.run(token)
