from .voice import Voice
import discord
from discord.ext import commands
import yaml


bot = commands.Bot(command_prefix=commands.when_mentioned_or("sous-"),
                   description='What do you think I am, a sous-chef?')
with open('config.yml') as f:
    bot.config = yaml.safe_load(f)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} ({bot.user.id})')


bot.add_cog(Voice(bot))
bot.run(bot.config['token'])
