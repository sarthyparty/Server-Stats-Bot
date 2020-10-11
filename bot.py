import discord

from dtoken import TOKEN

from discord.ext import commands

import discord

import datetime

import pytz

import matplotlib.pyplot as plt

import os

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
    async with ctx.channel.typing():
        my_date = datetime.date.today()
        today = datetime.datetime(my_date.year, my_date.month, my_date.day,0,0,0,0,pytz.timezone("CET"))
        count = 0
        for channel in ctx.guild.text_channels:
            await ctx.send("Counting messages in " + str(channel))
            messages = await channel.history(after=today, limit=None).flatten()
            count += len(messages)
            await ctx.send(str(channel) + " has " + str(len(messages)) + " messages.")

        await ctx.send("This server has sent " + str(count) + " messages today.")


@bot.command()
async def date(ctx, year, month, day):
    ctx.send("WARNING! THIS MAY TAKE A VERY LONG TIME. Please be patient:)")
    async with ctx.channel.typing():
        after = datetime.datetime(int(year), int(month), int(day),0,0,0,0,pytz.timezone("CET"))
        before = datetime.datetime(int(year), int(month), int(day) + 1,0,0,0,0,pytz.timezone("CET"))
        count = 0
        for channel in ctx.guild.text_channels:
            await ctx.send("Counting messages in " + str(channel))
            messages = await channel.history(after=after, before=before, limit=None).flatten()
            count += len(messages)
            await ctx.send(str(channel) + " has " + str(len(messages)) + " messages.")

        await ctx.send("This server has sent " + str(count) + " messages on " + str(after))

@bot.command()
async def week(ctx):
    days = [0,1,2,3,4,5,6]
    dates = [None,None,None,None,None,None,None]
    async with ctx.channel.typing():
        for day in days:
            date_ = datetime.date.today()
            after = datetime.datetime(date_.year, date_.month, date_.day - day)
            before = datetime.datetime(date_.year, date_.month, date_.day - day + 1)
            count = 0
            for channel in ctx.guild.text_channels:
                messages = await channel.history(after=after, before=before, limit=None).flatten()
                count += len(messages)
            dates[day] = after.date()
            day = count
            await ctx.send("This server has sent " + str(count) + " messages on " + str(after))

    await ctx.send("Generating graph... ")
    plt.plot(dates, days)
    plt.save("graph.png")
    await ctx.send(file=discord.File("graph.png"))
    os.remove("graph.png")



bot.run(TOKEN)
