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
    async with ctx.channel.typing():
        my_date = datetime.date.today()
        today = datetime.datetime(my_date.year, my_date.month, my_date.day)
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
        after = datetime.datetime(int(year), int(month), int(day))
        before = datetime.datetime(int(year), int(month), int(day) + 1)
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
    async with ctx.channel.typing():
        for day in days:
            date = datetime.date.today()
            after = datetime.datetime(date.year, date.month, date.day - day)
            before = datetime.datetime(date.year, date.month, date.day - day + 1)
            count = 0
            for channel in ctx.guild.text_channels:
                messages = await channel.history(after=after, before=before, limit=None).flatten()
                count += len(messages)

            await ctx.send("This server has sent " + str(count) + " messages on " + str(after))



bot.run(TOKEN)
