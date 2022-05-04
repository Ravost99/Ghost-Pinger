import os, time
try:
  import disnake
except ModuleNotFoundError: 
  os.system('pip install disnake')
  import disnake

from disnake.ext import commands
from datetime import datetime
from up import keep_alive

os.system('clear')

intents = disnake.Intents.default()
bot = commands.Bot(commands.when_mentioned_or('>>'), intents=intents)
whitelisted_ids = [742835236315856907] #whitelist ids here
mod_logs = 971101865263640616 # mod logs channel id

bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!\nWatching for pings!')
    print('-------------')
    keep_alive()


@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")
    current_date = datetime.today().strftime('%m-%d-%Y')
    mod_ch = await bot.fetch_channel(mod_logs)
    msg = message.content
    
    if '@' in msg:
      if message.author.bot or message.author.id in whitelisted_ids:
        print(f"Ignoring ghost ping by {message.author}")
        embed = disnake.Embed(
          title="Ignoring Ghost Ping",
          description=f"by {message.author}",
          color=0xFF0000
        )
        embed.add_field(
          name='Author',
          value=message.author,
          inline=True
        )
        embed.add_field(
          name='Message:',
          value=msg,
          inline=True
        )
        embed.set_footer(
          text=f'{current_time} {current_date}'
        )
        await mod_ch.send(embed=embed)
      else:
        embed = disnake.Embed(
          title='Ghost Ping Found!',
          color=0xFF0000
        )
        embed.add_field(
          name='Author',
          value=message.author,
          inline=True
        )
        embed.add_field(
          name='Message:',
          value=msg,
          inline=True
        )
        embed.set_footer(
          text=f'{current_time} {current_date}'
        )
        print(f'Ghost Ping Found! By {message.author}, message: {msg}. ({current_time} {current_date})\n')
        time.sleep(1)
        await message.channel.send(embed=embed)
        await mod_ch.send(embed=embed)

@bot.command(name='ping', description='Check if the bot is alive.')
async def ping(ctx):
    embed = disnake.Embed(
      title='Nope you can\'t ghost ping.',
      description=
        f'Lol I\'m alive {round(bot.latency * 1000)} ms :ping_pong: '
    )
    await ctx.send(embed=embed)


bot.run(os.environ['TOKEN'])