import discord
from discord.ext import commands
import json
import os


def load_prefixes():
    if not os.path.exists("prefixes.json"):
        with open("prefixes.json", "w") as f:
            json.dump({}, f)
    with open("prefixes.json", "r") as f:
        return json.load(f)

def save_prefixes(data):
    with open("prefixes.json", "w") as f:
        json.dump(data, f, indent=4)

prefixes = load_prefixes()

def get_prefix(bot, message):
    return prefixes.get(str(message.guild.id), "PENE!")

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())


@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, new_prefix: str):
    prefixes[str(ctx.guild.id)] = new_prefix
    save_prefixes(prefixes)
    await ctx.send(f"Prefijo cambiado a `{new_prefix}`")


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def info(ctx):
    await ctx.send("Soy un bot avanzado con múltiples comandos y funciones!")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No especificado"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} ha sido expulsado. Razón: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No especificado"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} ha sido baneado. Razón: {reason}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Se han eliminado {amount} mensajes.", delete_after=5)


@bot.command()
async def say(ctx, *, message: str):
    await ctx.send(message)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Avatar de {member.display_name}", color=discord.Color.blue())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)


@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(title="Lista de Comandos", description="Aquí tienes mis comandos disponibles:", color=discord.Color.green())
    embed.add_field(name="🔹 `ping`", value="Muestra la latencia del bot.", inline=False)
    embed.add_field(name="🔹 `info`", value="Muestra información sobre el bot.", inline=False)
    embed.add_field(name="🔹 `setprefix <nuevo_prefijo>`", value="Cambia el prefijo del bot.", inline=False)
    embed.add_field(name="🔹 `kick <usuario>`", value="Expulsa a un usuario.", inline=False)
    embed.add_field(name="🔹 `ban <usuario>`", value="Banea a un usuario.", inline=False)
    embed.add_field(name="🔹 `clear <cantidad>`", value="Elimina mensajes en el canal.", inline=False)
    embed.add_field(name="🔹 `say <mensaje>`", value="Repite el mensaje enviado.", inline=False)
    embed.add_field(name="🔹 `avatar [usuario]`", value="Muestra el avatar de un usuario.", inline=False)
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


bot.run("ODg1ODkyNzI1MzE5MjkwOTUw.G0V2EI.SuQRbNYd6rTke2tUTM_JvMgozbPac_tkO9Ozvg")
