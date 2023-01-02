from weatherCheck import webScrapeWeather

import discord
from discord.ext import commands, tasks
from discord.utils import get

import python_weather
import asyncio

from datetime import datetime
from threading import Timer

import json
from newsgrabber import headlinegrabber
from alarm import initTimer
from alarm import checkTime

from bs4 import BeautifulSoup
import requests

bot = commands.Bot('!')
weather = ''
weatherStatus = ''
headlines = []
timers = []

@bot.event
async def on_ready():
    print('Online!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('!configure'))
    checkTime.start()

@bot.command(aliases=['configure','c'])
async def _start(ctx, *city):
    # await ctx.send('Set your location for weather reports:')
    while True:
        # print('entering loop')
        try:
            global weather
            weather = webScrapeWeather(city)[0]
            global weatherStatus
            weatherStatus = webScrapeWeather(city)[1].capitalize()
            break
        except:
            await ctx.send('Location not found, try again.')
    # print('exited loop 1')
    while True:
        # print('entering loop 2')
        try:
            global headlines
            response = requests.get('https://www.cbc.ca/news')
            headlines = headlinegrabber(response.text)
            # await ctx.send(headlines)
            break
        except:
            await ctx.send('Error in news source, try again.')

    try:
        give_weather.start()
    except:
        pass

@bot.command(aliases=['alarm','a'])
async def _a(ctx, minutes):
    try:
        timers.append(initTimer(minutes))
        await ctx.send(f'Timer has been set for {minutes} minutes.')
    except:
        await ctx.send('Error.')


@tasks.loop(hours = 1)
async def give_weather():
    channel = bot.get_channel(858181017096945674)
    global weather
    print(weather)
    # await channel.send(weather)
    embed=discord.Embed(title="Good Morning, @Jopee!", description="Here's your daily run down:", color=0xffed09)
    embed.set_thumbnail(url="http://ssl.gstatic.com/onebox/weather/64/sunny.png")
    embed.add_field(name=weatherStatus, value=weather, inline=False)
    embed.add_field(name='News Updates', value=f'•{headlines[0]}\n•{headlines[1]}\n•{headlines[2]}\n•{headlines[3]}\n•{headlines[4]}', inline=False)
    await channel.send(embed=embed)

@tasks.loop(seconds = 30)
async def checkTime():
    print('checking time')
    global timers
    print(timers)
    print(datetime.now().strftime("%H"))
    print(datetime.now().strftime("%M"))
    for i in range(len(timers)):
        if timers[i][0] == int(datetime.now().strftime("%H")) and timers[i][1] == int(datetime.now().strftime("%M")):
            channel = bot.get_channel(858181017096945674)
            await channel.send('Alarm!')
            timers.pop(i)
        else:
            pass


bot.run("ODU4MTk5MDA4NzU2MTA1Mjc3.YNaqHA.LADqTigO0NChvx0cAQDDjzOdRxg")