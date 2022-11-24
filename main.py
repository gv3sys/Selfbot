import asyncio
import datetime
import functools
import io
import json
import os
import random
import re
import string
import urllib.parse
import urllib.request
import time
from urllib import parse, request
from itertools import cycle
from bs4 import BeautifulSoup as bs4
import contextlib
import aiohttp
import colorama
import discord
import numpy
import requests
from colorama import Fore
from discord import Permissions
from discord.ext import commands
from discord.utils import get
from gtts import gTTS
from pathlib import Path  # For paths
import platform  # For stats
import logging


def clear():
  system("cls")


TOKEN = "" #put your token between the ""

token = (TOKEN)

ping = False

bot = commands.Bot(command_prefix=("!"), self_bot=True)


@bot.event
async def on_message(message):
  await bot.process_commands(message)


@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Streaming(
    name='UPDMTLD', url='https://www.youtube.com/watch?v=2Sj_UygVjMI'))
  print(f"{Fore.YELLOW}Logged as {Fore.RED}{bot.user}")


bot.remove_command("help")


@bot.command() #purge messages of yourself
async def ps(message):
  async for msg in message.channel.history(limit=10000):
    if msg.author == bot.user:
      try:
        await msg.delete()
      except:
        pass


@bot.command() #purge all messages in chat 
async def pa(message):
  async for msg in message.channel.history(limit=10000):
    try:
      await msg.delete()
    except:
      pass


@bot.command()
async def hypesquad(ctx, house): #change hypersquad, chose between number 1 to 3
  await ctx.message.delete()
  request = requests.session()
  headers = {'Authorization': token, 'Content-Type': 'application/json'}

  global payload

  if house == "1":
    payload = {'house_id': 1} 

  if house == "2":
    payload = {'house_id': 2}

  if house == "3":
    payload = {'house_id': 3}

  try:
    requests.post('https://discordapp.com/api/v9/hypesquad/online',
                  headers=headers,
                  json=payload)
    print(f"{Fore.GREEN}Has cambiado a {house} correctamente!")
  except:
    print(f"{Fore.RED}Ha ocurrido un error al intentar cambiarte a {house}")


@bot.command() #show your ping 
async def ping(ctx):
  await ctx.message.delete()
  await ctx.send(f'Tu ping es de {round(bot.latency * 1000)} ms')


@bot.command(aliases=["9/11", "911", "terrorist"]) # a bit of trolling
async def nine_eleven(ctx):
  await ctx.message.delete()
  invis = ""  # char(173)
  message = await ctx.send(f'''
{invis}:man_wearing_turban::airplane:    :office:           
''')
  await asyncio.sleep(0.5)
  await message.edit(content=f'''
{invis} :man_wearing_turban::airplane:   :office:           
''')
  await asyncio.sleep(0.5)
  await message.edit(content=f'''
{invis}  :man_wearing_turban::airplane:  :office:           
''')
  await asyncio.sleep(0.5)
  await message.edit(content=f'''
{invis}   :man_wearing_turban::airplane: :office:           
''')
  await asyncio.sleep(0.5)
  await message.edit(content=f'''
{invis}    :man_wearing_turban::airplane::office:           
''')
  await asyncio.sleep(0.5)
  await message.edit(content='''
        :boom::boom::boom:    
        ''')


@bot.command(aliases=["jerkoff", "ejaculate", "orgasm"]) #a bit of trolling too
async def cum(ctx):
  await ctx.message.delete()
  message = await ctx.send('''
            :ok_hand:            :smile:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant:''')
  await asyncio.sleep(0.5)
  await message.edit(content='''
                      :ok_hand:            :smiley:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:  
     ''')
  await asyncio.sleep(0.5)
  await message.edit(content='''
                      :ok_hand:            :grimacing:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant:  
     ''')
  await asyncio.sleep(0.5)
  await message.edit(content='''
                      :ok_hand:            :persevere:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:   
     ''')
  await asyncio.sleep(0.5)
  await message.edit(content='''
                      :ok_hand:            :confounded:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant: 
     ''')
  await asyncio.sleep(0.5)
  await message.edit(content='''
                       :ok_hand:            :tired_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:    
             ''')
  await asyncio.sleep(0.5)
  await message.edit(contnet='''
                       :ok_hand:            :weary:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:= D:sweat_drops:
             :trumpet:      :eggplant:        
     ''')
  await asyncio.sleep(0.5)
  await message.edit(content='''
                       :ok_hand:            :dizzy_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')
  await asyncio.sleep(0.5)
  await message.edit(content='''
                       :ok_hand:            :drooling_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')


@bot.command() #send a giant invisible text 
async def clear(ctx):
  await ctx.message.delete()
  await ctx.send('ﾠﾠ' + '\n' * 400 + 'ﾠﾠ')


@bot.command(
  aliases=["img", "searchimg", "searchimage", "imagesearch", "imgsearch"]) #search fo images (it dosent work really well)
async def image(ctx, *, args):
  await ctx.message.delete()
  url = 'https://unsplash.com/search/photos/' + args.replace(" ", "%20")
  page = requests.get(url)
  soup = bs4(page.text, 'html.parser')
  image_tags = soup.findAll('img')
  if str(image_tags[2]['src']).find("https://trkn.us/pixel/imp/c="):
    link = image_tags[2]['src']
    try:
      async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
          image = await resp.read()
      with io.BytesIO(image) as file:
        await ctx.send(f"Search result for: **{args}**",
                       file=discord.File(file, f"exeter_anal.png"))
    except:
      await ctx.send(f'' + link + f"\nResultado de busqueda para: **{args}** ")
  else:
    await ctx.send("Nothing found for **" + args + "**")


@bot.command()
async def ams(ctx): #armstrong speach in spanish xd 
  await ctx.message.delete()
  await ctx.send(
    "Tengo un sueño. Que un día cada persona de esta nación controle su propio destino. Una nación verdaderamente libre, maldita sea. Una nación de acción, no de palabras, gobernada por la fuerza, no por un comité. Donde la ley cambie para adaptarse al individuo, y no al revés. Donde el poder y la justicia vuelvan a estar donde deben estar: en manos del pueblo. ¡Donde cada hombre es libre de pensar - de actuar - por sí mismo! Que se jodan todos estos abogados de pacotilla y burócratas de mierda. ¡A la mierda con este montón de trivialidades y de mierda de los famosos que hay en Internet las 24 horas del día! ¡Que se joda el orgullo americano! ¡A LA MIERDA los medios de comunicación! ¡QUE SE JODA TODO! América está enferma. Podrido hasta la médula. No hay forma de salvarlo, tenemos que arrancarlo de raíz. Hacer borrón y cuenta nueva. ¡QUEMARLO! Y de las cenizas, nacerá una nueva América. Evolucionada, pero indómita. Los débiles serán purgados y los más fuertes prosperarán - libres de vivir como les parezca, ¡harán que América sea grande de nuevo!... ¡En mi nueva América, la gente morirá y matará por lo que cree! No por dinero. ¡No por petróleo! No por lo que se les dice que es correcto. ¡Cada hombre será libre de luchar en sus propias guerras!"
  )


@bot.command()
async def am(ctx): #armstong speach 
  await ctx.message.delete()
  await ctx.send(
    "I have a dream. That one day every person in this nation will control their own destiny. A nation of the truly free, dammit. A nation of action, not words, ruled by strength, not committee! Where the law changes to suit the individual, not the other way around. Where power and justice are back where they belong: in the hands of the people! Where every man is free to think - to act - for himself! FUCK all these limp-dick lawyers and chickenshit bureaucrats. FUCK this 24-hour Internet spew of trivia and celebrity bullshit! FUCK American pride! FUCK the media! FUCK ALL OF IT! America is diseased. Rotten to the core. There's no saving it - we need to pull it out by the roots. Wipe the slate clean. BURN IT DOWN! And from the ashes, a new America will be born. Evolved, but untamed! The weak will be purged and the strongest will thrive - free to live as they see fit, they'll make America great again!... In my new America, people will die and kill for what they BELIEVE! Not for money. not for oil! Not for what they're told is right. Every man will be free to fight his own wars!"
  )


@bot.command() #second part of armstrong's speach
async def am2(ctx):
  await ctx.message.delete()
  await ctx.send(
    "I do need capital. And votes. Wanna know why? I have a dream. That one day, every person in this nation will control their OWN destiny. A land of the TRULY free, dammit. A nation of ACTION, not words. Ruled by STRENGTH, not committee. Where the law changes to suit the individual, not the other way around. Where power and justice are back where they belong: in the hands of the people! Where every man is free to think -- to act -- for himself! Fuck all these limp-dick lawyers and chicken-shit bureaucrats. Fuck this 24/7 Internet spew of trivia and celebrity bullshit. Fuck American pride. Fuck the media! Fuck all of it! America is diseased. Rotten to the core. There's no saving it -- we need to pull it out by the roots. WIpe the slate clean. BURN IT DOWN! And from the ashes, a new America will be born. Evolved, but untamed! The weak will be purged, and the strongest will thrive -- free to live as they see fit, they will make America GREAT AGAIN!"
  )


@bot.command()
async def am2s(ctx): #armstrongs speach in english 
  await ctx.message.delete()
  await ctx.send(
    "Necesito capital. Y votos. ¿Quieres saber por qué? Tengo un sueño. Que un día, cada persona de esta nación controle su propio destino. Una tierra verdaderamente libre, maldita sea. Una nación de acción, no de palabras. Gobernada por la FUERZA, no por un comité. Donde la ley cambia para adaptarse al individuo, y no al revés. Donde el poder y la justicia vuelven a estar donde deben estar: ¡en manos del pueblo! Donde cada hombre es libre de pensar - de actuar - por sí mismo. Que se jodan todos estos abogados de pacotilla y burócratas de mierda. Que se joda este vomitar de trivialidades y de mierda de las celebridades en Internet las 24 horas del día. Que se joda el orgullo americano. Que se jodan los medios de comunicación. Que les den a todos. América está enferma. Podrido hasta la médula. No hay forma de salvarlo. Tenemos que arrancarlo de raíz. Hacer borrón y cuenta nueva. ¡QUEMARLO! Y de las cenizas, nacerá una nueva América. ¡Evolucionada, pero indómita! Los débiles serán purgados, y los más fuertes prosperarán - libres de vivir como les parezca, ¡harán a América GRANDE DE NUEVO!"
  )


@bot.command() #send message to every channel in a server 
async def sendall(ctx, *, message):
  await ctx.message.delete()
  try:
    channels = ctx.guild.text_channels
    for channel in channels:
      await channel.send(message)
  except:
    pass


@bot.command() #send the lyrics of it has to be this way 
async def ithastobe(ctx):
  await ctx.message.delete()
  await ctx.send("Standing here")
  await asyncio.sleep(1.5)
  await ctx.send("I realize")
  await asyncio.sleep(1.5)
  await ctx.send("You are just like me")
  await asyncio.sleep(1.5)
  await ctx.send("Trying to make history")
  await asyncio.sleep(1.5)
  await ctx.send("But who's to judge")
  await asyncio.sleep(1.5)
  await ctx.send("The right from wrong?")
  await asyncio.sleep(1.5)
  await ctx.send("When our guard is down")
  await asyncio.sleep(1.5)
  await ctx.send("I think we'll both agree")
  await asyncio.sleep(1.5)
  await ctx.send("That violence breeds violence")
  await asyncio.sleep(1.5)
  await ctx.send("But in the end it has to be this way")
  await asyncio.sleep(6)
  await ctx.send("I've carved my own path")
  await asyncio.sleep(1.5)
  await ctx.send("You followed your wrath")
  await asyncio.sleep(1.5)
  await ctx.send("But maybe we're both the same")
  await asyncio.sleep(1.5)
  await ctx.send("The world has turned")
  await asyncio.sleep(1.5)
  await ctx.send("And so many have burned")
  await asyncio.sleep(1.5)
  await ctx.send("But nobody is to blame")
  await asyncio.sleep(1.5)
  await ctx.send("Yet staring across this barren wasted land")
  await asyncio.sleep(1.5)
  await ctx.send("I feel new life will be born")
  await asyncio.sleep(1.5)
  await ctx.send("Beneath the blood stainеd sand")



@bot.command() #see the stats of yout bot 
async def stats(ctx):
  await ctx.message.delete()
  """
    A usefull command that displays bot statistics.
    """
  pythonVersion = platform.python_version()
  dpyVersion = discord.__version__
  serverCount = len(bot.guilds)
  memberCount = len(set(bot.get_all_members()))

  await ctx.send(
    f"I'm in **{serverCount}** servers:\nI use the version **{pythonVersion}** of python, with the version **{dpyVersion}** of discord.py,"
  )



@bot.command(aliases=['pfp', 'avatar']) #get your pfp or someones pfp 
async def av(ctx, *, user: discord.Member = None):
  await ctx.message.delete()
  format = "gif"
  if user is None:
    user = ctx.author
  if user.is_avatar_animated() != True:
    format = "png"
  avatar = user.avatar_url_as(format=format if format != "gif" else None)
  async with aiohttp.ClientSession() as session:
    async with session.get(str(avatar)) as resp:
      image = await resp.read()
  with io.BytesIO(image) as file:
    await ctx.send(file=discord.File(file, f"Avatar.{format}"))


@bot.command(name='first-message', #see the first message in a chat or channel 
             aliases=['firstmsg', 'fm', 'firstmessage', 'primermsg'])
async def primermsg(ctx, channel: discord.TextChannel = None):
  await ctx.message.delete()
  if channel is None:
    channel = ctx.channel
  try:
    first_message = (await channel.history(limit=1,
                                           oldest_first=True).flatten())[0]
    await ctx.send(
      f"The first message in {channel.mention} is:  {first_message.jump_url}")
  except Exception as e:
    await ctx.send(f'[ERROR]: {e}')


@bot.command(aliases=["rekt", "nuke"]) # a raid option
async def destroy(ctx):
    await ctx.message.delete()
    for user in list(ctx.guild.members):
        try:
            await user.ban()
        except:
            pass
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
        except:
            pass
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
        except:
            pass
    try:
        await ctx.guild.edit(
            name="".join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(14, 32))),
            description="raid <3",
            reason="raid <3",
            icon=None,
            banner=None
        )
    except:
        pass
    for _i in range(250):
        await ctx.guild.create_text_channel(name="raid <3")
    for _i in range(250):
        randcolor = discord.Color(random.randint(0x000000, 0xFFFFFF))
        await ctx.guild.create_role(name="raid <3", color=randcolor)



@bot.command(aliases=["nitrogen"]) #a random nitro gen 
async def nitro(ctx):
  await ctx.message.delete()
  code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
  await ctx.send(f'https://discord.gift/{code}')



@bot.command() #Make a poll
async def poll(ctx, *, arguments=None):
  await ctx.message.delete()
  if arguments is None:
    await ctx.send(
      f'[ERROR]: Invalid input! Command: {bot.command_prefix}poll msg:<message> 1:<option1> 2:<option2>'
    )
    return
  message = discord.utils.escape_markdown(
    arguments[str.find(arguments, "msg:"):str.find(arguments, "1:")]).replace(
      "msg:", "")
  option1 = discord.utils.escape_markdown(
    arguments[str.find(arguments, "1:"):str.find(arguments, "2:")]).replace(
      "1:", "")
  option2 = discord.utils.escape_markdown(
    arguments[str.find(arguments, "2:"):]).replace("2:", "")
  message = await ctx.send(
    f'`Poll: {message}\nOpcion 1: {option1}\nOpcion 2: {option2}`')
  await message.add_reaction('🅰')
  await message.add_reaction('🅱')


@bot.command() #put text in reverse 
async def reverse(ctx, *, message=None):
  await ctx.message.delete()
  if message is None:
    await ctx.send(
      f'[ERROR]: Invalid input! Command: {bot.command_prefix}reverse <message>'
    )
    return
  message = message[::-1]
  await ctx.send(message)


#Mass create channels
@bot.command(aliases=["masschannels", "masschannel", "ctc"])
async def spamch(ctx):
  await ctx.message.delete()
  for _i in range(250):
    try:
      await ctx.guild.create_text_channel(name="RAID")
    except Exception as e:
      await ctx.send(f'[ERROR]: {e}')


#Mass delete channels
@bot.command(aliases=["delchannel"])
async def delchs(ctx):
  await ctx.message.delete()
  for channel in list(ctx.guild.channels):
    try:
      await channel.delete()
    except Exception as e:
      await ctx.send(f'[ERROR]: {e}')


#Rename channels
@bot.command(aliases=["rc"])
async def rnch(ctx, *, name=None):
  await ctx.message.delete()
  if name is None:
    await ctx.send(
      f'[ERROR]: Invalid input! Command: {bot.command_prefix}renamechannels <name>'
    )
    return
  for channel in ctx.guild.channels:
    await channel.edit(name=name)


#Rename server
@bot.command(aliases=["renameserver", "nameserver"])
async def rnsv(ctx, *, name=None):
  await ctx.message.delete()
  if name is None:
    await ctx.send(
      f'[ERROR]: Invalid input! Command: {bot.command_prefix}servername <name>'
    )
    return
  await ctx.guild.edit(name=name)


@bot.command() #mass react with an emoji
async def massrc(ctx, emote=None):
  await ctx.message.delete()
  if emote is None:
    await ctx.send(
      f'[ERROR]: Invalid input! Command: {bot.command_prefix}massreact <emote>'
    )
    return
  messages = await ctx.message.channel.history(limit=200).flatten()
  for message in messages:
    await message.add_reaction(emote)


@bot.command() #the idk emoji in ascci
async def niidea(ctx):
  await ctx.message.delete()
  shrug = r'¯\_(ツ)_/¯'
  await ctx.send(shrug)


#Send a censor message
@bot.command() 
async def spoiler(ctx, *, message=None):
  await ctx.message.delete()
  if message is None:
    await ctx.send(
      f'[ERROR]: Invalid input! Command: {bot.command_prefix}censor <message>')
  await ctx.send('||' + message + '||')


#Send a underline message
@bot.command()
async def subrayado(ctx, *, message=None):
  await ctx.message.delete()
  if message is None:
    await ctx.send(
      f'[ERROR]: Invalid input! Command: {bot.command_prefix}underline <message>'
    )
  await ctx.send('__' + message + '__')


#Send a italicize message
@bot.command()
async def cursiva(ctx, *, message=None):
  await ctx.message.delete()
  if message is None:
    await ctx.send(
      f'[ERROR]: Invalid input! Command: {bot.command_prefix}italicize <message>'
    )
    return
  await ctx.send('*' + message + '*')


#Send a strike message
@bot.command()
async def tachado(ctx, *, message=None):
  await ctx.message.delete()
  if message is None:
    await ctx.send(
      f'[ERROR]: Invalid input! Command: {bot.command_prefix}strike <message>')
    return
  await ctx.send('~~' + message + '~~')


@bot.command()
async def mencion(ctx, *, message=None):
  await ctx.message.delete()
  if message is None:
    await ctx.send(
      f'[ERROR]: Invalid input! Command: {bot.command_prefix}quote <message>')
    return
  await ctx.send('> ' + message)


#Send a code message
@bot.command()
async def code(ctx, *, message=None):
  await ctx.message.delete()
  if message is None:
    await ctx.send(
      f'[ERROR]: Invalid input! Command: {bot.command_prefix}code <message>')
    return
  await ctx.send('`' + message + "`")

@bot.command(aliases=["banwave", "banall", "etb"])
async def massban(ctx):
    await ctx.message.delete()
    users = list(ctx.guild.members)
    for user in users:
        try:
            await user.ban(reason="sry <3")
        except Exception as e:
            await ctx.send(f'[ERROR]: {e}')

while True:
  try:
    bot.run(token, bot=False)
  except:
    print("The token is invalid")
    quit()
