import discord
from discord.ext import commands, tasks
from mcstatus import MinecraftServer

TOKEN = 'TWOJ_DISCORD_BOT_TOKEN'  # Wstaw token swojego bota
MC_SERVER_ADDRESS = 'adres.serwera.pl'  # Wstaw adres swojego serwera Minecraft (np. 127.0.0.1:25565)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user.name}')
    update_status.start()

@tasks.loop(seconds=60)  # Odświeżaj co 60 sekund
async def update_status():
    try:
        server = MinecraftServer.lookup(MC_SERVER_ADDRESS)
        status = server.status()
        activity = discord.Game(name=f'Graczy online: {status.players.online}')
        await bot.change_presence(activity=activity)
    except Exception as e:
        print(f'Błąd podczas sprawdzania serwera: {e}')
        await bot.change_presence(activity=discord.Game(name='Brak połączenia z serwerem'))

@bot.command()
async def gracze(ctx):
    try:
        server = MinecraftServer.lookup(MC_SERVER_ADDRESS)
        status = server.status()
        await ctx.send(f'Na serwerze jest {status.players.online} graczy z {status.players.max} możliwych.')
    except Exception as e:
        await ctx.send('Nie udało się połączyć z serwerem Minecraft.')

bot.run(TOKEN) #rejn3k
