import discord
from discord.ext import commands
from discord import DMChannel
import json

from config import settings, settings_db
from mongo_db import insert_data, collection, get_data


intents = discord.Intents.all()
#intents.message_content = True

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)


@bot.event
async def on_ready():
    print('Bot runned')

@bot.event
async def on_message(ctx):
    channel = '👑get-the-title'
    if ctx.author != bot.user:
        author = ctx.author.id
        if ctx.content[0] != '/' and ctx.content[0] != '<':
            return 'pass message'
        else:
            if str(ctx.channel) == channel or str(ctx.channel.type) == 'private':
                if ctx.content[0] == '/':
                    if ctx.content == '/reg':
                        await ctx.reply('Check your direct messages')
                        embed_wallet = discord.Embed(color=0xff9900, 
                                                    title='Greetings!',
                                                    description='Send me your <TON-wallet adress> to authorize and claim your Title!\n**Example:**\n<EQD7y8d1ImET4WqHclpIJVED2WHKCXb4U3riNV6spyWmzuya>\n**ATTENTION!**\nWhen sending a wallet, please put these <angle brackets> at the beginning and end, as in the Example.')
                        embed_wallet.set_footer(text='Developed by Luc143r || Thanks 4 u')
                        user = await bot.fetch_user(author)
                        await DMChannel.send(user, embed=embed_wallet)
                    elif ctx.content == '/points':
                        try:
                            user = ctx.author
                            data_user = get_data(collection, {'username_ds': str(user)})
                            embed_statistic = discord.Embed(color=0xff9900,
                                                            title='Check your Title and points!',
                                                            description=f'**Wallet:** {data_user["wallet"]}\n**Title**: 0 - Heir\n**Points:** {data_user["points"]}')
                            embed_statistic.set_footer(text='Developed by Luc143r || Thanks 4 u')
                            await DMChannel.send(user, embed=embed_statistic)
                        except TypeError:
                            await DMChannel.send(user, 'To claim your Title, you need to authorize your wallet with /reg')
                elif ctx.content[0] == '<' and ctx.content[-1] == '>':
                    if str(ctx.channel.type) == 'private':
                        wallet = ctx.content.split('<')[1].split('>')[0]
                        if len(wallet) >= 48:
                            guild = bot.get_guild(986681170542608465)
                            role = discord.utils.get(guild.roles, name='0 - Heir')
                            member = guild.get_member(author)
                            data_ds = {
                                'wallet': f'{wallet}',
                                'username_ds': f'{member}',
                                'username_tg': '',
                                'points': 0,
                            }
                            if get_data(collection, {'wallet': data_ds['wallet']}):
                                if get_data(collection, {'wallet': data_ds['wallet']})['username_ds'] == '':
                                    await ctx.reply(f'Done')
                                    insert_data(collection, data_ds)
                            else:
                                await ctx.reply('Done🤫')
                                insert_data(collection, data_ds)
                            await member.add_roles(role)
                        else:
                            await ctx.reply('Wallet adress is not valid')
                    else:
                        await ctx.reply('Send your wallet to the bot in direct messages')

bot.run(settings['token'])