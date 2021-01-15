import discord
import random
import os
import asyncio
from discord.ext import commands

fortune_responses = ['As I see it, yes.','Ask again later.','Better not tell you now.','Cannot predict now.','Concentrate and ask again.','Don’t count on it.','It is certain.','It is decidedly so.','Most likely.','My reply is no.','My sources say no.','Outlook not so good.','Outlook good.','Reply hazy, try again.','Signs point to yes.','Very doubtful.','Without a doubt.','Yes.','Yes – definitely.','You may rely on it.']

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

@client.command()
async def help(ctx, command=None):
    # FORMAT
    #embed.add_field(name='name', value='value', inline=True)

    if command == 'roulette':
        emb = discord.Embed(color=discord.Color.orange(), description='Roulette Command Help')
        emb.set_author(name='Help')
        emb.add_field(name='Command', value='.roulette [#] [Roulette Bets]', inline=True)
        emb.add_field(name='Roulette Bets', value='These are the diffrent categories on the roulette board you bet the ball will land. You can look at the options/roulette board picture once you use the command', inline=True)
        emb.add_field(name='Example', value='.roulette 50 black 5 16 8', inline=True)
        emb.add_field(name='Extra', value='Your set bet amount will be bet on each option you select. So if you have 2 options set like "c1 and 17", then you will bet your bet amount twice', inline=True)
        await ctx.send(embed=emb)
    elif command == None or command == '1':

        embed = discord.Embed(color=discord.Color.orange(), description='All Avaliable Commands for Bot [Use {.help [#]} for the next page of commands]')
        embed.set_author(name='Help')
        embed.set_thumbnail(url='https://t4.ftcdn.net/jpg/03/96/76/81/360_F_396768192_wyVwIwcmZH4IJUMxVs4wwnndkSZHtvsf.jpg')
        #embed.set_image(url='https://t4.ftcdn.net/jpg/03/96/76/81/360_F_396768192_wyVwIwcmZH4IJUMxVs4wwnndkSZHtvsf.jpg')
        embed.add_field(name='Admin', value='----Admin Only Commands----', inline=False)
        embed.add_field(name='ban', value='.ban [@user]: Bans the mentioned user', inline=True)
        embed.add_field(name='kick', value='.kick [@user]: Kicks the mentiond user', inline=True)
        embed.add_field(name='unban', value='.unban [user#1111]: Unbans user from servers ban list', inline=True)
        embed.add_field(name='Utilities', value='----Utility Commands----', inline=False)
        embed.add_field(name='clear', value='.clear [#]: Clears selcted amount of messages', inline=True)
        embed.add_field(name='ping', value='.ping: Gives bot latency and online status', inline=True)
        embed.add_field(name='returnid', value='.returnid [@user]: Returns the id of user mentioned', inline=True)
        embed.add_field(name='Fun', value='----Fun Commands----', inline=False)
        embed.add_field(name='8ball', value='.8ball {question}: The all knowing bot answers your question', inline=True)
        embed.add_field(name='say', value='.say {text}: Makes the bot say what you want', inline=True)
        embed.add_field(name='muteparents', value='.muteparents: Toggles parents ability to speak', inline=True)

        await ctx.send(embed=embed)

    elif command == '2':

        embed = discord.Embed(color=discord.Color.orange(), description='Commands Help, [Pg. 2]')
        embed.set_author(name='Help')
        embed.add_field(name='Economy', value='----Economy Commands----', inline=False)
        embed.add_field(name='balance', value='.balance: See your money balance', inline=True)
        embed.add_field(name='beg', value='.beg: Beg to get $$. Cooldown is 1 hour', inline=True)
        embed.add_field(name='deposit', value='.deposit [#]: Deposit wallet $ to bank $', inline=True)
        embed.add_field(name='withdraw', value='.withdraw [#]: Withdraw wallet $ to bank $', inline=True)
        embed.add_field(name='steal', value='.steal [@user]: Steal a random amount from a users wallet', inline=True)
        embed.add_field(name='pay', value='.pay [@user] [#]: Pay users from your wallet', inline=True)
        embed.add_field(name='request', value='.request [@user] [#] [Reason:optional]: Request money from user', inline=True)
        embed.add_field(name='heist', value='.heist [@user]: Initiate a hesit on a users bank account', inline=True)
        embed.add_field(name='murder', value='.murder [@user]: 1/10000 to murder someone and take all their money', inline=True)
        embed.add_field(name='daily', value='.daily: Claim your daily $300', inline=True)
        embed.add_field(name='Gambling', value='----Gambling Commands----', inline=False)
        embed.add_field(name='coinflip', value='.coinflip [heads or tails] [#]: Flip a coin to try and double your amt', inline=True)
        embed.add_field(name='roulette', value='.roulette [#] [Roulette Bets]: Use .help roulette for more info', inline=True)
        embed.add_field(name='slotmachine', value='.slots [#] [Optional: Autobet #]: Play a slot machine', inline=True)
        embed.add_field(name='stockgame', value='.stonks [#] [Time until pull out]: Put money into the stock market and pull out before a crash', inline=True)

        await ctx.send(embed=embed)

    else:
        await ctx.send('Invalid Command Sepcified')

# -------------------------------ERRORS-------------------------------------
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That is not a valid command')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required Arguments')
    elif isinstance(error, commands.CommandOnCooldown):
        if ctx.command.name == 'stockgame':
            await ctx.send(f'Please wait {round(error.retry_after)} seconds until you can use this command again')
        elif ctx.command.name == 'daily':
            await ctx.send(f'Please wait {round((error.retry_after / 60) / 60)} hours until you can use this command again')
        else:
            await ctx.send(f'Please wait {round(error.retry_after//60)} mins until you can use this command again')
    elif isinstance(error, asyncio.TimeoutError):
        await ctx.send(f'Time to confirm ran out')
# --------------------------------------------------------------------------

# ----------------------------------DEBUG-----------------------------------



# --------------------------------------------------------------------------

@client.command()
async def load(ctx, extension):
    if ctx.message.author.guild_permissions.administrator == True:
        client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    if ctx.message.author.guild_permissions.administrator == True:
        client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 332601646729134092 or ctx.author.id == 719976863593922590:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send('Done')
    else:
        await ctx.send('You dont have permission to do that')

for filename in os.listdir(r'./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run('Nzk0NzA5MDM3OTIwNDE5ODcx.X--wdw.lyJ13mrW3e5CldvmnTHM7KNt3QQ')
