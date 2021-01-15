import discord
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        #print('Starting Load...')
        await self.client.change_presence(activity=discord.Game(name='with rocks!'), status=discord.Status.do_not_disturb)
        print('Bot Is Ready and Online')

    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if member != self.client.user:
            if ctx.message.author.guild_permissions.kick_members == True:
                await member.kick(reason=reason)
                await ctx.send(f'{member.mention} was kicked')
            else:
                await ctx.send('Invalid Perms')
        else:
            await ctx.send('Im not going to kick myself!!')

    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if member != self.client.user:
            if ctx.message.author.guild_permissions.ban_members == True:
                await member.ban(reason=reason)
                await ctx.send(f'{member.mention} was banned')
            else:
                await ctx.send('Invalid Perms')
        else:
            await ctx.send('Im not going to ban myself!!')

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
              if ctx.message.author.guild_permissions.ban_members:
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
              else:
                await ctx.send('Invalid Perms')

def setup(client):
  client.add_cog(Admin(client))
