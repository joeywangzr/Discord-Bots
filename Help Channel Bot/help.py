import os
import random
import discord
from discord.ext import commands
from discord.utils import get

import requests
import bs4

import time
from random import randint

bot = commands.Bot(command_prefix='ok joey')
bot.remove_command('help')
messageID = ''

occupiedChannels = []
pinnedUsers = []
# Starts the bot, with a status
@bot.event
async def on_ready():
    print('HELP is online!')
    await bot.change_presence(status = discord.Status.online, activity=discord.Game('=covid'))

@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title='```ERROR```', description='Invalid argument.', colour=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command(aliases=['h','help'])
async def _h(ctx):
    await ctx.send('Ping @Jopee for help lol')

# Perhaps auto open if message sent?

@bot.command(aliases=['google'])
async def _google(ctx): 
    await ctx.send('Ping @Jopee for help lol')

@bot.event
async def on_message(ctx):
    # Check if "help" channel
    global messageID 
    if str(ctx.channel.category) == 'help: open' or str(ctx.channel.category) == 'help: occupied':
        if ctx.author.name == 'Joey Bot':
            return
        if str(ctx.channel.category) == 'help: open':
            if str(ctx.channel) not in occupiedChannels:
                if ctx.author.name in pinnedUsers:
                    await ctx.channel.send('You are already occupying a help channel.')
                    return
                occupiedChannels.append(str(ctx.channel))

                # pinnedUsers[str(ctx.author.name)] = str(ctx.id)
                pinnedUsers.append(str(ctx.author.name))
                embed = discord.Embed(title='This help channel is now occupied', description='Type =thanks once your question has been answered.', colour=discord.Color.blue())
                await ctx.channel.send(embed=embed)
                channel = ctx.channel
                await channel.edit(category=bot.get_channel(751301312800358423))
                await ctx.pin(reason=None)
                messageID = ctx.id
                print(pinnedUsers)
            
            else:
                pass

        if str(ctx.channel.category) == 'help: occupied':
            if ctx.content.startswith('=thanks'):
                if ctx.author.name in pinnedUsers or ctx.author.name == 'Jopee':

                    channel = ctx.channel
                    if str(channel) in occupiedChannels:
                        occupiedChannels.remove(str(channel))
                    # await ctx.channel.purge()
                    embed = discord.Embed(title='This help channel is now open', description='Type your question here and a helper will help you!', colour=discord.Color.blue())
                    await channel.send(embed=embed)
                    await channel.edit(category=bot.get_channel(751325411782426644))

                    pinnedUsers.remove(ctx.author.name)
                    print(pinnedUsers)
                
                    message = await channel.fetch_message(messageID)
                    await message.unpin(reason=None)
                else:
                    pass

    elif 'ib' in str(ctx.channel) and str(ctx.channel).replace('-',' ').index('ib')>3:
        if ctx.content.startswith('=grade'):
            channel = str(ctx.channel).replace('-',' ')
            ib_index = channel.index('ib')-1
            subject = channel[0:ib_index].capitalize()
            if ctx.author.nick == None:
                await ctx.channel.send(ctx.author.name + '\'s predicted IB grade' + ' in ' + subject + ' is: ' + str(randint(1,7)))
                return
            await ctx.channel.send(ctx.author.nick + '\'s predicted IB grade' + ' in ' + subject + ' is: ' + str(randint(1,7)))


    elif ctx.content.startswith('=covid'):
        result = requests.get('https://www.alberta.ca/covid-19-alberta-data.aspx')
        soup = bs4.BeautifulSoup(result.text,'lxml')
        x = soup.select('.goa-table')[0].getText()
        x = x.split()

        canada_cases = x[69]
        alberta_cases = x[84]
        calgary_cases = x[98]
        
        y = soup.select('p')[8].getText()

        # edmonton_cases = x[108]
        embed = discord.Embed(title='**COVID-19 STATS**', description=f'There are currently: \n• **{canada_cases}** confirmed cases in :flag_ca: \n• **{alberta_cases}** active cases in Alberta <a:jelly:753472309783953448>\n• **{calgary_cases}** active cases in Calgary <a:lsdjelly:753472310417293334>\n{y}\nStay safe!', colour=discord.Color.blue())
        await ctx.channel.send(embed=embed)

    elif ctx.content.startswith('=help'):
        embed = discord.Embed(title='**Bot Commands**', description=f'=thanks to close a channel \n=covid to get COVID-19 stats in Alberta \n=grade to get your predicted IB grade (IB Channels only)', colour=discord.Color.blue())
        await ctx.channel.send(embed=embed)

    elif ctx.content.startswith('=lobster'):
        await ctx.channel.send('\*at the red lobster*')
        time.sleep(3)
        await ctx.channel.send('me: i will have the red lobster')
        time.sleep(1)
        await ctx.channel.send('waiter: okay')

bot.run(os.environ[('TOKEN')])