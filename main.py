from utils import get_channel
from utils import get_emoji
import discord
import os
from random import randint
from discord.ext.commands import Bot
from discord.ext.commands import MemberConverter
from datetime import datetime
import aiohttp
import json
import asyncio
import math
# from discord import FFmpegPCMAudio
# from youtube_dl import YoutubeDL
# from discord.utils import get
import requests
import string
# import chat_exporter
# from discord.ext import commands
# import io
from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

intents = discord.Intents.default()
intents.members = True

converter = MemberConverter()
bot = Bot(command_prefix='s.', intents=intents)
TOKEN = os.getenv("TOKEN")

@bot.event
async def on_ready():
    print("Setting NP game", flush=True)
    await bot.change_presence(activity=discord.Game(name="with 1-methyl-3-butanone"))
    print(f"Logged in as {bot.user.name}!", flush=True)
    print(f'{bot.user.name} has connected to Discord!')
    DiscordComponents(bot)  
    # .init_exporter(bot)

@bot.command(name='pfp', help="Displays a profile picture (syntax: !pfp <mention>")
async def pfp(ctx, mention="None"):
  print(f"{ctx.author.name}: {'s!pfp'} "+ str(mention))
  if(mention == "None"):
	  await ctx.send(f'{ctx.author.avatar_url}')
  else:
    try:
      member = await converter.convert(ctx, mention)
    except discord.ext.commands.errors.MemberNotFound as err:
      await ctx.send(f'{err}')
      return 0
    #member = await converter.convert(ctx, mention)
    await ctx.send(f'{member.avatar_url}')

@bot.command(name='info', help="Displays information about this bot")
async def info(ctx, *params): 

  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!info'} "+ str(param))

  embed = discord.Embed(title="Bot Info", timestamp=datetime.utcnow(), color=0x00ff00)
  embed.add_field(name="Creator", value="Made by Max49#9833", inline=False)
  embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/427832149173862400/1767e28d50d41fab9872c7137020df9c.webp?size=1024")
  await ctx.send(embed=embed)
  await ctx.channel.send(
        "Click the button below to visit my website!",
        components=[
            Button(style=ButtonStyle.URL, label="Visit Max's Website!", url="https://www.max49.cf/"),
        ],
    )

@bot.command(name='chat', help="gives you the ability to chat with the bot")
async def chat(ctx, *params):

  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!chat'} "+ str(param))

  if(len(params) == 1):
    msg = params[0]
    await ctx.send(msg)
    await ctx.message.delete()
  else:
    if(str(params[0][0]) == "<"):
      msg = ""
      total_params = params[1:]
      for thing in total_params:
        msg += (str(thing) + " ")
      chan = params[0]
      numbers = ["0","1","2","3","4","5","6","7","8","9"] 
      total_id = ""
      for character in chan:
        if character in numbers:
          total_id += character
      total_num_id = int(total_id)
      for channel in ctx.guild.channels:
        if(int(channel.id) == int(total_num_id)):
            wanted_channel_name = channel.name
            chan = get_channel(bot, wanted_channel_name)
            await chan.send(msg)
            await ctx.message.delete()
    else:
      msg = ""
      for thing in params:
        msg += (str(thing) + " ")
      await ctx.send(msg)
      await ctx.message.delete()
    
@bot.command(name='clear', help="clears screen (admin only)")
async def clear(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!clear'} "+ str(param))
  if ctx.author.guild_permissions.administrator:
    msg = "_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n_ _\n"
    await ctx.send(msg)

@bot.command(name='lab', help="see the latest posted assignment")
async def input(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!lab'} "+ str(param))
  with open('recent_url.json') as f:
    urls = json.load(f)
  url = urls[0]["url"]
  if(ctx.author.id == 427832149173862400 or ctx.author.id == 293416817408475136):
    try:
      attachment_url = ctx.message.attachments[0].url
      def check(msg):
        return msg.author == ctx.author and msg.channel == msg.channel 
      await ctx.send("What is the name of this file?")
      msg = await bot.wait_for("message", check=check)
      await ctx.send(f"{msg.content} is now the file that shows up when you run s!lab")
      urls[0]['name'] = msg.content
      urls[0]['url'] = attachment_url
      with open('recent_url.json', 'w') as json_file:
        json.dump(urls, json_file)
    except IndexError:
      await ctx.send(f"Here is a link to the latest assignment: **{urls[0]['name']}** - {url} (if you wanted to upload a document, attach it when you run the command)")
  else:
    await ctx.send(f"Here is a link to the latest assignment: **{urls[0]['name']}** - {url}")

@bot.command(name='gif', help="sends a random gif (syntax: s!gif <search>")
async def gif(ctx, *search):
  param = ""
  for thing in search:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!gif'} "+ str(param))
  search_term = ""
  for thing in search:
    search_term += (str(thing) + " ")
  api_key = os.getenv('GIPHY_KEY')
  async def search_gifs(query):
    session = aiohttp.ClientSession()
    response = await session.get(f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={query}&limit=50&offset=0")
    data = json.loads(await response.text())
    gif_choice = randint(0, 30)
    gif_url = data['data'][gif_choice]['images']['original']['url']
    await session.close()
    return gif_url 
  gif = await search_gifs(search_term)
  await ctx.send(gif)

@bot.command(name='pingtyler', help="pings tyler")
async def pingtyler(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!pingtyler'} "+ str(param))
  msg = "<@293416817408475136>"
  await ctx.send(msg)

@bot.command(name='spampingtyler', help="pings tyler")
async def spampingtyler(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!spampingtyler'} "+ str(param))
  msg = "<@293416817408475136>"
  for i in range(7):
    await ctx.send(msg)

@bot.command(name='smurf', help="tells you if you're smurfing")
async def smurf(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!smurf'} "+ str(param))
  await ctx.send(f"{ctx.author.mention}, you're smurfing!")

@bot.command(name='profile', help="displays your profile")
async def profile(ctx, profile="none"):
  if profile == "none":
    param = ""
  else:
    param = profile
  print(f"{ctx.author.name}: {'s!profile'} "+ str(param))
  with open('profiles.json') as f:
      profile_data = json.load(f)
  if(profile != "none"):
    uid = profile
    try:
      uid = int(uid)
    except ValueError:
      uid = profile
  else:
    uid = ctx.author.id
  found = 0
  found_indices = []
  for i in range(len(profile_data)):
    user_mention = f"<@!{profile_data[i]['ID']}>"
    if(profile_data[i]['ID'] == uid or profile_data[i]['Name'] == uid or profile_data[i]['Nick'] == uid or profile_data[i]['Tag'] == uid or user_mention == uid):
      embedVar = discord.Embed(title=f"{profile_data[i]['Name']}'s profile",  timestamp=datetime.utcnow(), color=0x00ff00)
      try:
        percent_correct = (profile_data[i]['Correct']/profile_data[i]['Total']) * 100
      except ZeroDivisionError:
        percent_correct = 0
      try:
        percent_world_correct = (profile_data[i]['WorldCorrect']/profile_data[i]['WorldTotal']) * 100
      except ZeroDivisionError:
        percent_world_correct = 0  
      embedVar.add_field(name="Chemistry Regents Review Stats", value=f"{str(profile_data[i]['Correct'])}/{str(profile_data[i]['Total'])} ({str(round(percent_correct, 2))}%)", inline=False)
      embedVar.add_field(name="AP World Review Stats", value=f"{str(profile_data[i]['WorldCorrect'])}/{str(profile_data[i]['WorldTotal'])} ({str(round(percent_world_correct, 2))}%)", inline=False)
      embedVar.add_field(name="Balance", value=f"{profile_data[i]['Balance']} schlucks", inline=False)
      embedVar.set_thumbnail(url=profile_data[i]['Avatar URL'])
      await ctx.send(embed=embedVar)
      found = 1
      found_indices.append(i)
  if(found == 0):
    isSameUser = 0
    for i in range(len(profile_data)):
      if(profile_data[i]['ID'] == ctx.author.id):
        await ctx.send("Looks like this user does not have a profile. Ask them to create one with `s!profile`!")
        isSameUser = 1
        break
    if(isSameUser == 0):
      profile_data.append({"Name": ctx.author.name, "Tag": str(ctx.author), "Nick": ctx.author.display_name, "ID": ctx.author.id, "Avatar URL": str(ctx.author.avatar_url),"Correct": 0, "Total": 0, "Calc": "True","Table": "True","WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1})
      embedVar = discord.Embed(title=f"{ctx.author.name}'s profile",  timestamp=datetime.utcnow(), color=0x00ff00)
      try:
        percent_correct = (profile_data[i]['Correct']/profile_data[i]['Total']) * 100 
      except ZeroDivisionError:
        percent_correct = 0
      embedVar.add_field(name="Chemistry Regents Review Stats", value=f"{str(profile_data[i]['Correct'])}/{str(profile_data[i]['Total'])} ({str(round(percent_correct, 2))}%)", inline=False)
      embedVar.add_field(name="AP World Review Stats", value=f"{str(profile_data[i]['WorldCorrect'])}/{str(profile_data[i]['WorldTotal'])} ({str(round(percent_world_correct, 2))}%)", inline=False)
      embedVar.set_thumbnail(url=profile_data[i]['Avatar URL'])
      await ctx.send(embed=embedVar)
  try:
    print(found_indices[1])
    profile_data.pop(found_indices[1])
  except IndexError:
    var = 1
  with open('profiles.json', 'w') as json_file:
    json.dump(profile_data, json_file)

@bot.command(name='regents', help="dispenses a Random regents question (syntax: s!regents (<atom>, <periodic>, <matter>, <solubility>")
async def regents(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!regents'} "+ str(param))
  found = 0
  with open('profiles.json') as f:
    profile_data = json.load(f)
  found_indices = []
  for i in range(len(profile_data)):
    if(profile_data[i]['ID'] == ctx.author.id):
      found = 1
      found_indices.append(i)
  if(found == 0):
    profile_data.append({"Name": ctx.author.name, "Tag": str(ctx.author), "Nick": ctx.author.display_name, "ID": ctx.author.id, "Avatar URL": str(ctx.author.avatar_url),"Correct": 0, "Total": 0, "Calc": "True","Table": "True","WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1})
    for i in range(len(profile_data)):
      if(profile_data[i]['ID'] == ctx.author.id):
        found = 1
        found_indices.append(i)
  i_value = found_indices[0]
  try:
    category_choice = params[0]
    if(category_choice.lower() == "matter"):
      category = "Matter"
      with open('questions/matter.json') as f:
        questions = json.load(f)
      if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
        question_number = int(randint(0, len(questions)-1))
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          elif questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          else:
            break
    elif(category_choice.lower() == "atom"):
      category = "Atomic Structure"
      with open('questions/atom.json') as f:
        questions = json.load(f)
      if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
        question_number = int(randint(0, len(questions)-1))
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          elif questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          else:
            break
    elif(category_choice.lower() == "periodic"):
      category = "Periodic Table"
      with open('questions/periodic.json') as f:
        questions = json.load(f)
      if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
        question_number = int(randint(0, len(questions)-1))
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          elif questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          else:
            break
    elif(category_choice.lower() == "solubility"):
      category = "Solubility"
      with open('questions/solubility.json') as f:
        questions = json.load(f)
      if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
        question_number = int(randint(0, len(questions)-1))
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          elif questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          else:
            break
    elif(category_choice.lower() == "kinetics"):
      category = "Kinetics"
      with open('questions/kinetics.json') as f:
        questions = json.load(f)
      if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
        question_number = int(randint(0, len(questions)-1))
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          elif questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          else:
            break
    else:
      await ctx.send("Invalid Category. Choosing random category.")
      category_number = int(randint(0, 4))
      if(category_number == 0):
        category = "Matter"
        with open('questions/matter.json') as f:
          questions = json.load(f)
        if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
          question_number = int(randint(0, len(questions)-1))
        elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Calc"] == "True":
              questions.pop(i)
              continue
            elif questions[question_number]["Table"] == "True":
              questions.pop(i)
              continue
            else:
              break
        elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Table"] == "True":
              questions.pop(i)
              continue
            else:
              break
        elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Calc"] == "True":
              questions.pop(i)
              continue
            else:
              break
      elif(category_number == 2):
        category = "Periodic Table"
        with open('questions/periodic.json') as f:
          questions = json.load(f)
        if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
          question_number = int(randint(0, len(questions)-1))
        elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Calc"] == "True":
              questions.pop(i)
              continue
            elif questions[question_number]["Table"] == "True":
              questions.pop(i)
              continue
            else:
              break
        elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Table"] == "True":
              questions.pop(i)
              continue
            else:
              break
        elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Calc"] == "True":
              questions.pop(i)
              continue
            else:
              break
      elif(category_number == 3):
        category = "Solubility"
        with open('questions/solubility.json') as f:
          questions = json.load(f)
        if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
          question_number = int(randint(0, len(questions)-1))
        elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Calc"] == "True":
              questions.pop(i)
              continue
            elif questions[question_number]["Table"] == "True":
              questions.pop(i)
              continue
            else:
              break
        elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Table"] == "True":
              questions.pop(i)
              continue
            else:
              break
        elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Calc"] == "True":
              questions.pop(i)
              continue
            else:
              break
      elif(category_number == 4):
        category = "Kinetics"
        with open('questions/kinetics.json') as f:
          questions = json.load(f)
        if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
          question_number = int(randint(0, len(questions)-1))
        elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Calc"] == "True":
              questions.pop(i)
              continue
            elif questions[question_number]["Table"] == "True":
              questions.pop(i)
              continue
            else:
              break
        elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Table"] == "True":
              questions.pop(i)
              continue
            else:
              break
        elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
          while True:
            question_number = int(randint(0, len(questions)-1))
            if questions[question_number]["Calc"] == "True":
              questions.pop(i)
              continue
            else:
              break
        
  except IndexError:
    category_number = int(randint(0, 4))
    if(category_number == 0):
      category = "Matter"
      with open('questions/matter.json') as f:
        questions = json.load(f)
      if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
          question_number = int(randint(0, len(questions)-1))
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          elif questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          else:
            break
    elif(category_number == 1):
      category = "Atomic Structure"
      with open('questions/atom.json') as f:
        questions = json.load(f)
      if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
          question_number = int(randint(0, len(questions)-1))
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          elif questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          else:
            break
    elif(category_number == 2):
      category = "Periodic Table"
      with open('questions/periodic.json') as f:
        questions = json.load(f)
      if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
          question_number = int(randint(0, len(questions)-1))
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          elif questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          else:
            break
    elif(category_number == 3):
      category = "Solubility"
      with open('questions/solubility.json') as f:
        questions = json.load(f)
      if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
          question_number = int(randint(0, len(questions)-1))
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          elif questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          else:
            break
    elif(category_number == 4):
      category = "Kinetics"
      with open('questions/kinetics.json') as f:
        questions = json.load(f)
      if(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "True"):
          question_number = int(randint(0, len(questions)-1))
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          elif questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "True" and profile_data[i_value]["Table"] == "False"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Table"] == "True":
            questions.pop(i)
            continue
          else:
            break
      elif(profile_data[i_value]["Calc"] == "False" and profile_data[i_value]["Table"] == "True"):
        while True:
          question_number = int(randint(0, len(questions)-1))
          if questions[question_number]["Calc"] == "True":
            questions.pop(i)
            continue
          else:
            break

  embedVar = discord.Embed(title="Question #" + str(question_number + 1), timestamp=datetime.utcnow(), color=0x00ff00)

  if(questions[question_number]['image'] != 0):
    embedVar.set_image(url=questions[question_number]['image'])
  
  embedVar.add_field(name=questions[question_number]['question'], value="a) " + str(questions[question_number]['choices'][0]) + "\nb) " + str(questions[question_number]['choices'][1]) + "\nc) " + str(questions[question_number]['choices'][2]) + "\nd) " + str(questions[question_number]['choices'][3]), inline=False)

  if(questions[question_number]['Calc'] == "True"):
    if(questions[question_number]['Table'] == "True"):
      embedVar.add_field(name="Tools required", value="Calculator and Reference Table", inline=False)
    elif(questions[question_number]['Table'] == "False"):
      embedVar.add_field(name="Tools required", value="Calculator", inline=False)
  elif(questions[question_number]['Table'] == "True"):
    if(questions[question_number]['Calc'] == "True"):
      embedVar.add_field(name="Tools required", value="Calculator and Reference Table", inline=False)
    elif(questions[question_number]['Calc'] == "False"):
      embedVar.add_field(name="Tools required", value="Reference Table", inline=False)
    
  embedVar.add_field(name="Category", value="`"+str(category)+"`", inline=False)

  await ctx.reply(embed=embedVar)

  def check(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower() in ["a", "b", "c", "d"]
  try:
    msg = await bot.wait_for("message", check=check, timeout=90)
  except asyncio.TimeoutError:
    await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
    for i in range(len(profile_data)):
        if(profile_data[i]['ID'] == ctx.author.id):
          profile_data[i]['Total'] += 1
  if msg.content.lower() == questions[question_number]['answer']:
      for i in range(len(profile_data)):
        if(profile_data[i]['ID'] == ctx.author.id):
          profile_data[i]['Correct'] += 1
          profile_data[i]['Total'] += 1
      await msg.reply("Correct!")
  else:
      for i in range(len(profile_data)):
        if(profile_data[i]['ID'] == ctx.author.id):
          profile_data[i]['Total'] += 1
      await msg.reply(f"Incorrect Answer. The correct answer was `{questions[question_number]['answer']}`.\nYou should probably review the `{category}` unit.")
  with open('profiles.json', 'w') as json_file:
    json.dump(profile_data, json_file)

@bot.command(name="quiz", help="tells you your quiz score!")
async def quiz(ctx, score=100):
  print(f"{ctx.author.name}: {'s!quiz'} "+ str(score))
  upper_bound = score
  if(upper_bound >= 20):
    max_score = int(upper_bound) + 3
  else:
    max_score = int(upper_bound)
  if(upper_bound < 0):
    score = randint(upper_bound, 0)
  else:
    score = randint(0, int(max_score))
  #if(upper_bound <= 0 or upper_bound > 200):
  #  msg = f"{ctx.author.mention}, why would anyone ever make a quiz out of that score..."
  if(score == 0):
    additional_message = "bruh"
    msg = f"{ctx.author.mention}, you got a {score} out of {upper_bound} on the quiz. {additional_message}"
  elif(upper_bound == 100 and score < 5):
    additional_message = "how... did you manage to get a score that low?? I mean even guessing on the multiple choice would have gotten you a higher score than this. wow I'm actually surprised someone's actually this bad at chemistry. Did you sleep through this entire unit? Did you forget to do half the test??? I'm baffled."
    msg = f"{ctx.author.mention}, you got a {score} out of {upper_bound} on the quiz. {additional_message}"
  elif(score == 69):
      additional_message = "nice :ok_hand:"
      msg = f"{ctx.author.mention}, you got a {score} out of {upper_bound} on the quiz. {additional_message}"
  elif(score < upper_bound):
      with open('quiz_reasons.json') as f:
        reasons = json.load(f)
      fail_reason = randint(0,len(reasons)-1)
      if(upper_bound - score <= 75):
        additional_message = "You got points off for " + str(reasons[fail_reason]) + "."
      elif(upper_bound - score >= 76):
        additional_message = "You got points off for " + str(reasons[fail_reason]) + ", "
        fail_reason = randint(0,len(reasons)-1)
        additional_message += str(reasons[fail_reason]) + ", and "
        fail_reason = randint(0,len(reasons)-1)
        additional_message += str(reasons[fail_reason]) + "."
      if(upper_bound == 100 and score < 65):
        additional_message += " You failed the test. Good job."
      msg = f"{ctx.author.mention}, you got a {score} out of {upper_bound} on the quiz. {additional_message}"
  elif(score == upper_bound):
      additional_message = "You got a perfect score!"
      msg = f"{ctx.author.mention}, you got a {score} out of {upper_bound} on the quiz. {additional_message}"
  elif(score > upper_bound):
      additional_message = "Schlooth has bestowed extra points upon you! You smurfed!"
      msg = f"{ctx.author.mention}, you got a {score} out of {upper_bound} on the quiz. {additional_message}"

  await ctx.send(msg)

@bot.command(name="addquiz", help="adds a quiz reason", aliases=['quizadd'])
async def add_reason(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!addquiz'} "+ str(param))
  with open('quiz_reasons.json') as f:
      quiz_reasons = json.load(f)
  def check(msg):
    return msg.author == ctx.author and msg.channel == msg.channel
  await ctx.send("Please enter the quiz reason you would like to be added:")
  msg = await bot.wait_for("message", check=check)
  msg = msg.content.replace("\"", "")
  msg = msg.replace("\\", "\\\\")
  quiz_reasons.append(msg)
  await ctx.send("Quiz reason successfully added!")
  with open('quiz_reasons.json', 'w') as json_file:
    json.dump(quiz_reasons, json_file)
  
@bot.command(name='review', help="dispenses a review question (kinetics)")
async def review(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!review'} "+ str(param))
  with open('questions/kinetics.json') as f:
    questions = json.load(f)
  question_number = int(randint(0, len(questions)-1))

  embedVar = discord.Embed(title="Question #" + str(question_number + 1), timestamp=datetime.utcnow(), color=0xD3D3D3)

  if(questions[question_number]['image'] != 0):
    embedVar.set_image(url=questions[question_number]['image'])
  
  embedVar.add_field(name=questions[question_number]['question'], value="a) " + str(questions[question_number]['choices'][0]) + "\nb) " + str(questions[question_number]['choices'][1]) + "\nc) " + str(questions[question_number]['choices'][2]) + "\nd) " + str(questions[question_number]['choices'][3]), inline=False)

  embedVar.add_field(name="Category", value="`Kinetics`", inline=False)

  await ctx.reply(embed=embedVar)

  def check(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower() in ["a", "b", "c", "d"]

  attempts = 1
  while True:
    try:
      msg = await bot.wait_for("message", check=check, timeout=90)
    except asyncio.TimeoutError:
      await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
      break
    if msg.content.lower() == questions[question_number]['answer']:
      await msg.reply("Correct!")
      break
    else:
      if(attempts != 0):
        await msg.reply(f"Incorrect answer. You have {attempts} attempts left")
        attempts -= 1
        continue
      else:
        await msg.reply(f"Incorrect Answer. The correct answer was `{questions[question_number]['answer']}`.")
        break

@bot.command(name='addquestion', help="owner only")
async def addquestion(ctx, *params):
  if(ctx.author.id == 427832149173862400):
    def check(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower()[0] in string.printable
    def choices(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower() in ["a", "b", "c", "d"]
    def yesorno(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower() in ["yes", "no"]
    file = params[0]
    with open(f'questions/{file}.json') as f:
      question_data = json.load(f)
    try:
      past_number = question_data[-1]["number"]
      new_number = past_number + 1
    except IndexError:
      new_number = 0
    await ctx.send("Please enter the question")
    question = await bot.wait_for("message", check=check)
    await ctx.send("Please enter choice a")
    option_a = await bot.wait_for("message", check=check)
    await ctx.send("Please enter choice b")
    option_b = await bot.wait_for("message", check=check)
    await ctx.send("Please enter choice c")
    option_c = await bot.wait_for("message", check=check)
    await ctx.send("Please enter choice d")
    option_d = await bot.wait_for("message", check=check)
    await ctx.send("Please enter the answer")
    answer = await bot.wait_for("message", check=choices)
    await ctx.send("Is there an image with this question?")
    has_image = await bot.wait_for("message", check=yesorno)
    if(has_image.content == "yes"):
      await ctx.send("Please enter the imgur image link")
      image_link = await bot.wait_for("message", check=check)
      image = image_link.content
    else:
      image = 0
    await ctx.send("Does this question require the use of a calculator?")
    calculator = await bot.wait_for("message", check=yesorno)
    if(calculator.content == "yes"):
      need_calc = "True"
    else:
      need_calc = "False"
    await ctx.send("Does this question require the use of the reference table?")
    reference = await bot.wait_for("message", check=yesorno)
    if(reference.content == "yes"):
      need_reference = "True"
    else:
      need_reference = "False"

    question_data.append({"number": new_number, "question": question.content.replace('\n',' '), "choices": [option_a.content.replace('\n',' '), option_b.content.replace('\n',' '), option_c.content.replace('\n',' '), option_d.content.replace('\n',' ')], "answer": answer.content.replace('\n',' '), "image": image, "Calc": need_calc, "Table": need_reference})
    with open(f'questions/{file}.json', 'w') as json_file:
      json.dump(question_data, json_file)
    await ctx.send("Question successfully added!")
  else:
    ctx.send("This command is for the owner only")

@bot.command(name='spam', help="spams text")
async def spam(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!spam'} "+ str(param))
  messages = ""
  for thing in params:
      messages += (str(thing) + " ")
  msg = f"{messages}"
  if(msg[:2] == "s!"):
    await ctx.send("stop trying to loop me")
  elif(msg[:1] == ";"):
    await ctx.send("I'm not a pokemon automation bot")
  else:
    for i in range(5):
        await ctx.send(msg)
  
@bot.command(name='leaderboard', help="Displays the global leaderboards", aliases=['lb', 'leader'])
async def lb(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!lb'} "+ str(param))
  with open('profiles.json') as f:
    profile_data = json.load(f)
  percentages = {}
  try:
    if(str(params[0]).lower() in ['world', 'chem', 'apworld', 'chemistry', 'bal', 'money', 'rich', 'schlucks']):
      if(str(params[0]).lower() == 'world' or str(params[0]).lower() == 'apworld'):
        for i in range(len(profile_data)):
          try:
            percent_correct = (profile_data[i]['WorldCorrect']/profile_data[i]['WorldTotal']) * 100
          except ZeroDivisionError:
            percent_correct = 0
          percentages[str(profile_data[i]['Name'])] = percent_correct
        embedVar = discord.Embed(title="AP World Leaderboard", timestamp=datetime.utcnow(), color=0x00ff00)
        sorted_percentages = {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=True)} 
        msg = ""
        place = 1
        for key in sorted_percentages:
          msg += str(place) + ". " + key + " (" + str(round(sorted_percentages[key], 2)) + "%)\n"
          place += 1
        embedVar.add_field(name="Placements", value=msg, inline=False)
        await ctx.send(embed=embedVar)
      elif(str(params[0]).lower() == 'bal' or str(params[0]).lower() == 'money' or str(params[0]).lower() == 'rich' or str(params[0]).lower() == 'schlucks'):
        for i in range(len(profile_data)):
          try:
            schlucks = profile_data[i]['Balance']
          except ZeroDivisionError:
            schlucks = 0
          percentages[str(profile_data[i]['Name'])] = schlucks
        embedVar = discord.Embed(title="Richest Users", timestamp=datetime.utcnow(), color=0x00ff00)
        sorted_percentages = {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=True)} 
        msg = ""
        place = 1
        for key in sorted_percentages:
          msg += str(place) + ". " + key + " (" + str(round(sorted_percentages[key], 2)) + " schlucks)\n"
          place += 1
        embedVar.add_field(name="Placements", value=msg, inline=False)
        await ctx.send(embed=embedVar)
      else:
        for i in range(len(profile_data)):
          try:
            percent_correct = (profile_data[i]['Correct']/profile_data[i]['Total']) * 100
          except ZeroDivisionError:
            percent_correct = 0
          percentages[str(profile_data[i]['Name'])] = percent_correct
        embedVar = discord.Embed(title="Chemistry Leaderboard", timestamp=datetime.utcnow(), color=0x00ff00)
        sorted_percentages = {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=True)} 
        msg = ""
        place = 1
        for key in sorted_percentages:
          msg += str(place) + ". " + key + " (" + str(round(sorted_percentages[key], 2)) + "%)\n"
          place += 1
        embedVar.add_field(name="Placements", value=msg, inline=False)
        await ctx.send(embed=embedVar)
    else:
      await ctx.send("Invalid leaderboard choice! Showing chemistry leaderboard")
      for i in range(len(profile_data)):
          try:
            percent_correct = (profile_data[i]['Correct']/profile_data[i]['Total']) * 100
          except ZeroDivisionError:
            percent_correct = 0
          percentages[str(profile_data[i]['Name'])] = percent_correct
      embedVar = discord.Embed(title="Chemistry Leaderboard", timestamp=datetime.utcnow(), color=0x00ff00)
      sorted_percentages = {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=True)} 
      msg = ""
      place = 1
      for key in sorted_percentages:
        msg += str(place) + ". " + key + " (" + str(round(sorted_percentages[key], 2)) + "%)\n"
        place += 1
      embedVar.add_field(name="Placements", value=msg, inline=False)
      await ctx.send(embed=embedVar)
  except IndexError:
    for i in range(len(profile_data)):
      try:
        percent_correct = (profile_data[i]['Correct']/profile_data[i]['Total']) * 100
      except ZeroDivisionError:
        percent_correct = 0
      percentages[str(profile_data[i]['Name'])] = percent_correct
    embedVar = discord.Embed(title="Chemistry Leaderboard", timestamp=datetime.utcnow(), color=0x00ff00)
    sorted_percentages = {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=True)} 
    msg = ""
    place = 1
    for key in sorted_percentages:
      msg += str(place) + ". " + key + " (" + str(round(sorted_percentages[key], 2)) + "%)\n"
      place += 1
    embedVar.add_field(name="Placements", value=msg, inline=False)
    await ctx.send(embed=embedVar)

@bot.command(name='settings', help="displays the settings menu")
async def settings(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!settings'} "+ str(param))
  with open('profiles.json') as f:
    profile_data = json.load(f)
  uid = ctx.author.id
  found = 0
  found_indices = []
  for i in range(len(profile_data)):
    if(profile_data[i]['ID'] == uid):
      found = 1
      found_indices.append(i)
  if(found == 0):
    profile_data.append({"Name": ctx.author.name, "Tag": str(ctx.author), "Nick": ctx.author.display_name, "ID": ctx.author.id, "Avatar URL": str(ctx.author.avatar_url),"Correct": 0, "Total": 0, "Calc": "True","Table": "True","WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1})
    for i in range(len(profile_data)):
      if(profile_data[i]['ID'] == uid):
        found_indices.append(i)
  try:
    i_value = found_indices[0]
  except IndexError:
    await ctx.send("The bot encountered an unexpected error. (Error ID: 142)")
    return 0
  
  try:
    if(str(params[0]).lower() not in ["calc", "table"]):
      await ctx.send("Invalid setting!")
      return 0
    if(str(params[0]).lower() == "calc"):
      try:
        if(str(params[1]).lower() == "on"):
          profile_data[i_value]["Calc"] = "True"
        elif(str(params[1]).lower() == "off"):
          profile_data[i_value]["Calc"] = "False"
        else:
          await ctx.send("Second parameter should be either \"on\" or \"off\"")
          return 0
      except IndexError:
        await ctx.send("Please provide what you want the setting to be equal to when you run the command!")
        return 0
    if(str(params[0]).lower() == "table"):
      try:  
        if(str(params[1]).lower() == "on"):
          profile_data[i_value]["Table"] = "True"
        elif(str(params[1]).lower() == "off"):
          profile_data[i_value]["Table"] = "False"
        else:
          await ctx.send("Second parameter should be either \"on\" or \"off\"")
          return 0
      except IndexError:
        await ctx.send("Please provide what you want the setting to be equal to when you run the command!")
        return 0
    with open('profiles.json', 'w') as json_file:
      json.dump(profile_data, json_file)
    await ctx.send("Setting saved successfully!")
  except IndexError: 
    if(profile_data[i_value]["Calc"] == "True"):
      calc_value = f"{get_emoji('green_circle')} Enabled"
    else:
      calc_value = f"{get_emoji('red_circle')} Disabled"
    if(profile_data[i_value]["Table"] == "True"):
      table_value = f"{get_emoji('green_circle')} Enabled"
    else:
      table_value = f"{get_emoji('red_circle')} Disabled"
    
    embedVar = discord.Embed(title=f"{ctx.author.name}'s Regents Question Settings", description="Use the command syntax `s!settings <calc/table> <on/off>` to change these settings", timestamp=datetime.utcnow(), color=0xFF0000)
    embedVar.add_field(name="Questions that require the use of a calculator", value=calc_value, inline=False)
    embedVar.add_field(name="Questions that require the use of the reference table", value=table_value, inline=False)
    await ctx.send(embed=embedVar)

@bot.command(name='world', help="dispenses a Random AP World practice  question", aliases=['apworld', 'history'])
async def world(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!world'} "+ str(param))
  if(ctx.author.id == 523319470105993226):
    await ctx.send("you get no more questions (this only shows up for sean because he complained about the lack of questions. if he wants, he could volunteer to input them himself :roomad:)")
    return 0
  else:
    found = 0
    with open('profiles.json') as f:
      profile_data = json.load(f)
    for i in range(len(profile_data)):
      if(profile_data[i]['ID'] == ctx.author.id):
        found = 1
    if(found == 0):
      profile_data.append({"Name": ctx.author.name, "Tag": str(ctx.author), "Nick": ctx.author.display_name, "ID": ctx.author.id, "Avatar URL": str(ctx.author.avatar_url),"Correct": 0, "Total": 0, "Calc": "True","Table": "True","WorldCorrect": 0, "WorldTotal": 0, "Balance": 0, "Job": "", "Salary": 0, "xp": 0, "level": 1})

    with open('questions/apworld.json') as f:
      questions = json.load(f)
    question_number = int(randint(0, len(questions)-1))

    embedVar = discord.Embed(title="Question #" + str(question_number + 1), timestamp=datetime.utcnow(), color=0xadd8e6)

    if(questions[question_number]['image'] != 0):
      embedVar.set_image(url=questions[question_number]['image'])
    
    embedVar.add_field(name=questions[question_number]['question'], value="a) " + str(questions[question_number]['choices'][0]) + "\nb) " + str(questions[question_number]['choices'][1]) + "\nc) " + str(questions[question_number]['choices'][2]) + "\nd) " + str(questions[question_number]['choices'][3]), inline=False)

    await ctx.reply(embed=embedVar)

    def check(msg):
        return msg.author == ctx.author and msg.channel == msg.channel and \
        msg.content.lower() in ["a", "b", "c", "d"]
    try:
      msg = await bot.wait_for("message", check=check, timeout=90)
    except asyncio.TimeoutError:
      await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
      for i in range(len(profile_data)):
          if(profile_data[i]['ID'] == ctx.author.id):
            profile_data[i]['WorldTotal'] += 1
    if msg.content.lower() == questions[question_number]['answer']:
        for i in range(len(profile_data)):
          if(profile_data[i]['ID'] == ctx.author.id):
            profile_data[i]['WorldCorrect'] += 1
            profile_data[i]['WorldTotal'] += 1
        await msg.reply("Correct!")
    else:
        for i in range(len(profile_data)):
          if(profile_data[i]['ID'] == ctx.author.id):
            profile_data[i]['WorldTotal'] += 1
        await msg.reply(f"Incorrect Answer. The correct answer was `{questions[question_number]['answer']}`")
    with open('profiles.json', 'w') as json_file:
      json.dump(profile_data, json_file)

@bot.command(name='addworldquestion', help="owner only")
async def addworldquestion(ctx):
  if(ctx.author.id == 427832149173862400 or ctx.author.id == 523309470105993226 or ctx.author.id == 293416817408475136):
    def check(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower()[0] in string.printable
    def choices(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower() in ["a", "b", "c", "d"]
    def yesorno(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower() in ["yes", "no"]
    with open('questions/apworld.json') as f:
      question_data = json.load(f)
    try:
      past_number = question_data[-1]["number"]
      new_number = past_number + 1
    except IndexError:
      new_number = 0
    await ctx.send("Please enter the question")
    question = await bot.wait_for("message", check=check)
    await ctx.send("Please enter choice a")
    option_a = await bot.wait_for("message", check=check)
    await ctx.send("Please enter choice b")
    option_b = await bot.wait_for("message", check=check)
    await ctx.send("Please enter choice c")
    option_c = await bot.wait_for("message", check=check)
    await ctx.send("Please enter choice d")
    option_d = await bot.wait_for("message", check=check)
    await ctx.send("Please enter the answer")
    answer = await bot.wait_for("message", check=choices)
    await ctx.send("Is there an image with this question?")
    has_image = await bot.wait_for("message", check=yesorno)
    if(has_image.content == "yes"):
      await ctx.send("Please enter the imgur image link")
      image_link = await bot.wait_for("message", check=check)
      image = image_link.content
    else:
      image = 0

    question_data.append({"number": new_number, "question": question.content.replace('\n',' '), "choices": [option_a.content.replace('\n',' '), option_b.content.replace('\n',' '), option_c.content.replace('\n',' '), option_d.content.replace('\n',' ')], "answer": answer.content.replace('\n',' '), "image": image})
    with open('questions/apworld.json', 'w') as json_file:
      json.dump(question_data, json_file)
    await ctx.send("Question successfully added!")
  else:
    await ctx.send("This command is for the owner only")

@bot.command(name='test', help='test')
async def test(ctx, *params):  
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!test'} "+ str(param))
  def check(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower()[0] in string.printable
  await ctx.send("What do you want schleth to say in chit-chat")
  msg = await bot.wait_for("message", check=check)
  url = "https://discord.com/api/webhooks/842912209184096276/LKQ5-Nkj1VAp1hnpnhzgTK9EtShxrbnh6lT4VxTE5lQl1GjNug51ciLrEQzhynDif-y-" #webhook url, from here: https://i.imgur.com/f9XnAew.png

  #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook

  data = {
      "content" : msg.content,
      "username" : "schleth"
  }

  result = requests.post(url, json = data)

  try:
      result.raise_for_status()
  except requests.exceptions.HTTPError as err:
      print(err)
  else:
      print("Payload delivered successfully, code {}.".format(result.status_code))

  #result: https://i.imgur.com/DRqXQzA.png

@bot.command(name='stats', help="dispenses a Random AP Stats practice  question", aliases=['apstats'])
async def stats(ctx, *params):
    param = ""
    for thing in params:
      param += str(thing) + " "
    print(f"{ctx.author.name}: {'s!stats'} "+ str(param))
    with open('questions/apstats.json') as f:
      questions = json.load(f)
    question_number = int(randint(0, len(questions)-1))

    embedVar = discord.Embed(title="Question #" + str(question_number + 1), timestamp=datetime.utcnow(), color=0xadd8e6)

    embedVar.set_image(url=questions[question_number]['image'])
    
    # embedVar.add_field(name=questions[question_number]['question'], value="a) " + str(questions[question_number]['choices'][0]) + "\nb) " + str(questions[question_number]['choices'][1]) + "\nc) " + str(questions[question_number]['choices'][2]) + "\nd) " + str(questions[question_number]['choices'][3] + "\ne) " + str(questions[question_number]['choices'][4])), inline=False)

    await ctx.reply(embed=embedVar)

    def check(msg):
        return msg.author == ctx.author and msg.channel == msg.channel and \
        msg.content.lower() in ["a", "b", "c", "d", "e"]
    try:
      msg = await bot.wait_for("message", check=check, timeout=90)
    except asyncio.TimeoutError:
      await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
    if msg.content.lower() == questions[question_number]['answer']:
        await msg.reply("Correct!")
    else:
        await msg.reply(f"Incorrect Answer. The correct answer was `{questions[question_number]['answer']}`")

@bot.command(name='addstats', help="owner only")
async def addstats(ctx):
  if(ctx.author.id == 427832149173862400):
    def check(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower()[0] in string.printable
    def choices(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower() in ["a", "b", "c", "d", "e"]
    def yesorno(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower() in ["yes", "no"]
    with open('questions/apstats.json') as f:
      question_data = json.load(f)
    try:
      past_number = question_data[-1]["number"]
      new_number = past_number + 1
    except IndexError:
      new_number = 0
    # await ctx.send("Please enter the question")
    # question = await bot.wait_for("message", check=check)
    # await ctx.send("Please enter choice a")
    # option_a = await bot.wait_for("message", check=check)
    # await ctx.send("Please enter choice b")
    # option_b = await bot.wait_for("message", check=check)
    # await ctx.send("Please enter choice c")
    # option_c = await bot.wait_for("message", check=check)
    # await ctx.send("Please enter choice d")
    # option_d = await bot.wait_for("message", check=check)
    # await ctx.send("Please enter choice e")
    # option_e = await bot.wait_for("message", check=check)
    await ctx.send("Please enter the imgur image link")
    image_link = await bot.wait_for("message", check=check)
    image = image_link.content
    await ctx.send("Please enter the answer")
    answer = await bot.wait_for("message", check=choices)
    # await ctx.send("Is there an image with this question?")
    # has_image = await bot.wait_for("message", check=yesorno)
    # if(has_image.content == "yes"):

    question_data.append({"number": new_number, "answer": answer.content, "image": image})
    with open('questions/apstats.json', 'w') as json_file:
      json.dump(question_data, json_file)
    await ctx.send("Question successfully added!")
  else:
    await ctx.send("This command is for the owner only")

@bot.command(name='save')
async def save(ctx):
  if ctx.author.guild_permissions.administrator:
    await ctx.send("Saving...")
    # transcript = await chat_exporter.export(ctx.channel, None, "EST")
    # if transcript is None:
        # return
    # transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"archive-{ctx.channel.name}.html")
    # await ctx.send(file=transcript_file)
  else:
    await ctx.send("no saving for you")

@bot.command(name='adminstuff')
async def adminstuff(ctx):
  embedVar = discord.Embed(color=0xadd8e6)
  
  embedVar.add_field(name="How to gain access to the server", value="To gain access to the rest of the server, type **\"Tyler Bissoondial is a chad smurf\"** in this chat (case does not matter). Schlooth Bot will verify you soon after.", inline=False)

  await ctx.send(embed=embedVar)

@bot.command(name='howchinese')
async def china(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!howchinese'} "+ str(param))
  if(ctx.author.id == 418935684192272384 or ctx.author.id == 547514034027495444 or ctx.author.id == 539240329417588746 or ctx.author.id == 392093056171507713):
    num = randint(97, 100)
    await ctx.send(f"{ctx.author.mention}, you are {num}% chinese!")
  elif(ctx.author.id == 293416817408475136 or ctx.author.id == 333686255768305664 or ctx.author.id == 369278177404518412):
    num = randint(45, 99)
    await ctx.send(f"{ctx.author.mention}, you are {num}% chinese!")
  else:
    num = randint(-1, 65)
    await ctx.send(f"{ctx.author.mention}, you are {num}% chinese!")

@bot.event
async def on_member_join(member):
    chan = get_channel(bot, "verification")
    await chan.send(f"{member.mention}, please type the above phrase to get access to the rest of the server!")

@bot.event
async def on_message(ctx):
  if ctx.channel.id == 846124225173389322:
    if ctx.content.lower() == "tyler bissoondial is a chad smurf":
        member = ctx.author
        var = discord.utils.get(ctx.guild.roles, name = "Worker")
        await member.add_roles(var)
        await ctx.delete()
        chan = get_channel(bot, "verification-logs")
        await chan.send(f"Successfully given {ctx.author.mention} the role")
    else:
      if(ctx.author.id != 824112221751083018):
        await ctx.delete()

  if(ctx.content == "s!button"):
    await ctx.channel.send(
        "look at these cool buttons",
        components=[
            Button(style=ButtonStyle.blue, label="this is a blue button"),
            Button(style=ButtonStyle.red, label="cool red buttom"),
            Button(style=ButtonStyle.URL, label="look at my cool website", url="https://www.max49.cf/"),
        ],
    )

    res = await bot.wait_for("button_click")
    if res.channel == ctx.channel:
        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content=f'{res.component.label} clicked'
        )
  await bot.process_commands(ctx)

@bot.command(name='trivia', help="dispenses a user-submitted trivia question!")
async def trivia(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!trivia'} "+ str(param))

  with open('questions/trivia.json') as f:
    questions = json.load(f)
  question_number = int(randint(0, len(questions)-1))

  embedVar = discord.Embed(title="Question #" + str(question_number + 1), timestamp=datetime.utcnow(), color=0x00C3FF)

  if(questions[question_number]['image'] != 0):
    embedVar.set_image(url=questions[question_number]['image'])

  embedVar.add_field(name=questions[question_number]['question'], value="a) " + str(questions[question_number]['choices'][0]) + "\nb) " + str(questions[question_number]['choices'][1]) + "\nc) " + str(questions[question_number]['choices'][2]) + "\nd) " + str(questions[question_number]['choices'][3]), inline=False)

  embedVar.add_field(name="Added by:", value=questions[question_number]['creator'])

  await ctx.reply(embed=embedVar)

  def check(msg):
      return msg.author == ctx.author and msg.channel == msg.channel and \
      msg.content.lower() in ["a", "b", "c", "d"]
  try:
    msg = await bot.wait_for("message", check=check, timeout=120)
  except asyncio.TimeoutError:
    await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
  if msg.content.lower() == questions[question_number]['answer']:
    await msg.reply("Correct!")
  else:
    await msg.reply(f"Incorrect Answer. The correct answer was `{questions[question_number]['answer']}`")

@bot.command(name='addtrivia', help="add a question to s!trivia!")
async def addtrivia(ctx, *params):
  param = ""
  for thing in params: 
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!addtrivia'} "+ str(param))
  def check(msg):
    return msg.author == ctx.author and msg.channel == msg.channel and \
    msg.content.lower()[0] in string.printable
  def choices(msg):
    return msg.author == ctx.author and msg.channel == msg.channel and \
    msg.content.lower() in ["a", "b", "c", "d"]
  def yesorno(msg):
    return msg.author == ctx.author and msg.channel == msg.channel and \
    msg.content.lower() in ["yes", "no"]
  await ctx.send(f"{ctx.author.mention}, please enter the question (no questions with newlines)")
  question = await bot.wait_for("message", check=check)
  await ctx.send(f"{ctx.author.mention}, please enter choice a")
  option_a = await bot.wait_for("message", check=check)
  await ctx.send(f"{ctx.author.mention}, please enter choice b")
  option_b = await bot.wait_for("message", check=check)
  await ctx.send(f"{ctx.author.mention}, please enter choice c")
  option_c = await bot.wait_for("message", check=check)
  await ctx.send(f"{ctx.author.mention}, please enter choice d")
  option_d = await bot.wait_for("message", check=check)
  await ctx.send(f"{ctx.author.mention}, please enter the answer")
  answer = await bot.wait_for("message", check=choices)
  await ctx.send(f"{ctx.author.mention}, is there an image with this question?")
  has_image = await bot.wait_for("message", check=yesorno)
  with open('questions/trivia.json') as f:
    question_data = json.load(f)
  if(has_image.content == "yes"):
    await ctx.send("Please enter the imgur image link")
    image_link = await bot.wait_for("message", check=check)
    image = image_link.content
  else:
    image = 0
  try:
    past_number = question_data[-1]["number"]
    new_number = past_number + 1
  except IndexError:
    new_number = 0
  question_data.append({"number": new_number, "question": question.content.replace('\n',' '), "choices": [option_a.content.replace('\n',' '), option_b.content.replace('\n',' '), option_c.content.replace('\n',' '), option_d.content.replace('\n',' ')], "answer": (answer.content.replace('\n',' ')).lower(), "image": image, "creator": ctx.author.name})
  with open('questions/trivia.json', 'w') as json_file:
    json.dump(question_data, json_file)
  await ctx.send(f"{ctx.author.mention}, your question was successfully added!")

@bot.command(name="bal", aliases=['balance', 'money'])
async def bal(ctx, profile="none"):
  if profile == "none":
    param = ""
  else:
    param = profile
  print(f"{ctx.author.name}: {'s!bal'} "+ str(param))
  with open('profiles.json') as f:
      profile_data = json.load(f)
  if(profile != "none"):
    uid = profile
    try:
      uid = int(uid)
    except ValueError:
      uid = profile
  else:
    uid = ctx.author.id
  found = 0
  for i in range(len(profile_data)):
    user_mention = f"<@!{profile_data[i]['ID']}>"
    if(profile_data[i]['ID'] == uid or profile_data[i]['Name'] == uid or profile_data[i]['Nick'] == uid or profile_data[i]['Tag'] == uid or user_mention == uid):
      found = 1
      embedVar = discord.Embed(title=f"{profile_data[i]['Name']}'s balance", timestamp=datetime.utcnow(), color=0x00C3FF)
      embedVar.add_field(name="Balance", value=f"{profile_data[i]['Balance']} schlucks", inline=False)
      await ctx.reply(embed=embedVar)
  if(found == 0):
    await ctx.send("No profile found!")
  with open('profiles.json', 'w') as json_file:
    json.dump(profile_data, json_file)
  

@bot.command(name="updateprofiles")
async def update(ctx):
  if(ctx.author.id == 427832149173862400):
    with open('profiles.json') as f:
      profiles = json.load(f)
    for i in range(len(profiles)):
      profiles[i]['xp'] = 0
    for i in range(len(profiles)):
      profiles[i]['level'] = 1
    with open('profiles.json', 'w') as json_file:
      json.dump(profiles, json_file)
    await ctx.reply("Profiles successfully updated!")

@bot.command(name="resetcooldown")
async def resetcool(ctx):
  if(ctx.author.id == 427832149173862400):
    work.reset_cooldown(ctx)
    await ctx.send("Work cooldown reset!")
  else:
    await ctx.send("lol imagine not owning the bot")

@bot.command(name="work", help="work")
@commands.cooldown(1, 600, commands.BucketType.user)
async def work(ctx, *params):
  param = ""
  for thing in params:
    param += str(thing) + " "
  print(f"{ctx.author.name}: {'s!work'} "+ str(param))
  with open('profiles.json') as f:
    profiles = json.load(f)
  try:
    with open('work/jobs.json') as f:
      jobs = json.load(f)
    job_list = []
    for thing in jobs:
      for key, value in thing.items():
        if(key == "name"):
          job_list.append(value)
    if(params[0] == "list"):
      embedVar = discord.Embed(title="Currently Available Jobs", timestamp=datetime.utcnow(), color=0x00C3FF)
      msg = ""
      for i in range(len(jobs)):
        msg += f"{jobs[i]['name']}: {jobs[i]['base_salary']} schlucks\n"
      embedVar.add_field(name="Jobs", value=msg, inline=False)
      embedVar.add_field(name="\u200b", value="Do `s!work <job>` to select a job!")
      await ctx.reply(embed=embedVar)
      work.reset_cooldown(ctx)
      return 0
    if(str(params[0]).lower() in job_list):
      for i in range(len(profiles)):
        for j in range(len(job_list)):
          if(jobs[j]['name'] == str(params[0]).lower()):
            job_index = j
        if(profiles[i]['ID'] == ctx.author.id):
          if(profiles[i]['Job'] == ""):
            if(str(params[0]).lower() == "tyler"):
              if(ctx.author.id != 293416817408475136):
                await ctx.reply("You are not chad enough to have this job. Exiting.")
                work.reset_cooldown(ctx)
                return 0
            profiles[i]['Job'] = str(params[0]).lower()
            profiles[i]['Salary'] = jobs[job_index]['base_salary']
            await ctx.reply(f"You are now working as a `{str(params[0]).lower()}`! Do `s!work` to start working and making schlucks!")
            with open('profiles.json', 'w') as json_file:
              json.dump(profiles, json_file)
            work.reset_cooldown(ctx)
            return 0
          else:
            await ctx.reply(f"You're already working as a {profiles[i]['Job']}! Please do `s!work resign` to choose a new job.")
            work.reset_cooldown(ctx)
            return 0
    if(str(params[0]).lower() == "resign"):
      for i in range(len(profiles)):
        if(profiles[i]['ID'] == ctx.author.id):
          if(profiles[i]['Job'] != ""):
            old_job = profiles[i]['Job']
            profiles[i]['Job'] = ""
            profiles[i]['Salary'] = 0
            profiles[i]['xp'] = 0
            profiles[i]['level'] = 1
            await ctx.reply(f"You have resigned from your job as a `{old_job}`! Select a new job from `s!work list` to start working again!")
            with open('profiles.json', 'w') as json_file:
              json.dump(profiles, json_file)
            work.reset_cooldown(ctx)
            return 0
          else:
            await ctx.reply(f"You're already don't have a job! Select a job fron `s!work list`!")
            work.reset_cooldown(ctx)
            return 0
  except IndexError:
    var = 0
  for i in range(len(profiles)):
    if(profiles[i]['ID'] == ctx.author.id):
      if(profiles[i]['Job'] == ""):
        await ctx.reply("You don't have a job yet! Please choose one at `s!work list`")
        work.reset_cooldown(ctx)
        return 0
      else:
        # check for promotion
        if(profiles[i]['xp'] > (100 + (profiles[i]['level'] * 1.5))):
          embedVar = discord.Embed(title="Promotion!", timestamp=datetime.utcnow(), color=0xFFC0CB)
          embedVar.add_field(name=f"Congratulations {ctx.author.name}! You've been working hard recently and have worked your way up to a promotion!", value=f"Level: **{profiles[i]['level']}** --> **{profiles[i]['level'] + 1}**\nSalary: **{profiles[i]['Salary']} schlucks** --> **{math.floor(profiles[i]['Salary'] * 1.5)} schlucks**")
          profiles[i]['level'] += 1
          profiles[i]['xp'] = 0
          profiles[i]['Salary'] = math.floor(profiles[i]['Salary'] * 1.5)
          await ctx.reply(embed=embedVar)
          work.reset_cooldown(ctx)
          with open('profiles.json', 'w') as json_file:
            json.dump(profiles, json_file)
          return 0
        with open(f"work/{profiles[i]['Job']}.json") as f:
          work_scens = json.load(f)
        scen = randint(0, len(work_scens)-1)
        embedVar = discord.Embed(title=f"Work as a {profiles[i]['Job']}", color=0x00C3FF)
        embedVar.add_field(name=f"**{work_scens[scen]['type']}** - {work_scens[scen]['desc']}", value=f"`{work_scens[scen]['prompt']}`")
        await ctx.reply(embed=embedVar)
        attempts = 2
        def check(msg):
          return msg.author == ctx.author and msg.channel == msg.channel 
        while True:
          try:
            msg = await bot.wait_for("message", check=check, timeout=120)
          except asyncio.TimeoutError:
            await ctx.send(f"Sorry {ctx.author.mention}, you didn't reply in time!")
            break
          if msg.content.lower() == work_scens[scen]['answer']:
            correctEmbed = discord.Embed(color=0x00FF00)
            correctEmbed.add_field(name="Nice job!", value=f"You've earned {profiles[i]['Salary']} schlucks for working!")
            profiles[i]['Balance'] += profiles[i]['Salary']
            xp_given = randint(0, 20)
            profiles[i]['xp'] += xp_given
            await msg.reply(embed=correctEmbed)
            break
          else:
            if(attempts != 0):
              await msg.reply(f"Incorrect answer. You have {attempts} attempts left")
              attempts -= 1
              continue
            else:
              profiles[i]['Balance'] += math.floor(int(profiles[i]['Salary'])/3)
              await msg.reply(f"Incorrect Answer. The correct answer was `{work_scens[scen]['answer']}`. You've earned {math.floor(int(profiles[i]['Salary'])/3)} schlucks for working.")
              break
  with open('profiles.json', 'w') as json_file:
    json.dump(profiles, json_file)

@work.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cd = round(error.retry_after)
        minutes = str(cd // 60)
        seconds = str(cd % 60)
        em = discord.Embed(title=f"You can only work once per 10 minutes!",description=f"Try again in {minutes} minutes and {seconds} seconds.", color=0xFF0000)
        await ctx.send(embed=em)

@bot.command(name='amogus')
async def amogus(ctx):
  await ctx.send("ඞ"*2000)

@bot.command(name="say")
async def say(ctx, *params):
  msg = ' '.join(params)
  webhooks = await ctx.channel.webhooks()
  await ctx.message.delete()
  # print(webhooks)
  if len(webhooks) == 0:
    use_hook = await ctx.channel.create_webhook(name="Scloth")
  else:
    webhook_times = [webhook.created_at for webhook in webhooks]

    shortest = min(webhook_times)
    for webhook in webhooks:
        if webhook.created_at == shortest:
            use_hook = webhook
            if(use_hook.user != 'Chemistry Bot#6476'):
              use_hook = await ctx.channel.create_webhook(name="chem")
              break
            else:
              break
  if(msg == ""):
    await ctx.send("No message provided to say!")
  else:
    async with aiohttp.ClientSession() as session:
        # print(use_hook.url)
        webhook = Webhook.from_url(use_hook.url, adapter=AsyncWebhookAdapter(session))
        await webhook.send(msg, username=ctx.author.display_name, avatar_url=ctx.author.avatar_url, allowed_mentions=None)
    # await ctx.send(msg)

@bot.command(name="saym", help="syntax: s!saym <user> <message>")
async def say(ctx, *params):
  try:
    member = await converter.convert(ctx, params[0])
  except discord.ext.commands.errors.MemberNotFound as err:
    await ctx.send(f'{err} If the user\'s name is two words, please use quotation marks around their name.')
    return 0
  await ctx.message.delete()
  total_params = params[1:]
  msg = ' '.join(total_params)
  webhooks = await ctx.channel.webhooks()
  # print(webhooks)
  if len(webhooks) == 0:
    use_hook = await ctx.channel.create_webhook(name="Scloth")
  else:
    webhook_times = [webhook.created_at for webhook in webhooks]

    shortest = min(webhook_times)
    for webhook in webhooks:
        if webhook.created_at == shortest:
            use_hook = webhook
            if(use_hook.user != 'Chemistry Bot#6476'):
              use_hook = await ctx.channel.create_webhook(name="chem")
              break
            else:
              break
  if(msg == ""):
    await ctx.send("No message provided to say!")
  else:
    async with aiohttp.ClientSession() as session:
        # print(use_hook.url)
        webhook = Webhook.from_url(use_hook.url, adapter=AsyncWebhookAdapter(session))
        await webhook.send(msg, username=member.display_name, avatar_url=member.avatar_url, allowed_mentions=None)
    # await ctx.send(msg)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)}ms')
  

bot.run(TOKEN)
