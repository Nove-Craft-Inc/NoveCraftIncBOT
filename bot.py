import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

# Cargar configuración y variables de entorno
load_dotenv()

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

config = load_config()

# Intents necesarios para un bot avanzado
intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(intents=intents, command_prefix=commands.when_mentioned, help_command=None)

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} comandos sincronizados.")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")

# Comando de prueba con slash command
@bot.tree.command(name="ping", description="Responde con Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

# Cargar módulos
initial_extensions = [
    "cogs.music",       # Módulo de música
    "cogs.admin",       # Módulo de administración
    "cogs.moderation",  # Módulo de moderación
    "cogs.utility",     # Módulo de utilidades
    "cogs.fun",         # Módulo de entretenimiento
    "cogs.economy",     # Módulo de economía
    "cogs.leveling",    # Módulo de sistema de niveles
    "cogs.logs",        # Módulo de registros
    "cogs.config",      # Módulo de configuración del bot
]

if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Error al cargar {extension}: {e}")

    bot.run(os.getenv("DISCORD_TOKEN"))
