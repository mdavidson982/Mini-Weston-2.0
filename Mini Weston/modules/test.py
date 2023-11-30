import discord
from discord.ext import commands

class test(commands.Cog):
    def __inti__(self,bot):
        self.bot=bot

    @commands.command()
    async def test(self, ctx, value:int):
        await ctx.send(mathStuff(value))

def mathStuff(value):
    return value**2
async def setup(bot):
    await bot.add_cog(test(bot))
