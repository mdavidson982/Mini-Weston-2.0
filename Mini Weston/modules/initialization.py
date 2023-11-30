import discord
from discord.ext import commands

class initialization(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Joined Servers: ")
        for guild in self.bot.guilds:
            selected_channel = guild.name
            print(selected_channel)

async def setup(bot):
    await bot.add_cog(initialization(bot))