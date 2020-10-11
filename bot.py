import discord

from dtoken import TOKEN

from discord.ext import commands

import discord

import datetime

bot = commands.Bot(command_prefix='*', description="Server stats bot")


@bot.event
async def on_ready():
    print('Logged in as')

    print(bot.user.name)

    print(bot.user.id)

    print('------')


@bot.event
async def on_message(message):
    await bot.process_commands(message)


@bot.command()
async def hey(ctx):
    await ctx.send("hey")


@bot.command()
async def daily(ctx):
    my_date = datetime.date.today()
    today = datetime.datetime(my_date.year, my_date.month, my_date.day)
    count = 0
    for channel in ctx.guild.text_channels:
        await ctx.send("Counting messages in " + str(channel))
        messages = await channel.history(after=today).flatten()
        count += len(messages)

    await ctx.send("This server has sent " + str(count) + " messages today.")


bot.run(TOKEN)
