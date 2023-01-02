# Automatically make roles if they are not there, also automatically add permissions (dead cannot speak in among us)
# Ignore capitalization
# Discord server owner setup initialization (input role names, channel names)
# unmute self, unmute specific persno, mute specific person
# set custom channel for each discord server
# add embeds 
from death import deathMessages
from death import endMessages

import os
import random
import discord
from discord.ext import commands
from discord.utils import get

players = []

bot = commands.Bot(command_prefix='-')
bot.remove_command('help')

# Starts the bot, with a status.
@bot.event
async def on_ready():
    print('Amonger is online!')
    await bot.change_presence(status = discord.Status.online, activity=discord.Game('-help'))

# Error handling.
# @bot.event
# async def on_command_error(ctx, error):
#     embed = discord.Embed(title='ERROR', description='Invalid argument.', colour=discord.Color.orange())
#     await ctx.send(embed=embed)

@bot.command(aliases=['h','help'])
async def _h(ctx):
    embed = discord.Embed(title='Bot Commands', description='-j: join queue\n-e: exit queue\n-q: view queue\n-m: mute all\n-um: unmute all\n-d username: kill player\n-gg: end game')
    await ctx.send(embed=embed)
@bot.command(aliases=['gc','code','start'])
async def _gc(ctx, code):
    embed = discord.Embed(title='GAME CODE:', description='**'+code+'**', colour=discord.Color.orange())
    await ctx.send(embed=embed)

@bot.command(aliases=['mute','m','ma'])
async def _m(ctx):
    global players
    players = []
    if discord.utils.get(ctx.guild.roles, name='Head Amonger') not in ctx.author.roles:
        await ctx.send('```Only users with the Head Amonger role may use the bot.```')
        return
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Among Us')
    for member in voiceChannel.members:
        if discord.utils.get(ctx.guild.roles, name='Dead') not in member.roles:
            await member.edit(mute=True)
        else:
            await member.edit(mute=False)
            await member.move_to(discord.utils.get(ctx.guild.voice_channels, name='Dead'))
    embed = discord.Embed(description='All users in voice channel "' + str(ctx.author.voice.channel) + '" have been muted!', colour=discord.Color.orange())
    await ctx.send(embed=embed)

@bot.command(aliases=['unmute','um','uma'])
async def _um(ctx):
    global players
    players = []
    if discord.utils.get(ctx.guild.roles, name='Head Amonger') not in ctx.author.roles:
        await ctx.send('```Only users with the Head Amonger role may use the bot.```')
        return
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Among Us')
    deadChannel = discord.utils.get(ctx.guild.voice_channels, name='Dead')
    for member in voiceChannel.members:
        await member.edit(mute=False)
    for member in deadChannel.members:
        await member.move_to(discord.utils.get(ctx.guild.voice_channels, name='Among Us'))
        await member.edit(mute=True)
    embed = discord.Embed(description='All users in voice channel "' + str(ctx.author.voice.channel) + '" have been unmuted!', colour=discord.Color.orange())
    await ctx.send(embed=embed)

@bot.command(aliases=['dead','d'])
async def _d(ctx, user:discord.Member):
    global players
    players = []
    if ctx == ctx.author.name:
        pass
    elif discord.utils.get(ctx.guild.roles, name='Head Amonger') not in ctx.author.roles:
        await ctx.send('```Only users with the Head Amonger role may use the bot.```')
        return
    # try:# users can mute themselves if they die
    embed = discord.Embed(description=user.name + random.choice(deathMessages), colour=discord.Color.orange())
    await ctx.send(embed=embed)
    await user.edit(mute=True)
    await user.add_roles(discord.utils.get(ctx.guild.roles, name='Dead'))

@bot.command(aliases=['end','gg']) 
async def _gg(ctx):
    global players
    players = []
    embed = discord.Embed(description=random.choice(endMessages), colour=discord.Color.orange())
    await ctx.send(embed=embed)
    deadChannel = discord.utils.get(ctx.guild.voice_channels, name='Dead')
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Among Us')
    for member in voiceChannel.members:
        await member.edit(mute=False)
    for member in deadChannel.members:
        await member.move_to(voiceChannel)
    for member in voiceChannel.members:
        await member.edit(mute=False)
    for member in ctx.guild.members:
        if discord.utils.get(ctx.guild.roles, name='Dead') in member.roles:
            await member.remove_roles(discord.utils.get(ctx.guild.roles, name='Dead'))

@bot.command(aliases=['join','j'])
async def _j(ctx):
    global players
    if ctx.author.name in players:
        embed = discord.Embed(description='You are already in the queue! Type -exit to leave.')
        await ctx.send(embed=embed)
    else:
        players.append(str(ctx.author.name))
        embed = discord.Embed(title=str(ctx.author.name) + ' wants to play Among Us!', description='There are ' + str(len(players)) + ' players in the queue. Type -join to join the queue!')
        await ctx.send(embed=embed)

@bot.command(aliases=['exit','e'])
async def _e(ctx):
    global players
    if ctx.author.name not in players:
        embed = discord.Embed(description='You cannot leave if you aren\'t in the queue! Type -join to join.')
        await ctx.send(embed=embed)
    else:
        players.remove(str(ctx.author.name))
        embed = discord.Embed(description='You have been removed from the queue. Type -join to rejoin!')
        await ctx.send(embed=embed)

@bot.command(aliases=['queue','q'])
async def _q(ctx):
    global players
    if len(players) > 0:
        embed = discord.Embed(title='**QUEUE:**',description=', '.join(players) + ' are all in the queue.')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='**QUEUE:**', description='No one is in the queue. Type -join to join the queue!')
        await ctx.send(embed=embed)

bot.run(os.environ[('TOKEN')])

# Feature + detect player status?
# Feature - player set waiting music, other stuff