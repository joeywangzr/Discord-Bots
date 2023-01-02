import discord
from discord.ext import commands
from discord.utils import get
import glob
import asyncio
import time
import random
import os

token = "ODU4MTk5MDA4NzU2MTA1Mjc3.YNaqHA.LADqTigO0NChvx0cAQDDjzOdRxg"
bot = commands.Bot('!')

@bot.event
async def on_message(message):
    if message.content.startswith('$greet'):
        channel = message.channel
        await channel.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await bot.wait_for('message', check=check)
        await channel.send('Hello {.author}!'.format(msg))

bot.run(token)
