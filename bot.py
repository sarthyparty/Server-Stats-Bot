from dtoken import TOKEN
from discord.ext import commands
import discord
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns

bot = commands.Bot(command_prefix='*', description="data graphing bot")
df = pd.read_csv('college_data.csv', index_col = 0)


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
async def grapheq(ctx, func):
    func = func.replace('^', '**')
    x_values = []
    y_values = []
    for i in range(0,100):
        x_values.append(i)
        y_values.append(eval(func.replace('x', str(i))))

    await ctx.send("Generating graph... ")
    plt.plot(x_values, y_values)
    plt.savefig(fname="graph")
    await ctx.send(ctx.author.mention, file=discord.File("graph.png"))
    os.remove("graph.png")
    plt.clf()


@bot.command()
async def listcols(ctx):
  await ctx.send(str(df.columns))

@bot.command()
async def listnumcols(ctx):
  await ctx.send(df.drop('Private', axis = 1).columns)

@bot.command()
async def head(ctx, column=None, num = 5):
  if column == None:
    await ctx.send(str(df.head(num)))
  elif column in df.columns:
    await ctx.send(df[column].head(num))
  else:
    await ctx.send("The column you specified is not in the dataframe")

@bot.command()
async def scatter(ctx):
  await ctx.send("Graphing scatterplot...")
  fig = plt.figure(figsize = (10,10))
  axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
  axes.scatter(df['Apps'], df['Enroll'])
  axes.set_xlabel("Apps Built")
  axes.set_ylabel("Enrolled Students")
  axes.set_title("Comparing the number of enrolled students per college to the the number of apps built")
  plt.savefig(fname="graph")
  await ctx.send(file=discord.File("graph.png"))
  os.remove("graph.png")
  plt.clf()

@bot.command()
async def distplot(ctx, column):
  if column in df.columns and column != "Private":
    await ctx.send("Graphing dist...")
    sns.distplot(df[column]) 
    plt.savefig(fname="graph")
    await ctx.send(file=discord.File("graph.png"))
    os.remove("graph.png")
    plt.clf()
  else:
    await ctx.send("The column was not in the dataframe or it was not a numerical column")

@bot.command()
async def catplot(ctx):
  plt.figure(figsize=(16,16))
  sns.catplot(x='Private',y='Enroll',data=df,kind='bar')
  plt.savefig(fname="graph")
  await ctx.send(file=discord.File("graph.png"))
  os.remove("graph.png")
  plt.clf()

@bot.command()
async def regression(ctx):
  plt.figure(figsize=(10,12))
  sns.lmplot(x='Accept', y='Outstate', data=df, hue='Private', palette='rainbow')
  plt.savefig(fname="graph")
  await ctx.send(file=discord.File("graph.png"))
  os.remove("graph.png")
  plt.clf()

# @bot.command()
# async def daily(ctx):
#     async with ctx.channel.typing():
#         my_date = datetime.date.today()
#         today = datetime.datetime(my_date.year, my_date.month, my_date.day)
#         count = 0
#         for channel in ctx.guild.text_channels:
#             await ctx.send("Counting messages in " + str(channel))
#             messages = await channel.history(after=today, limit=None).flatten()
#             count += len(messages)
#             await ctx.send(str(channel) + " has " + str(len(messages)) + " messages.")

#         await ctx.send("This server has sent " + str(count) + " messages today.")


# @bot.command()
# async def date(ctx, year, month, day):
#     ctx.send("WARNING! THIS MAY TAKE A VERY LONG TIME. Please be patient:)")
#     async with ctx.channel.typing():
#         after = datetime.datetime(int(year), int(month), int(day))
#         before = datetime.datetime(int(year), int(month), int(day) + 1)
#         count = 0
#         for channel in ctx.guild.text_channels:
#             await ctx.send("Counting messages in " + str(channel))
#             messages = await channel.history(after=after, before=before, limit=None).flatten()
#             count += len(messages)
#             await ctx.send(str(channel) + " has " + str(len(messages)) + " messages.")

#         await ctx.send("This server has sent " + str(count) + " messages on " + str(after))


# @bot.command()
# async def week(ctx):
#     await ctx.send("WARNING! THIS MAY TAKE A VERY LONG TIME!")
#     await ctx.send("You will be mentioned when the graph is generated:)")
#     days = [0, 1, 2, 3, 4, 5, 6]
#     dates = [None, None, None, None, None, None, None]
#     async with ctx.channel.typing():
#         for day in days:
#             date_ = datetime.date.today()
#             after = datetime.datetime(date_.year, date_.month, date_.day - day)
#             before = datetime.datetime(date_.year, date_.month, date_.day - day + 1)
#             count = 0
#             for channel in ctx.guild.text_channels:
#                 messages = await channel.history(after=after, before=before, limit=None).flatten()
#                 count += len(messages)
#             dates[day] = after.date()
#             days[day] = count

#     await ctx.send("Generating graph... ")
#     plt.plot(dates, days)
#     plt.savefig(fname="graph")
#     await ctx.send(file=discord.File("graph.png"))
#     await ctx.send(ctx.author.mention)
#     os.remove("graph.png")


# @bot.command()
# async def graph(ctx, Days):
#     await ctx.send("WARNING! THIS MAY TAKE A VERY LONG TIME!")
#     await ctx.send("You will be mentioned when the graph is generated:)")
#     days = []
#     dates = []

#     for i in range(0, int(Days)):
#         days.append(i)
#         dates.append(None)
#     async with ctx.channel.typing():
#         for day in days:
#             date_ = datetime.date.today()
#             after = datetime.datetime(date_.year, date_.month, date_.day - day)
#             before = datetime.datetime(date_.year, date_.month, date_.day - day + 1)
#             count = 0
#             for channel in ctx.guild.text_channels:
#                 messages = await channel.history(after=after, before=before, limit=None).flatten()
#                 count += len(messages)
#             dates[day] = after.date()
#             days[day] = count

#     await ctx.send("Generating graph... ")
#     plt.xticks([dates[0], dates[-1]], visible=True, rotation="horizontal")
    # plt.plot(dates, days)
    # plt.savefig(fname="graph")
    # await ctx.send(file=discord.File("graph.png"))
    # await ctx.send(ctx.author.mention)
    # os.remove("graph.png")


bot.run(TOKEN)
