# Importaciones esenciales
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
import sys
import shlex
# Importaciones específicas de bibliotecas externas
import aiohttp
import colorama
import discord
import pyfiglet
import numpy
import openai
import psutil
import requests
from colorama import Fore
from discord import Permissions
from discord.ext import commands, tasks
from discord.utils import get
from contextlib import redirect_stdout
from openai import AsyncOpenAI


# Tiempo de inicio del bot
start_time = time.time()
archivo_estados = "status.txt"

# Función para leer el token de Discord desde un archivo de texto
def read_discord_token(filename):
    with open(filename, "r") as file:
        return file.read().strip()

# Función para leer el token de la API de OpenAI
def read_openai_token(filename):
    with open(filename, "r") as file:
        return file.read().strip()

# Función para leer los estados desde un archivo de texto
def read_statuses(filename):
    with open(filename, "r") as file:
        return file.read().strip().split(';')

# Definición del token de Discord
TOKEN = read_discord_token("token.txt")

# Carga el token de OpenAI desde el archivo 'token_open.txt'
openai_token = read_openai_token("token_open.txt")

# Inicializa el cliente de OpenAI con el token leído del archivo
client = AsyncOpenAI(api_key=openai_token)

# Definición del archivo que contiene los estados
STATUS_FILE = "status.txt"

# Lista de modelos de voz disponibles
tts_models = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

# Función para limpiar la consola
def clear():
    os.system("clear")



# Creación del bot con el prefijo y la configuración del self_bot
bot = commands.Bot(command_prefix=("!"), self_bot=True)

# Configuración del token
token = TOKEN

# Variable para controlar si el bot está en modo ping
ping = False

# Evento que se dispara cada vez que se recibe un mensaje
@bot.event
async def on_message(message):
    # Procesa los comandos del mensaje
    await bot.process_commands(message)

    # Imprime un mensaje indicando que el bot ha iniciado sesión correctamente
    print(f"{Fore.YELLOW}Has iniciado como {Fore.RED}{bot.user}")

# Elimina el comando predeterminado "help" para personalizarlo
bot.remove_command("help")


@bot.command()
async def help(ctx, *, command_name: str = None):
    """El comando de ayuda xd"""
    if command_name:
        # Busca el comando especificado por el usuario
        command = bot.get_command(command_name)
        if command:
            # Si el comando existe, devuelve su descripción
            await ctx.send(f"Descripción de `{command_name}`: {command.help}")
        else:
            await ctx.send("Ese comando no existe.")
    else:
        # Obtiene la lista de comandos ordenados alfabéticamente por nombre
        sorted_commands = sorted(bot.commands, key=lambda x: x.name)

        commands = []
        for command in sorted_commands:
            # Formatea cada comando con su nombre y ayuda en negrita
            commands.append(f"**{command.name}** - {command.help}")

        # Divide el mensaje si supera las 14 líneas
        chunk_size = 14
        chunks = [commands[i:i + chunk_size] for i in range(0, len(commands), chunk_size)]

        # Envía el mensaje para cada chunk y añade una reacción numerada
        for i, chunk in enumerate(chunks):
            # Construye el mensaje para el chunk actual
            message = f"**Lista de comandos** (Bloque {i + 1} de {len(chunks)}):\n"
            message += "\n".join(chunk)

            # Agrega la reacción numerada correspondiente al bloque actual
            num_emoji = f"{i + 1}\N{COMBINING ENCLOSING KEYCAP}"
            sent_message = await ctx.send(message)
            await sent_message.add_reaction(num_emoji)

            # Espera para el próximo mensaje
            await asyncio.sleep(1)  # Opcional, para evitar flood rate limits

# Función para cambiar el estado del bot
async def change_status():
    statuses = read_statuses(STATUS_FILE)
    if not statuses:
        return  # Si no hay estados, no hacemos nada
    status = random.choice(statuses)
    await bot.change_presence(activity=discord.Streaming(name=status, url="http://www.twitch.tv/tu_stream"))

# Comando para interactuar con GPT-3.5
@bot.command()
async def gpt(ctx, *, message: str):
    """Interactúa con GPT-4, requiere el token de OpenAI."""
    try:
        # Genera la respuesta usando el modelo
        completion = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": message}]  # Usa el mensaje del usuario
        )

        # Envía la respuesta al canal de Discord
        await ctx.send(completion.choices[0].message.content)

    except Exception as e:
        await ctx.send(f'Error al obtener respuesta: {str(e)}')

@bot.command()
async def tts(ctx, model: str = None, *, message: str = None):
    """Convierte el mensaje a audio usando TTS de OpenAI.
    
    Uso:
        !tts [modelo] [mensaje]
    
    Modelos disponibles:
        - alloy
        - echo
        - fable
        - onyx
        - nova
        - shimmer
    """
    if model is None or message is None:
        # Si no se proporcionan el modelo o el mensaje, muestra la ayuda
        await ctx.send("Por favor, especifica un modelo y un mensaje.\n\n" + tts.__doc__)
        return

    if model not in tts_models:
        await ctx.send(f"Modelo no válido. Los modelos disponibles son: {', '.join(tts_models)}")
        return

    try:
        # Configura la URL de la API
        url = "https://api.openai.com/v1/audio/speech"
        
        # Configura los headers, incluyendo la clave de API
        headers = {
            "Authorization": f"Bearer {openai_token}",  # Usa la clave de API cargada
            "Content-Type": "application/json"
        }

        # Configura el cuerpo de la solicitud
        data = {
            "model": "tts-1-hd",  # Asegúrate de que este modelo esté disponible
            "input": message,
            "voice": model,  # Usa el modelo proporcionado por el usuario
            "response_format": "mp3"  # Cambia a "mp3" para recibir el audio directamente
        }

        # Realiza la solicitud POST a la API
        response = requests.post(url, headers=headers, json=data)

        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            # Guarda el archivo MP3 en el sistema
            audio_file_path = "output.mp3"
            with open(audio_file_path, 'wb') as audio_file:
                audio_file.write(response.content)  # Escribe el contenido del audio

            # Envía el archivo al canal de Discord
            await ctx.send(file=discord.File(audio_file_path))
            
            # Elimina el archivo después de enviarlo
            os.remove(audio_file_path)
        else:
            await ctx.send(f'Error al obtener audio: {response.status_code} - {response.text}')

    except Exception as e:
        await ctx.send(f'Error al obtener audio: {str(e)}')



# Comando para analizar imágenes
@bot.command()
async def gpti(ctx, *, image_url: str):
    """Analiza una imagen a partir de su URL."""
    try:
        # Genera la respuesta usando la imagen proporcionada
        completion = await client.chat.completions.create(
            model="gpt-4o",  # Asegúrate de que este modelo esté disponible
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Que es esta imagen?, describeme que sale en esta imagen"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            }
                        },
                    ],
                }
            ],
        )

        # Envía la respuesta al canal de Discord
        await ctx.send(completion.choices[0].message.content)

    except Exception as e:
        await ctx.send(f'Error al analizar la imagen: {str(e)}')

@bot.command()
async def imagin(ctx, *, prompt: str):
    """Genera una imagen a partir del prompt dado en resolución 1080p."""
    try:
        # Genera la imagen usando DALL-E en resolución 1920x1080
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1792x1024",  # Cambiado a resolución 1080p
            quality="hd",  # Asegúrate de que la calidad esté configurada en alta
            n=1,
        )

        image_url = response.data[0].url

        # Envía la URL de la imagen generada al canal de Discord
        await ctx.send(image_url)

    except Exception as e:
        await ctx.send(f'Error al generar la imagen: {str(e)}')

@bot.command()
async def translate_audio(ctx, url: str = None):
    """Traduce un archivo de audio a texto en inglés. Usa un link o sube un archivo de audio."""
    if url is None and not ctx.message.attachments:
        await ctx.send("Por favor, proporciona un enlace de audio o sube un archivo de audio.")
        return

    if url:
        # Descargar el archivo de audio desde el enlace
        try:
            audio_file_path = "./temp_audio.mp3"  # Nombre temporal del archivo
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        await ctx.send("No se pudo descargar el archivo de audio desde el enlace proporcionado.")
                        return
                    with open(audio_file_path, 'wb') as f:
                        f.write(await response.read())
        except Exception as e:
            await ctx.send(f'**Error al descargar el audio: ** {str(e)}')
            return
    else:
        attachment = ctx.message.attachments[0]
        audio_file_path = f"./{attachment.filename}"
        await attachment.save(audio_file_path)

    try:
        # Abre el archivo de audio
        with open(audio_file_path, "rb") as audio_file:
            translation = await client.audio.translations.create(
                model="whisper-1",
                file=audio_file
            )

        # Comprobar el tipo de respuesta
        if isinstance(translation, dict) and 'text' in translation:
            await ctx.send(f"Traducción: {translation['text']}")
        else:
            await ctx.send("Error en la traducción del audio.")

    except Exception as e:
        await ctx.send(f'Error al traducir el audio: {str(e)}')

    finally:
        # Eliminar el archivo de audio temporal
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)

@bot.command()
async def wispertxt(ctx, url: str = None):
    """Transcribe un archivo de audio a texto. Usa un link o sube un archivo de audio."""
    if url is None and not ctx.message.attachments:
        await ctx.send("Por favor, proporciona un enlace de audio o sube un archivo de audio.")
        return

    if url:
        # Descargar el archivo de audio desde el enlace
        try:
            audio_file_path = "./temp_audio.mp3"  # Nombre temporal del archivo
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        await ctx.send("No se pudo descargar el archivo de audio desde el enlace proporcionado.")
                        return
                    with open(audio_file_path, 'wb') as f:
                        f.write(await response.read())
        except Exception as e:
            await ctx.send(f'**Error al descargar el audio:** {str(e)}')
            return
    else:
        attachment = ctx.message.attachments[0]
        audio_file_path = f"./{attachment.filename}"
        await attachment.save(audio_file_path)

    try:
        # Abre el archivo de audio
        with open(audio_file_path, "rb") as audio_file:
            transcription = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"  # Esto debería dar solo texto
            )

        # Aquí la transcripción debe ser un string directo
        await ctx.send(f"Transcripción: {transcription}")  # Envía directamente la transcripción

    except Exception as e:
        await ctx.send(f'Error al transcribir el audio: {str(e)}')
    finally:
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)  # Elimina el archivo de audio temporal

async def wispertr(ctx, idioma: str, url: str = None):
    """Transcribe un archivo de audio a texto y lo traduce al idioma especificado. Usa un link o sube un archivo de audio."""
    
    if url is None and not ctx.message.attachments:
        await ctx.send("Por favor, proporciona un enlace de audio o sube un archivo de audio.")
        return

    if url:
        # Descargar el archivo de audio desde el enlace
        try:
            audio_file_path = "./temp_audio.mp3"  # Nombre temporal del archivo
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        await ctx.send("No se pudo descargar el archivo de audio desde el enlace proporcionado.")
                        return
                    with open(audio_file_path, 'wb') as f:
                        f.write(await response.read())
        except Exception as e:
            await ctx.send(f'**Error al descargar el audio:** {str(e)}')
            return
    else:
        attachment = ctx.message.attachments[0]
        audio_file_path = f"./{attachment.filename}"
        await attachment.save(audio_file_path)

    try:
        # Abre el archivo de audio
        with open(audio_file_path, "rb") as audio_file:
            transcription = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"  # Esto debería dar solo texto
            )

        # Aquí la transcripción debe ser un string directo
        transcripcion_texto = transcription  # Usa la transcripción directamente

        # Envía el mensaje al modelo GPT para traducir el texto
        translate_message = f"Traducemelo al {idioma}: {transcripcion_texto}"
        completion = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": translate_message}]  # Usa el mensaje de traducción
        )

        # Envía la respuesta al canal de Discord
        await ctx.send(completion.choices[0].message.content)

    except Exception as e:
        await ctx.send(f'Error al transcribir o traducir el audio: {str(e)}')
    finally:
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)  # Elimina el archivo de audio temporal

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
    """Manda un mensaje una cantidad de veces indicada (numero de veces "mensaje") con un retraso de 0.2 segundos entre cada mensaje"""
    await ctx.message.delete()

    for i in range(times):
        await ctx.send(message)
        await asyncio.sleep(0.2)

@bot.command(aliases=["hypersquad"])
async def hs(ctx, house: str):
    """Cambia la afiliación de HypeSquad de un usuario a la casa especificada. (Bravery, Brilliance, o Balance)."""
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
    """Recrea ciertos evento historico (11 de septiembre)...."""
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
    """Haz una animacion de que te estas masturbando."""
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

@bot.command(description="Envía un mensaje a todos los canales de texto en el servidor.")
async def sendall(ctx, *, message):
    """Envía un mensaje a todos los canales de texto del servidor."""
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
async def stats(ctx):
    """
    Comando para mostrar estadísticas del equipo y selfbot.
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
    Obten la foto de perfil de un usuario usando el ID (no funciona el @).
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
    Borra todos los roles y canales de un server y crea 250 canales y roles llamado raid
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
    Invierte el texto.
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
async def cch(ctx, quantity=1, *, channel_name="test"):
    """
    Crea una cantidad específica de canales con el nombre especificado, si se deja en blanco se llamara test y solo hara un canal.
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
    Reacciona de forma masiva con un emote (cantidad + emote)  .
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
async def spoiler(ctx, *, message=None):
    """
    Envía un mensaje como spoiler.
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
async def subrayado(ctx, *, message=None):
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
async def cursiva(ctx, *, message=None):
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
async def tachado(ctx, *, message=None):
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
async def citar(ctx, *, message=None):
    """
    Envía un mensaje como si estuviera citado.
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
    Envía un mensaje con como si fuera un bloque de codigo.
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
    Bannea a todos los usuarios en el servidor.
    """
    await ctx.message.delete()  # Elimina el mensaje del comando ejecutado
    banned_users = []
    for member in ctx.guild.members:
        try:
            await member.ban(reason="Ban xd")
            banned_users.append(member.name)
        except Exception as e:
            await ctx.send(f'[ERROR]: {e}')

# Run Python code
@bot.command()
async def run(ctx, *, code):
    """
    Ejecuta código Python.
    """
    await ctx.message.delete()  # Elimina el mensaje del comando ejecutado
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            exec(code)
        except Exception:
            traceback.print_exc(file=f)
    output = f.getvalue()
    if output:
        await ctx.send(f'Salida del código: {output}')
    else:
        await ctx.send("Código ejecutado sin ninguna salida.")

@bot.command()
async def cmd(ctx, *, command):
    """
    Ejecuta un comando en el sistem host y muestra la salida.
    """
    try:
        await ctx.message.delete()  # Elimina el mensaje del comando ejecutado
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


@bot.command()
async def ascii(ctx, *, texto: str):
    """
    Convierte texto a texto art ascii.
    """
    try:
        await ctx.message.delete()  # Elimina el mensaje del comando ejecutado
        # Convierte el texto en arte ASCII utilizando pyfiglet
        ascii_art = pyfiglet.figlet_format(texto)

        # Envía el arte ASCII como un mensaje al canal
        await ctx.send("```" + ascii_art + "```")
    except Exception as e:
        await ctx.send(f"Se produjo un error: {e}")

@bot.command(aliases=["ri", "rol"], no_pm=True)
@commands.guild_only()
async def info_rol(ctx, *, rol: discord.Role):
    '''Muestra información sobre un rol'''
    guild = ctx.guild

    dias_desde_creacion = (ctx.message.created_at - rol.created_at).days
    rol_creado = rol.created_at.strftime("%d %b %Y %H:%M")
    creado_en = "{} (¡hace {} días!)".format(rol_creado, dias_desde_creacion)

    # Verificar si hay miembros en el rol
    if rol.members:
        miembros = ''
        i = 0
        for usuario in rol.members:
            miembros += f'{usuario.name}, '
            i += 1
            if i > 30:
                break
    else:
        miembros = 'No hay miembros en este rol'

    if str(rol.colour) == "#000000":
        color = "predeterminado"
    else:
        color = str(rol.colour).upper()

    info_rol = f"""
    Nombre del Rol: {rol.name}
    Usuarios: {len(rol.members)}
    Mencionable: {rol.mentionable}
    Visible : {rol.hoist}
    Posición: {rol.position}
    Administrador: {rol.managed}
    Color: {color}
    Fecha de Creación: {creado_en}
    Miembros: {miembros[:-2]}
    ID del Rol: {rol.id}
    """
    await ctx.send(f"```{info_rol}```")

@bot.command(aliases=['iconodeservidor'], no_pm=True)
async def logo_servidor(ctx):
    '''Devuelve la URL del icono del servidor.'''
    icono = ctx.guild.icon_url
    servidor = ctx.guild
    try:
        await ctx.send(icono)
    except discord.HTTPException:
        try:
            async with ctx.session.get(icono) as resp:
                imagen = await resp.read()
            with io.BytesIO(imagen) as archivo:
                await ctx.send(file=discord.File(archivo, 'logo_servidor.png'))
        except discord.HTTPException:
            await ctx.send(icono)

@bot.group(invoke_without_command=True, name='emoji', aliases=['emote', 'e'])
async def emoji(ctx, *, emoji: str):
    '''¡Usa emojis sin nitro!'''
    emoji = emoji.split(":")
    if len(emoji) == 1:
        emoji_name = emoji[0].strip()
        found_emoji = discord.utils.find(lambda e: emoji_name in e.name.lower(), ctx.bot.emojis)
        if found_emoji is not None:
            await ctx.send(str(found_emoji))
        else:
            await ctx.send("No se pudo encontrar el emoji.")
    elif len(emoji) == 3:
        emoji_id = emoji[2].strip()[:-1]
        found_emoji = discord.utils.get(ctx.bot.emojis, id=int(emoji_id))
        if found_emoji is not None:
            await ctx.send(str(found_emoji))
        else:
            await ctx.send("No se pudo encontrar el emoji.")
    else:
        await ctx.send("Formato de emoji incorrecto. Por favor, utiliza uno de estos formatos: <:nombre:ID> o simplemente el nombre del emoji.")


@bot.command()
async def textemoji(ctx, *, msg):
    """Convierte texto en emojis"""
    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

    if msg != None:
        out = msg.lower()
        text = out.replace(' ', '    ').replace('10', '\u200B:keycap_ten:')\
                  .replace('ab', '\u200B🆎').replace('cl', '\u200B🆑')\
                  .replace('0', '\u200B:zero:').replace('1', '\u200B:one:')\
                  .replace('2', '\u200B:two:').replace('3', '\u200B:three:')\
                  .replace('4', '\u200B:four:').replace('5', '\u200B:five:')\
                  .replace('6', '\u200B:six:').replace('7', '\u200B:seven:')\
                  .replace('8', '\u200B:eight:').replace('9', '\u200B:nine:')\
                  .replace('!', '\u200B❗').replace('?', '\u200B❓')\
                  .replace('vs', '\u200B🆚').replace('.', '\u200B🔸')\
                  .replace(',', '🔻').replace('a', '\u200B🅰')\
                  .replace('b', '\u200B🅱').replace('c', '\u200B🇨')\
                  .replace('d', '\u200B🇩').replace('e', '\u200B🇪')\
                  .replace('f', '\u200B🇫').replace('g', '\u200B🇬')\
                  .replace('h', '\u200B🇭').replace('i', '\u200B🇮')\
                  .replace('j', '\u200B🇯').replace('k', '\u200B🇰')\
                  .replace('l', '\u200B🇱').replace('m', '\u200B🇲')\
                  .replace('n', '\u200B🇳').replace('ñ', '\u200B🇳')\
                  .replace('o', '\u200B🅾').replace('p', '\u200B🅿')\
                  .replace('q', '\u200B🇶').replace('r', '\u200B🇷')\
                  .replace('s', '\u200B🇸').replace('t', '\u200B🇹')\
                  .replace('u', '\u200B🇺').replace('v', '\u200B🇻')\
                  .replace('w', '\u200B🇼').replace('x', '\u200B🇽')\
                  .replace('y', '\u200B🇾').replace('z', '\u200B🇿')
        try:
            await ctx.send(text)
        except Exception as e:
            await ctx.send(f'```{e}```')
    else:
        await ctx.send('¡Escribe algo!', delete_after=3.0)

@bot.command()
async def clean(ctx, quantity: int):
    '''Limpiar un número de tus propios mensajes
    Uso: {prefix}clean 5'''
    if quantity <= 15:
        total = quantity + 1
        async for message in ctx.channel.history(limit=total):
            if message.author == ctx.author:
                await message.delete()
                await asyncio.sleep(3.0)
    else:
        async for message in ctx.channel.history(limit=6):
            if message.author == ctx.author:
                await message.delete()
                await asyncio.sleep(3.0)


@bot.command()
async def hackban(ctx, userid, *, reason=None):
    '''Banear a alguien que no está en el servidor'''
    try:
        userid = int(userid)
    except:
        await ctx.send('¡ID inválida!')
        return

    try:
        await ctx.guild.ban(discord.Object(userid), reason=reason)
    except:
        await ctx.send('No se pudo llevar a cabo el ban.')
        return

    await ctx.send('Usuario baneado exitosamente.')


while True:
  try:
    bot.run(token, bot=False)
  except:
    print("The token is invalid")
    quit()
