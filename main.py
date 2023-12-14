# Importaciones necesarias
import asyncio
import datetime
import io
import json
import os
import random
import re
import string
import time
from urllib import parse, request
from itertools import cycle
import contextlib
from pathlib import Path
import platform
import subprocess
import sys´
import string
# Importaciones específicas de bibliotecas externas
import aiohttp
import colorama
import discord
import numpy
import openai
import psutil
import requests
from colorama import Fore
from discord import Permissions
from discord.ext import commands
from discord.utils import get
from contextlib import redirect_stdout

# Tiempo de inicio del bot
start_time = time.time()

# Clave de la API de OpenAI 
openai.api_key = ""

# Definición del token de Discord
TOKEN = ""

# Función para limpiar la consola
def clear():
    os.system("cls")

# Configuración del token
token = TOKEN

# Variable para controlar si el bot está en modo ping
ping = False

# Creación del bot con el prefijo y la configuración del self_bot
bot = commands.Bot(command_prefix=("!"), self_bot=True)

# Evento que se dispara cada vez que se recibe un mensaje
@bot.event
async def on_message(message):
    # Procesa los comandos del mensaje
    await bot.process_commands(message)

# Evento que se dispara cuando el bot está listo para funcionar
@bot.event
async def on_ready():
    # Cambia la presencia del bot para mostrar un estado de transmisión
    await bot.change_presence(activity=discord.Streaming(
        name='UPDMTLD', url='https://discord.gg/XQp9TTh3'))

    # Imprime un mensaje indicando que el bot ha iniciado sesión correctamente
    print(f"{Fore.YELLOW}Has iniciado como {Fore.RED}{bot.user}")

# Elimina el comando predeterminado "help" para personalizarlo
bot.remove_command("help")

@bot.command()
async def help(ctx): 
    """El comando de ayuda xd"""
    # Obtiene la lista de comandos ordenados alfabéticamente por nombre
    sorted_commands = sorted(bot.commands, key=lambda x: x.name)

    commands = []
    for command in sorted_commands:
        # Formatea cada comando con su nombre y ayuda
        commands.append(f"{command.name} - {command.help}")

    # Divide el mensaje si supera las 16 líneas
    chunk_size = 16
    chunks = [commands[i:i + chunk_size] for i in range(0, len(commands), chunk_size)]

    for i, chunk in enumerate(chunks):
        # Construye y envía el mensaje para cada chunk
        message = "**Lista de comandos**:\n"
        message += "\n".join(chunk)
        sent_message = await ctx.send(message)

@bot.command()
async def ia(ctx, *, message: str):
    """
    Command para interactuar con la API de OpenAI.
    """
    await ctx.message.delete()  # Delete the user's message
    try:
        # Request a completion from OpenAI
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  # Replace with the correct model name if different
            prompt=message,
            temperature=0.7,
            max_tokens=150,
        )

        # Send the generated response to the channel
        await ctx.send(response.choices[0].text)

    except Exception as e:
        # Handle errors and inform the user
        await ctx.send(f"There was an error processing the request to OpenAI! Details: {str(e)}")


        
@bot.command()
async def purge(ctx, limit: int):
    """Purga mensajes, funciona con !purge (numero de mensajes a eliminar)"""
    # Elimina el mensaje del usuario que llamó al comando
    await ctx.message.delete()

    # Verifica si el canal es un canal de texto de Discord
    if isinstance(ctx.channel, discord.TextChannel):
        # Utiliza el método purge para eliminar mensajes en un canal de texto
        messages = await ctx.channel.purge(limit=limit + 1)
        
        # Espera 1 segundo antes de enviar el siguiente mensaje
        await asyncio.sleep(1)

        # Envía un mensaje informando cuántos mensajes se eliminaron
        await ctx.send(f"Eliminados {len(messages) - 1} mensajes", delete_after=5)
    else:
        # Utiliza un bucle para eliminar mensajes en canales que no son de texto
        async for message in ctx.channel.history(limit=limit + 1):
            await message.delete()

        # Espera 1 segundo antes de enviar el siguiente mensaje
        await asyncio.sleep(1)

        # Envía un mensaje informando cuántos mensajes se eliminaron
        await ctx.send(f"Eliminados {limit} mensajes", delete_after=5)

@bot.command()
async def spam(ctx, times: int, *, message: str):
    """Spamea un mensaje varias veces con un retraso de 0.2 segundos entre cada mensaje."""
    await ctx.message.delete()

    for i in range(times):
        await ctx.send(message)
        await asyncio.sleep(0.2)

@bot.command(aliases=["hypersquad"])
async def hs(ctx, house: str):
    """Cambia la afiliación de HypeSquad de un usuario a la casa especificada.

    Parameters:
    - house (str): El nombre de la casa a la que se cambiará la afiliación (Bravery, Brilliance, o Balance).
    """
    await ctx.message.delete()
    headers = {'Authorization': token, 'Content-Type': 'application/json'}
    house_id = {
        "Bravery": 1,
        "Brilliance": 2,
        "Balance": 3
    }.get(house)

    if house_id is None:
        await ctx.send(f"La casa `{house}` no es válida. Las opciones son `Bravery`, `Brilliance` y `Balance`.")
        return

    payload = {'house_id': house_id}

    try:
        response = requests.post('https://discordapp.com/api/v9/hypesquad/online',
                                 headers=headers,
                                 json=payload)
        response.raise_for_status()
        
        # Obtén el nombre de la casa a la que se cambió
        house_name = {
            1: "Bravery",
            2: "Brilliance",
            3: "Balance"
        }.get(house_id, "Desconocida")
        
        await ctx.send(f"Has cambiado a `{house_name}` correctamente!", delete_after=5)
    except requests.exceptions.HTTPError as e:
        error = e.response.json()
        error_message = error.get("message", "Ocurrió un error desconocido.")
        await ctx.send(f"Ocurrió un error al cambiarte a `{house}`: {error_message}")


@bot.command()
async def ping(ctx):
    """Muestra el ping del bot en milisegundos."""
    await ctx.message.delete()
    await ctx.send(f'Tu ping es de {round(bot.latency * 1000)} ms')


@bot.command(aliases=["9/11", "911", "terrorist"])
async def nine_eleven(ctx):
    """Recrea ciertos evento historico...."""
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


@bot.command(aliases=["jerkoff", "ejaculate", "orgasm"], description="Un poco de troleo también.")
async def cum(ctx):
    """Un poco de troleo también."""
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
    await message.edit(content='''
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


@bot.command(description="Envía un texto invisible gigante.")
async def clear(ctx):
    """Envía un texto invisible gigante."""
    await ctx.message.delete()
    await ctx.send('ﾠﾠ' + '\n' * 400 + 'ﾠﾠ')


@bot.command(description="Envía un discurso de Armstrong en español.")
async def ams(ctx):
    """Envía un discurso de Armstrong en español."""
    await ctx.message.delete()
    await ctx.send("Tengo un sueño. Que un día cada persona de esta nación controle su propio destino. Una nación verdaderamente libre, maldita sea. Una nación de acción, no de palabras, gobernada por la fuerza, no por un comité. Donde la ley cambie para adaptarse al individuo, y no al revés. Donde el poder y la justicia vuelvan a estar donde deben estar: en manos del pueblo. ¡Donde cada hombre es libre de pensar - de actuar - por sí mismo! Que se jodan todos estos abogados de pacotilla y burócratas de mierda. ¡A la mierda con este montón de trivialidades y de mierda de los famosos que hay en Internet las 24 horas del día! ¡Que se joda el orgullo americano! ¡A LA MIERDA los medios de comunicación! ¡QUE SE JODA TODO! América está enferma. Podrido hasta la médula. No hay forma de salvarlo, tenemos que arrancarlo de raíz. Hacer borrón y cuenta nueva. ¡QUEMARLO! Y de las cenizas, nacerá una nueva América. Evolucionada, pero indómita. Los débiles serán purgados y los más fuertes prosperarán - libres de vivir como les parezca, ¡harán que América sea grande de nuevo!... ¡En mi nueva América, la gente morirá y matará por lo que cree! No por dinero. ¡No por petróleo! No por lo que se les dice que es correcto. ¡Cada hombre será libre de luchar en sus propias guerras!")

@bot.command(description="Sends an Armstrong speech in English.")
async def am(ctx):
    """Sends an Armstrong speech in English."""
    await ctx.message.delete()
    await ctx.send("I have a dream. That one day every person in this nation will control their own destiny. A nation of the truly free, dammit. A nation of action, not words, ruled by strength, not committee! Where the law changes to suit the individual, not the other way around. Where power and justice are back where they belong: in the hands of the people! Where every man is free to think - to act - for himself! FUCK all these limp-dick lawyers and chickenshit bureaucrats. FUCK this 24-hour Internet spew of trivia and celebrity bullshit! FUCK American pride! FUCK the media! FUCK ALL OF IT! America is diseased. Rotten to the core. There's no saving it - we need to pull it out by the roots. WIpe the slate clean. BURN IT DOWN! And from the ashes, a new America will be born. Evolved, but untamed! The weak will be purged, and the strongest will thrive -- free to live as they see fit, they will make America GREAT AGAIN!")

@bot.command(description="Sends the second part of Armstrong's speech.")
async def am2(ctx):
    """Sends the second part of Armstrong's speech."""
    await ctx.message.delete()
    await ctx.send("I do need capital. And votes. Wanna know why? I have a dream. That one day, every person in this nation will control their OWN destiny. A land of the TRULY free, dammit. A nation of ACTION, not words. Ruled by STRENGTH, not committee. Where the law changes to suit the individual, not the other way around. Where power and justice are back where they belong: in the hands of the people! Where every man is free to think -- to act -- for himself! Fuck all these limp-dick lawyers and chicken-shit bureaucrats. Fuck this 24/7 Internet spew of trivia and celebrity bullshit. Fuck American pride. Fuck the media! Fuck all of it! America is diseased. Rotten to the core. There's no saving it -- we need to pull it out by the roots. WIpe the slate clean. BURN IT DOWN! And from the ashes, a new America will be born. Evolved, but untamed! The weak will be purged, and the strongest will thrive -- free to live as they see fit, they will make America GREAT AGAIN!")

@bot.command(description="Envía la segunda parte del discurso de Armstrong en español.")
async def am2s(ctx):
    """Envía la segunda parte del discurso de Armstrong en español."""
    await ctx.message.delete()
    await ctx.send("Necesito capital. Y votos. ¿Quieres saber por qué? Tengo un sueño. Que un día, cada persona de esta nación controle su propio destino. Una tierra verdaderamente libre, maldita sea. Una nación de acción, no de palabras. Gobernada por la FUERZA, no por un comité. Donde la ley cambia para adaptarse al individuo, y no al revés. Donde el poder y la justicia vuelven a estar donde deben estar: ¡en manos del pueblo! Donde cada hombre es libre de pensar - de actuar - por sí mismo. Que se jodan todos estos abogados de pacotilla y burócratas de mierda. Que se joda este vomitar de trivialidades y de mierda de las celebridades en Internet las 24 horas del día. Que se joda el orgullo americano. Que se jodan los medios de comunicación. Que les den a todos. América está enferma. Podrido hasta la médula. No hay forma de salvarlo. Tenemos que arrancarlo de raíz. Hacer borrón y cuenta nueva. ¡QUEMARLO! Y de las cenizas")

@bot.command(description="Envía un mensaje a todos los canales de texto en el servidor.")
async def sendall(ctx, *, message):
    """Envía un mensaje a todos los canales de texto en el servidor."""
    await ctx.message.delete()
    author = ctx.author

    if not author.guild_permissions.manage_guild:
        await ctx.send("No tienes permisos para enviar mensajes en todos los canales de texto.")
        return

    random_number = random.randint(1000, 9999)
    confirm_message = await ctx.send(f"Para confirmar la acción, escribe el siguiente número aleatorio de 4 dígitos: `{random_number}`. Escribe 'si' seguido del número para continuar o cualquier otra cosa para cancelar.")

    def check(m):
        return m.author == author and m.channel == ctx.channel and m.content.lower() == f"si {random_number}"

    try:
        await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await confirm_message.edit(content="Tiempo de espera agotado. Acción cancelada.")
        return

    sent_to = []
    failed_to = []

    for channel in ctx.guild.text_channels:
        try:
            if channel.permissions_for(ctx.guild.me).send_messages:
                await channel.send(message)
                sent_to.append(channel.name)
                await asyncio.sleep(0.5)
        except:
            failed_to.append(channel.name)

    if sent_to:
        await ctx.send(f"El mensaje se envió correctamente a los siguientes canales:\n\n{', '.join(sent_to)}")
    if failed_to:
        await ctx.send(f"El mensaje no se pudo enviar a los siguientes canales:\n\n{', '.join(failed_to)}")

@bot.command()
async def ithastobe(ctx):
    """
    Enviar la letra de 'It Has To Be This Way'.
    """
    lyrics = [
        "Standing here",
        "I realize",
        "You are just like me",
        "Trying to make history",
        "But who's to judge",
        "The right from wrong?",
        "When our guard is down",
        "I think we'll both agree",
        "That violence breeds violence",
        "But in the end it has to be this way",
        "I've carved my own path",
        "You followed your wrath",
        "But maybe we're both the same",
        "The world has turned",
        "And so many have burned",
        "But nobody is to blame",
        "Yet staring across this barren wasted land",
        "I feel new life will be born",
        "Beneath the blood stained sand"
    ]

    for line in lyrics:
        await ctx.send(line)
        await asyncio.sleep(1.5) if line != "But in the end it has to be this way" else await asyncio.sleep(6)

@bot.command()
async def stats(ctx):
    """
    Comando para mostrar estadísticas del selfbot.
    """
    await ctx.message.delete()

    python_version = sys.version
    discord_version = discord.__version__
    os_platform = platform.system()
    os_info = f"{platform.system()} {platform.release()}"
    guild_count = len(bot.guilds)
    member_count = sum(len(guild.members) for guild in bot.guilds)

    # Use psutil to get CPU and memory information
    cpu_cores = psutil.cpu_count(logical=False)
    ram_info = psutil.virtual_memory()
    cpu_info = platform.processor()

    # Calculate uptime in seconds
    uptime_seconds = round(time.time() - start_time)
    uptime_str = str(datetime.timedelta(seconds=uptime_seconds))

    stats = (f"```\n"
             f"***********************************************************************************\n"
             f"Versión de Python: {python_version}\n"
             f"Versión de Discord.py: {discord_version}\n"
             f"Sistema Operativo: {os_platform} {platform.release()}\n"
             f"***********************************************************************************\n"
             f"Estoy en: {guild_count} servidores\n"
             f"***********************************************************************************\n"
             f"Tipo de CPU: {cpu_info}\n"
             f"Cantidad de núcleos de CPU: {cpu_cores}\n"
             f"Cantidad de RAM total: {ram_info.total / (1024 ** 3):.2f} GB\n"  # Convertir bytes a gigabytes
             f"Uso de memoria: {ram_info.percent}%\n"
             f"Tiempo de actividad: {uptime_str}\n"
             f"***********************************************************************************\n"

             f"```")
    await ctx.send(stats)


@bot.command()
async def av(ctx, user_id: int = None):
    """
    Comando para mostrar el avatar de un usuario por su ID (no funciona el @).
    """
    await ctx.message.delete()

    if user_id is None:
        user = ctx.author
    else:
        try:
            user = await bot.fetch_user(user_id)
        except discord.errors.NotFound:
            return await ctx.send(f"No se pudo encontrar un usuario con el ID {user_id}.")

    format = "gif" if user.is_avatar_animated() else "png"
    avatar_url = user.avatar_url_as(format=format)

    await ctx.send(f"Avatar de <@{user.id}>")
    await ctx.send(avatar_url)



@bot.command(aliases=["rekt", "nuke"])
async def destroy(ctx, verification_code: int = None):
    """
    Comando para realizar un ataque a gran escala en el servidor, tienes que poner
    """
    await ctx.message.delete()    
    random_number = random.randint(1000, 9999)
    confirm_message = await ctx.send(f"Para confirmar la acción, escribe el siguiente número aleatorio de 4 dígitos: `{random_number}`. Escribe 'si' seguido del número para continuar o cualquier otra cosa para cancelar.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == f"si {random_number}"

    try:
        await bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await confirm_message.edit(content="Tiempo de espera agotado. Acción cancelada.")
        return

    # Banear a todos los miembros del servidor
    for user in list(ctx.guild.members):
        try:
            await user.ban()
        except:
            pass
    
    # Eliminar todos los canales del servidor
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
        except:
            pass
    
    # Eliminar todos los roles del servidor
    for role in list(ctx.guild.roles):
        try:
            await role.delete()
        except:
            pass
    
    # Intentar cambiar la información del servidor
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
    
    # Crear 250 canales de texto con el nombre "raid <3"
    for _i in range(250):
        await ctx.guild.create_text_channel(name="raid <3")
    
    # Crear 250 roles con el nombre "raid <3" y colores aleatorios
    for _i in range(250):
        randcolor = discord.Color(random.randint(0x000000, 0xFFFFFF))
        await ctx.guild.create_role(name="raid <3", color=randcolor)

@bot.command(aliases=["nitrogen"]) #a random nitro gen 
async def nitro(ctx):
    """
    Genera nitro falso.
    """
    await ctx.message.delete()
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    await ctx.send(f' https://discord.gift/{code}')



@bot.command() #put text in reverse 
async def inversa(ctx, *, message=None):
    """
    Invierte el texto proporcionado.
    """
    await ctx.message.delete()
    if message is None:
        await ctx.send(
            f'[ERROR]: ¡Entrada no válida! Uso del comando: {bot.command_prefix}inversa <mensaje>'
        )
        return
    message = message[::-1]
    await ctx.send(message)

@bot.command(aliases=["masschannels", "masschannel", "ctc"])
async def cch(ctx, quantity=1, *, channel_name="RAID"):
    """
    Crea una cantidad específica de canales con el nombre especificado.
    """
    await ctx.message.delete()
    
    try:
        quantity = int(quantity)
    except ValueError:
        await ctx.send("¡Error! La cantidad debe ser un número entero.")
        return
    
    for _ in range(quantity):
        try:
            await ctx.guild.create_text_channel(name=channel_name)
        except Exception as e:
            await ctx.send(f'[ERROR]: {e}')


# Mass delete channels
@bot.command(aliases=["delchannel"])
async def delchs(ctx):
    """
    Elimina todos los canales en el servidor.
    """
    await ctx.message.delete()
    for channel in list(ctx.guild.channels):
        try:
            await channel.delete()
        except Exception as e:
            await ctx.send(f'[ERROR]: {e}')


# Rename channels
@bot.command()
async def mrnch(ctx, *, name=None):
    """
    Cambia el nombre de todos los canales en el servidor.
    """
    await ctx.message.delete()
    if name is None:
        await ctx.send("Error")
        return
    for channel in ctx.guild.channels:
        await channel.edit(name=name)

@bot.command()
async def rename_channel(ctx, *, name=None):
    """
    Cambia el nombre del canal donde se ejecutó el comando.
    """
    await ctx.message.delete()

    if name is None:
        await ctx.send("¡Error! Debes proporcionar un nombre para el canal.")
        return
    try:
        await ctx.channel.edit(name=name)
        await ctx.send(f"El nombre del canal ha sido cambiado a: {name}")
    except Exception as e:
        await ctx.send(f'[ERROR]: {e}')

# Rename server
@bot.command(aliases=["renameserver", "nameserver"])
async def rnsv(ctx, *, name=None):
    """
    Cambia el nombre del servidor.
    """
    await ctx.message.delete()
    if name is None:
        await ctx.send(
            f'[ERROR]: Entrada no válida. Uso del comando: {bot.command_prefix}servername <nombre>'
        )
        return
    await ctx.guild.edit(name=name)

@bot.command() #mass react with an emoji
async def massrc(ctx, quantity=None, emote=None):
    """
    Reacciona masivamente a una cantidad específica de mensajes con un emoji.
    """
    await ctx.message.delete()

    if quantity is None or emote is None:
        await ctx.send(
            f'[ERROR]: Debes especificar la cantidad y el emoji. Uso del comando: {bot.command_prefix}massrc <cantidad> <emoji>'
        )
        return

    try:
        quantity = int(quantity)
    except ValueError:
        await ctx.send("¡Error! La cantidad debe ser un número entero.")
        return

    messages = await ctx.message.channel.history(limit=quantity).flatten()
    for message in messages:
        await message.add_reaction(emote)

@bot.command() #the idk emoji in ASCII
async def niidea(ctx):
    """
    Envía el emoji ¯\_(ツ)_/¯
    """
    await ctx.message.delete()
    shrug = r'¯\_(ツ)_/¯'
    await ctx.send(shrug)

# Send a censored message
@bot.command()
async def censor(ctx, *, message=None):
    """
    Envía un mensaje censurado.
    """
    await ctx.message.delete()

    if message is None:
        await ctx.send(
            f'[ERROR]: Entrada no válida. Uso del comando: {bot.command_prefix}censor <mensaje>'
        )
        return

    await ctx.send('||' + message + '||')

# Send an underlined message
@bot.command()
async def underline(ctx, *, message=None):
    """
    Envía un mensaje subrayado.
    """
    await ctx.message.delete()

    if message is None:
        await ctx.send(
            f'[ERROR]: Entrada no válida. Uso del comando: {bot.command_prefix}underline <mensaje>'
        )
        return

    await ctx.send('__' + message + '__')

# Send an italicized message
@bot.command()
async def italicize(ctx, *, message=None):
    """
    Envía un mensaje en cursiva.
    """
    await ctx.message.delete()

    if message is None:
        await ctx.send(
            f'[ERROR]: Entrada no válida. Uso del comando: {bot.command_prefix}italicize <mensaje>'
        )
        return

    await ctx.send('*' + message + '*')

# Send a strikethrough message
@bot.command()
async def strike(ctx, *, message=None):
    """
    Envía un mensaje tachado.
    """
    await ctx.message.delete()

    if message is None:
        await ctx.send(
            f'[ERROR]: Entrada no válida. Uso del comando: {bot.command_prefix}strike <mensaje>'
        )
        return

    await ctx.send('~~' + message + '~~')

@bot.command()
async def quote(ctx, *, message=None):
    """
    Envía un mensaje citado.
    """
    await ctx.message.delete()

    if message is None:
        await ctx.send(
            f'[ERROR]: Entrada no válida. Uso del comando: {bot.command_prefix}quote <mensaje>'
        )
        return

    await ctx.send('> ' + message)

#Send a code message
# Send a code-formatted message
@bot.command()
async def code(ctx, *, message=None):
    """
    Envía un mensaje con formato de código.
    """
    await ctx.message.delete()

    if message is None:
        await ctx.send(
            f'[ERROR]: Entrada no válida. Uso del comando: {bot.command_prefix}code <mensaje>'
        )
        return

    await ctx.send('`' + message + "`")

# Mass ban users
@bot.command(aliases=["banwave", "banall"])
async def massban(ctx):
    """
    Prohíbe a todos los usuarios en el servidor.
    """
    banned_users = []
    for user in ctx.guild.members:
        try:
            await user.ban(reason="Prohibición masiva por un administrador")
            banned_users.append(user.name)
        except Exception as e:
            await ctx.send(f'[ERROR]: {e}')

# Run Python code
@bot.command()
async def run(ctx, *, code):
    """
    Ejecuta código Python.
    """
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            exec(code)
        except Exception as e:
            await ctx.send(f'Error: {e}')
            return
    output = f.getvalue()
    if output:
        await ctx.send(f'Salida del código: {output}')
    else:
        await ctx.send("Código ejecutado sin ninguna salida.")

import shlex

@bot.command()
async def cmd(ctx, *, command):
    """
    Ejecuta un comando en la shell y muestra la salida.
    """
    try:
        # Dividir el comando en argumentos utilizando shlex
        args = shlex.split(command)

        # Ejecutar el comando en la shell
        result = subprocess.run(args, capture_output=True, text=True)
        output = result.stdout
        if not output:
            output = result.stderr

        # Limitar la longitud de la salida para prevenir abusos
        output = output[:2000]

        await ctx.send(f"```{output}```")
    except Exception as e:
        await ctx.send(f"Se produjo un error: {e}")



while True:
  try:
    bot.run(token, bot=False)
  except:
    print("The token is invalid")
    quit()
