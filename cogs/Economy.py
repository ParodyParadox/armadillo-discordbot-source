import discord
import json
import os
import random
import time
from discord.ext import commands

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client
        #os.chdir(r'C:\Users\Zeak\github\armadillobot-discord')

    @commands.command(aliases=['bal'])
    async def balance(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        wallet_amt = users[str(user.id)]['wallet']
        bank_amt = users[str(user.id)]['bank']

        em = discord.Embed(title=f"{ctx.author.name}'s balance", color=discord.Color.red())
        em.add_field(name='Wallet', value=f'${wallet_amt}')
        em.add_field(name='Bank', value=f'${bank_amt}')
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,60*30, commands.BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        earnings = random.randint(25,200)
        await ctx.send(f'Someone gave you ${earnings} in cash!')

        users[str(user.id)]['wallet'] += earnings
        await pushchange(users)

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, input):
        user = ctx.author
        wallet = await get_wallet(user.id)
        if input == 'all':
            amt = int(wallet)
        else:
            amt = int(input)
        await open_account(user)
        users = await get_bank_data()

        if amt < 0:
            await ctx.send('You cant deposit a negitive number!!')
        elif (wallet - amt) >= 0:
            users[str(user.id)]['bank'] += amt
            users[str(user.id)]['wallet'] -= amt
            await pushchange(users)
            await ctx.send(f'Succesfully deposited ${amt}')
        else:
            await ctx.send('You dont have enough money in you wallet to do that!')

    @commands.command(aliases=['wit'])
    async def withdraw(self, ctx, input):
        user = ctx.author
        bank = await get_bank(user.id)
        if input == 'all':
            amt = int(bank)
        else:
            amt = int(input)
        await open_account(user)
        users = await get_bank_data()

        if amt < 0:
            await ctx.send('You cant withdraw a negitive number!!')
        elif (bank - amt) >= 0:
            users[str(user.id)]['wallet'] += amt
            users[str(user.id)]['bank'] -= amt
            await pushchange(users)
            await ctx.send(f'Succesfully withdrew ${amt}')
        else:
            await ctx.send('You dont have enough money in you bank account to do that!')

    @commands.command()
    async def beggersDream(self, ctx, amt, member : discord.Member):
        if ctx.author.id == 332601646729134092 or ctx.author.id == 719976863593922590:
            amt = int(amt)
            users = await get_bank_data()
            users[str(member.id)]['wallet'] += amt
            await pushchange(users)
            await ctx.send('Done')
            #await ctx.channel.purge(limit=1)
        else:
            await ctx.send('You dont have permission to do that')

    @commands.command()
    @commands.cooldown(1,60*30, commands.BucketType.user)
    async def steal(self, ctx, member : discord.Member):
        await open_account(ctx.author)
        users = await get_bank_data()
        user = ctx.author
        user_id = str(member.id)
        balance = await get_wallet(user_id)
        steal_amount = random.randint(75,100)

        if (balance - steal_amount) <=0:
            steal_amount = balance

        users[user_id]['wallet'] -= steal_amount
        users[str(user.id)]['wallet'] += steal_amount
        await pushchange(users)

        await ctx.send(f'{ctx.author.mention} just stole ${steal_amount} from {member.mention}!!')

    @commands.command()
    @commands.cooldown(1,60*30, commands.BucketType.user)
    async def heist(self, ctx, member : discord.Member):
        await open_account(ctx.author)
        users = await get_bank_data()
        steal_amount = random.randint(100,400)
        number = random.randint(1,3)
        bank_bal = await get_bank(member.id)
        user = await self.client.fetch_user(ctx.author.id)

        if (bank_bal - steal_amount) <= 0:
            steal_amount = bank_bal

        embed = discord.Embed(title=f'Try for heist against {member.name}', color=0x38761D, description=f'Steal from a users bank account!')
        embed.add_field(name='Amount To Steal:', value=f'${steal_amount}', inline=True)
        embed.add_field(name='From:', value=f'{member.mention}', inline=True)
        embed.add_field(name='Chances:', value='1/3 to succesfully heist', inline=False)
        await ctx.send(embed=embed)
        await ctx.send('Doing heist now . . . .')
        time.sleep(4)

        if number == 1:
            await ctx.send(f'SUCCESS! {ctx.author.mention} succesfully completed a heist for {steal_amount}, from {member.mention}!')
            users[str(ctx.author.id)]['wallet'] += steal_amount
            users[str(member.id)]['bank'] -= steal_amount
            await pushchange(users)
        else:
            await ctx.send(f'Sorry, you failed the heist')

    @commands.command()
    @commands.cooldown(1,3600, commands.BucketType.user)
    async def murder(self, ctx, member : discord.Member):
        await open_account(ctx.author)
        users = await get_bank_data()
        randnum = random.randint(0, 800)
        targetwallet = await get_wallet(member.id)
        targetbank = await get_bank(member.id)
        targettotal = targetbank + targetwallet
        if randnum == 1:
            users[str(ctx.author.id)]['bank'] += targettotal
            users[str(member.id)]['bank'] -= targetbank
            users[str(member.id)]['wallet'] -= targetwallet
            await pushchange(users)
            await ctx.send(f'{ctx.author.mention} JUST MURDERED {member.mention}!!!')
            await ctx.send(f"All of {member.mention}'s money is now {ctx.author.mention}'s!")
        else:
            await ctx.send(f'Sorry, looks like you failed. {member.mention}, {ctx.author.mention} just tried to kill you!!')

    @commands.command(aliases=['pay', 'give'])
    async def _pay(self, ctx, member : discord.Member, amount):
        amount = int(amount)
        user = ctx.author
        await open_account(user)
        users = await get_bank_data()
        bal = await get_wallet(user.id)

        if amount <=0:
            await ctx.send('Hey! I saw what you tried to do there!')
            amount = 0
        if bal < amount:
            if bal < 0:
                amount = 0
                bal = 0
            else:
                amount = bal
            await ctx.send(f'You dont have enough money to do that! Giving ${bal} instead...')

        users[str(user.id)]['wallet'] -= amount
        users[str(member.id)]['wallet'] += amount
        await pushchange(users)
        await ctx.send(f'{user.mention} gave {member.mention} ${amount}')

    @commands.command()
    @commands.cooldown(1,60, commands.BucketType.user)
    async def request(self, ctx, member : discord.Member, amount, *, reason="None given"):
        if member.id != self.client.user.id:
            await ctx.send(f'Message sent to {member.mention} requesting ${amount}')
            target = await self.client.fetch_user(member.id)
            requester = str(ctx.author.name)
            guildname = str(ctx.guild.name)
            embed = discord.Embed(title=f'Request from {requester}', color=0x38761D, description=f'{requester} has requested money from you in "{guildname}"')
            embed.add_field(name='Amount', value=f'${amount}', inline=True)
            embed.add_field(name='Reason', value=reason, inline=True)
            embed.add_field(name='Input this Command to Give Money:', value=f'.pay {ctx.author.mention} {amount}', inline=False)
            embed.set_thumbnail(url='https://icons.iconarchive.com/icons/paomedia/small-n-flat/1024/money-icon.png')
            await target.send(embed=embed)
        else:
            await ctx.send('Im not gonna give you any money!!')

    @commands.command()
    async def buypic(self, ctx):
        user = ctx.author
        await open_account(user)
        users = await get_bank_data()
        wallet = await get_wallet(user.id)
        rand = random.randint(1,22)
        url = './cogs/pics/{rand}.jpg'
        dm = await self.client.fetch_user(ctx.author.id)

        if wallet - 100 < 0:
            await ctx.send('Sorry, you need $100 in your wallet to buy an image!')
        else:
            await ctx.send('Just charged $100 to you account. The pic was sent to your dms')
            await dm.send(file=discord.File(r'./cogs/pics/{rand}.jpg'.format(rand=rand)))
            users[str(user.id)]['wallet'] -= 100
            await pushchange(users)

    @commands.command()
    @commands.cooldown(1,3600*24,commands.BucketType.user)
    async def daily(self, ctx):
        user = ctx.author
        await open_account(user)
        users = await get_bank_data()
        amt = 300

        users[str(user.id)]['wallet'] += amt
        await pushchange(users)

        await ctx.send(f'You received your ${amt} in cash for the day :)')


# ------GAMBLING--------------------------------------------------------------------------------------------------------------------------------------------------------

class Gambling(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['flip', 'coinFlip', 'CoinFlip', 'Flip'])
    async def coinflip(self, ctx, option, amt=20):
        if option == 'heads' or option == 'tails':
            await open_account(ctx.author)
            users = await get_bank_data()
            wallet = await get_wallet(ctx.author.id)
            amt = int(amt)
            randomnum = random.randint(0,1)

            if (wallet - amt) < 0:
                await ctx.send('You dont have enough money in your wallet for that bet!')
            else:
                if (randomnum == 0 and option == 'heads') or (randomnum == 1 and option == 'tails'):
                    winlose = f'You Won!!!, you just won ${amt}x2!'

                else:
                    winlose = f'You lost. You lost ${amt}'
                embed = discord.Embed(title=f'CoinFlip for {ctx.author.mention}', color=0x38761D, description='Heads or Tails?')
                embed.add_field(name='User Choice:', value=option, inline=True)
                embed.add_field(name='User Bet:', value='$' + str(amt), inline=True)
                embed.add_field(name='Win/Lose???', value=winlose, inline=False)
                await ctx.send(embed=embed)
                id = str(ctx.author.id)
                if winlose[4] == 'W':
                    users[id]['wallet'] += amt
                else:
                    users[id]['wallet'] -= amt
                await pushchange(users)
        else:
            await ctx.send('Please enter "heads" or "tails" into the command')

    @commands.command(aliases=['stocks', 'stock', 'market', 'stonk', 'stonks'])
    @commands.cooldown(3,60,commands.BucketType.user)
    async def stockgame(self, ctx, amt, time):
        time = int(time)
        amt = int(amt)
        #if amt > 500:
        #    await ctx.send('The max you can put into the market is $500')
        if time > 130:
            await ctx.send('Sorry, you can only trade for a max of 130 seconds')
        elif time < 2:
            await ctx.send('Sorry, you have to keep your money in the market for a minimum of 2 seconds')
        else:
            desc = 'Put your money into the market, wait a max of 10 seconds to type stop and take it out before the market crashes!'
            url = 'https://vmsseaglescall.org/wp-content/uploads/2019/10/251DF7B8-4172-4160-9684-95ED0A468177-475x284.jpeg'
            await open_account(ctx.author)
            users = await get_bank_data()
            user = ctx.author
            wallet = await get_wallet(user.id)
            message = ''
            interest = 0
            crashedQ = True

            timeOfCrash = random.randint(-100, 180)
            #timeOfCrash = -50
            if time >= timeOfCrash:
                crashQ = True
                message = 'The market crashed before you pulled out :('
            else:
                crashedQ = False
                message = 'The market didnt crash before you pulled out!'

            if time < 11:
                interest += round(random.uniform(0, 2), 2)
            elif time < 21:
                interest += round(random.uniform(1, 3), 2)
            elif time < 31:
                interest += round(random.uniform(2, 4), 2)
            elif time < 41:
                interest += round(random.uniform(3, 5), 2)
            elif time < 51:
                interest += round(random.uniform(4, 6), 2)
            elif time < 61:
                interest += round(random.uniform(5, 7), 2)
            elif time < 71:
                interest += round(random.uniform(6, 8), 2)
            elif time < 81:
                interest += round(random.uniform(7, 9), 2)
            elif time < 91:
                interest += round(random.uniform(8, 10), 2)
            elif time < 101:
                interest += round(random.uniform(9, 11), 2)
            elif time < 111:
                interest += round(random.uniform(10, 12), 2)
            elif time < 121:
                interest += round(random.uniform(11, 13), 2)
            elif time < 131:
                interest += round(random.uniform(12, 14), 2)

            if crashedQ == False:
                interest = interest/10
                totalAmt = amt + round((amt * interest))
                totalAmt = int(totalAmt)
                interestShow = round(interest * 100)
                #print(interest)
                #print(totalAmt)
            elif crashedQ == True and timeOfCrash < 0:
                interest = -(interest/10)
                totalAmt = round((amt * interest))
                totalAmt = int(totalAmt)
                interestShow = round(interest * 100)
                #print(interest)
                #print(totalAmt)
            else:
                totalAmt = 0

            if wallet - amt < 0:
                await ctx.send('You dont have enough money in your wallet to do that!')
            else:
                embed = discord.Embed(title='Stock Market Game!', description=desc, color=0x38761D)
                embed.add_field(name='Time Until Pull:', value=f'{time} seconds', inline=True)
                embed.add_field(name='Input Amount:', value=f'${amt}', inline=True)
                embed.add_field(name='Result:', value=message)
                embed.add_field(name='Interest Gained:', value=f'{interestShow}%')
                embed.add_field(name='Total Earnings:', value=f'${totalAmt - amt}')
                embed.set_image(url=url)
                await ctx.send(embed=embed)

                users[str(user.id)]['wallet'] -= amt
                users[str(user.id)]['wallet'] += round(totalAmt)
                await pushchange(users)


    @commands.command(aliases=['slots', 'slot'])
    async def slotmachine(self, ctx, amt=10, times=1):
        amt = int(amt)
        if amt < 10:
            await ctx.send('The minimum bet is $10')
        else:
            user = ctx.author
            await open_account(user)
            users = await get_bank_data()
            wallet = await get_wallet(user.id)
            x = 0

            if (wallet - amt) < 0:
                await ctx.send('You dont have enough $$ in your wallet to do that!')
            elif amt == 0:
                await ctx.send('You cant bet $0 silly!')
            elif amt > 250:
                await ctx.send('Sorry, $250 is the max amt to bet')
            else:
                if times > 3:
                    await ctx.send('You can only auto bet up to 3 times!')
                    await ctx.send('Set auto bet to 3')
                    times = 3
                elif times <= 0:
                    await ctx.send('You cant bet 0 times!!')
                    times = 1

                while x < times:
                    #extra hard
                    #slotimgs = ['🟥','🟩','🟦','🏆','🟨','🟧','🟪']
                    slotimgs = ['🟥','🟩','🟦','🏆','🟨','🟧']
                    slotpicarr = []
                    slotnum = []
                    slotpic = ''
                    winnum = 0
                    trophy = 0
                    trophytemp = 0
                    tempnum = 0
                    winAmt = 0

                    count = 0
                    while (count < 5):
                        #for extra hard
                        #rand = random.randint(0,6)
                        rand = random.randint(0,5)
                        slotpicarr.append(slotimgs[rand])
                        slotpic = ' '.join(slotpicarr)
                        slotnum.append(rand)
                        count += 1

                    for num in slotnum:
                        for num2 in slotnum:
                            if num == num2:
                                if num == 3:
                                    trophytemp += 1
                                else:
                                    tempnum += 1
                        if tempnum > winnum:
                            winnum = tempnum
                        elif trophytemp > trophy:
                            trophy = trophytemp
                        tempnum = 0
                        trophytemp = 0

                    if winnum == 3:
                        winAmt += amt * 4
                    elif winnum == 4:
                        winAmt += amt * 5
                    elif winnum == 5:
                        winAmt += 1000
                    elif trophy == 3:
                        winAmt += amt * 6
                    elif trophy == 4:
                        winAmt += amt * 10
                    elif trophy == 5:
                        winAmt += 5000
                    else:
                        winAmt += 0


                    embed = discord.Embed(title='Slot Machine Game', color=0x38761D, description='Play a slot machine to get money!')
                    embed.add_field(name='Slot:', value=slotpic, inline=False)
                    embed.add_field(name='Amount Input:', value=f'${amt}', inline=True)
                    embed.add_field(name='Amount Won:', value=f'${winAmt}', inline=True)
                    embed.set_thumbnail(url='https://www.grapevinebirmingham.com/wp-content/uploads/2020/06/Slot-Machine.jpg')
                    await ctx.send(embed=embed)

                    if winAmt == 0:
                        users[str(user.id)]['wallet'] -= amt
                    else:
                        users[str(user.id)]['wallet'] -= amt
                        users[str(user.id)]['wallet'] += winAmt

                    await pushchange(users)
                    x += 1



    @commands.command()
    async def roulette(self, ctx, amt, *, args):
        amt = int(amt)
        winAmt = 0
        options = args.split()
        wheelColor = ''
        user = ctx.author
        await open_account(user)
        users = await get_bank_data()
        wallet = await get_wallet(user.id)
        invalid = False

        wheelNumber = random.randint(0, 36)

        if (random.randint(0,1) == 0):
            wheelColor = 'black'
        else:
            wheelColor = 'red'

        for option in options:
            # Specific Number
            if option.isdigit():
                value = int(option)
                if value == wheelNumber:
                    winAmt = amt * 5
            else:
                # Color
                if option == 'black':
                    if option == wheelColor:
                        winAmt = amt*2
                elif option == 'red':
                    if option == wheelColor:
                        winAmt = amt*2
                # Even or Odd
                elif option == 'even':
                    if wheelNumber % 2 == 0:
                        winAmt = amt*2
                elif option == 'odd':
                    if wheelNumber % 2 == 1:
                        winAmt = amt *2
                # Range stuff
                elif option == '1-12':
                    for i in range(1,13):
                        if i == wheelNumber:
                            winAmt = amt * 2.5
                elif option == '13-24':
                    for i in range(13,25):
                        if i == wheelNumber:
                            winAmt = amt * 2.5
                elif option == '25-36':
                    for i in range(25,37):
                        if i == wheelNumber:
                            winAmt = amt *2.5
                elif option == '1-18':
                    for i in range(1,19):
                        if i == wheelNumber:
                            winAmt = amt * 2
                elif option == '19-36':
                    for i in range(19,37):
                        if i == wheelNumber:
                            winAmt = amt * 2
                # Row Select
                elif option == 'row1' or option == 'c1':
                    for i in range(1,37,3):
                        if i == wheelNumber:
                            winAmt = amt * 2.5
                elif option == 'row2' or option == 'c2':
                    for i in range(2,37,3):
                        if i == wheelNumber:
                            winAmt = amt * 2.5
                elif option == 'row3' or option == 'c3':
                    for i in range(3,37,3):
                        if i == wheelNumber:
                            winAmt = amt * 2.5
                else:
                    await ctx.send('You have an invalid option set')
                    invalid = True

        if not invalid:
            totalAmt = amt * (len(options))
            if wallet - totalAmt < 0:
                await ctx.send('You dont have enough $$ in your wallet to spin!')
                await ctx.send(f'You tried to bet: ${totalAmt}.')
            else:
                embed = discord.Embed(title='Roulette!', color=0x38761D, description='Use [.help roulette] for more info on roulette')
                embed.add_field(name='Bet amount:', value=f'${amt}', inline=True)
                embed.add_field(name='Bets:', value=f'{", ".join(options)}', inline=True)
                embed.add_field(name='Wheel Selected:', value=f'{wheelColor} {wheelNumber}')
                embed.add_field(name='You Won:', value=f'${winAmt}')
                embed.set_image(url='https://www.stormforgeproductions.com/wp-content/uploads/roulette-board.jpg')
                await ctx.send(embed=embed)

                if winAmt == 0:
                    users[str(user.id)]['wallet'] -= totalAmt
                else:
                    users[str(user.id)]['wallet'] -= totalAmt
                    users[str(user.id)]['wallet'] += winAmt

                await pushchange(users)

    @commands.command(aliases=['leaderboard', 'rank', 'board', 'ranks'])
    @commands.cooldown(1,60*7,commands.BucketType.default)
    async def leaderBoard(self, ctx):
        await ctx.send('It will take around a min for the output of the command')
        users = await get_bank_data()
        first = {'name':'NA', 'wallet':0, 'bank':0, 'total':0}
        second = {'name':'NA', 'wallet':0, 'bank':0, 'total':0}
        third = {'name':'NA', 'wallet':0, 'bank':0, 'total':0}
        fourth = {'name':'NA', 'wallet':0, 'bank':0, 'total':0}
        for user in users:
            member = await self.client.fetch_user(int(user))
            wallet = users[user]['wallet']
            bank = users[user]['bank']
            total = wallet + bank

            if total > first['total']:
                first['name'] = str(member)
                first['bank'] = bank
                first['wallet'] = wallet
                first['total'] = total
                continue
            elif total > second['total']:
                second['name'] = str(member)
                second['bank'] = bank
                second['wallet'] = wallet
                second['total'] = total
                continue
            elif total > third['total']:
                third['name'] = str(member)
                third['bank'] = bank
                third['wallet'] = wallet
                third['total'] = total
                continue
            elif total > fourth['total']:
                fourth['name'] = str(member)
                fourth['bank'] = bank
                fourth['wallet'] = wallet
                fourth['total'] = total
                continue
            else:
                continue

        embed = discord.Embed(title='Economy Leaderboard', color=0xedaddc, description='The current money ranking across ALL servers')
        #first place
        embed.add_field(name='First Place:', value='--Most Total Money--', inline=False)
        embed.add_field(name=f'-----{first["name"]}', value=f'Wallet: ${first["wallet"]}, Bank: ${first["bank"]}, Total: ${first["total"]}')
        #second place
        embed.add_field(name='Second Place:', value='--Second Most Total Money--',inline=False)
        embed.add_field(name=f'------{second["name"]}', value=f'Wallet: ${second["wallet"]}, Bank: ${second["bank"]}, Total: ${second["total"]}')
        #third place
        embed.add_field(name='Third Place:', value='--Third Most Total Money--',inline=False)
        embed.add_field(name=f'-----{third["name"]}', value=f'Wallet: ${third["wallet"]}, Bank: ${third["bank"]}, Total: ${third["total"]}')
        #runner up
        embed.add_field(name='Runner Up:', value='--Runner Up To 3rd--',inline=False)
        embed.add_field(name=f'-----{fourth["name"]}', value=f'Wallet: ${fourth["wallet"]}, Bank: ${fourth["bank"]}, Total: ${fourth["total"]}')
        await ctx.send(embed=embed)



# ------END-------------------------------------------------------------------------------------------------------------------------------------------------------------

def setup(client):
    client.add_cog(Economy(client))
    client.add_cog(Gambling(client))

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

async def get_wallet(id):
    bal = await get_bank_data()
    value = bal[str(id)]['wallet']
    return value

async def get_bank(id):
    bal = await get_bank_data()
    value = bal[str(id)]['bank']
    return value
