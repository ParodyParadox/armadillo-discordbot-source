import discord
from discord.ext import commands
import json
import os

class Utils(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):
        await ctx.send('yeah, im testing you too bud! watch out!')
        message = await ctx.send(f'{ctx.message.author}')
        print('worked')

    @commands.command()
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def changeStatus(self, ctx, *, desc):
        if ctx.message.author.guild_permissions.administrator:
            await self.client.change_presence(activity=discord.Game(name=desc), status=discord.Status.do_not_disturb)
            await ctx.send(f'Changed My Status to "{desc}"')

    @commands.command()
    async def returnid(self, ctx, member : discord.Member):
        await ctx.send(f'The id of {member.mention} is "{member.id}"')

    @commands.command()
    async def returnUser(self, ctx, id):
        user = await self.client.fetch_user(int(id))
        await ctx.send(user.name)

    @commands.command()
    async def resetAllMoney(self, ctx, cash, bank, password):
        if password == 'passcode':
            cash = int(cash)
            bank = int(bank)
            userids = []
            users = await get_bank_data()
            await ctx.channel.purge(limit=1)

            async for member in ctx.guild.fetch_members(limit=None):
                await open_account(member)
                userids.append(str(member.id))
            for user in userids:
                users[user]['wallet'] = cash
                users[user]['bank'] = bank

            await pushchange(users)

    @commands.command()
    async def cheatBalance(self, ctx, cash, bank, member : discord.Member):
        users = await get_bank_data()
        await open_account(member)
        user = str(member.id)
        users[user]['wallet'] = cash
        users[user]['bank'] = bank
        await pushchange(users)

async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 20
        users[str(user.id)]['bank'] = 50

    with open('mainbank.json', 'w') as f:
        json.dump(users,f)
    return True

async def get_bank_data():
    with open('mainbank.json', 'r') as f:
        users = json.load(f)
    return users

async def pushchange(users):
    with open('mainbank.json', 'w') as f:
        json.dump(users,f)

def setup(client):
    client.add_cog(Utils(client))
