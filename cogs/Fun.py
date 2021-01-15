import discord
import random
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.fortune_responses = ['As I see it, yes.','Ask again later.','Better not tell you now.','Cannot predict now.','Concentrate and ask again.','Don’t count on it.','It is certain.','It is decidedly so.','Most likely.','My reply is no.','My sources say no.','Outlook not so good.','Outlook good.','Reply hazy, try again.','Signs point to yes.','Very doubtful.','Without a doubt.','Yes.','Yes – definitely.','You may rely on it.']
        self.mombot = False

    @commands.command(aliases=['8ball', 'fortune', 'eightball', 'answerme'])
    async def _8ball(self, ctx, *, question):
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(self.fortune_responses)}')

    @commands.command(aliases=['muteParents', 'MuteParents', 'muteparents', 'screwParents', 'ScrewParents', 'screwparents'])
    async def _muteParents(self, ctx):
        self.mombot = not self.mombot
        if self.mombot:
            await ctx.send('I will now delete Parent Bots messages :)')
        else:
            await ctx.send('I will no longer delete Parent Bots messages :(')

    @commands.command()
    async def say(self, ctx, *, msg):
        await ctx.channel.purge(limit=1)
        await ctx.send(msg)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.mombot:
            #if message.author != self.client.user:
            #    await message.channel.send(message.author)
            #    print(message.author.id)
            #    await message.channel.send(message.author.id == 605864767915294730)
            if message.author.id == 605864767915294730 or message.author.id == 503720029456695306:
                await message.channel.purge(limit=1)
                #await message.channel.send('Removed Parents Message :)')

def setup(client):
    client.add_cog(Fun(client))
