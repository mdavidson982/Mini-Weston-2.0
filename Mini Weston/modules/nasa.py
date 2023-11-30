import discord, requests, json, aiohttp
from discord.ext import commands
import Private as p

#NASA Buttons
class ReadDescription(discord.ui.View):
    def __init__(self, json, timeout = 180):
        super().__init__(timeout=timeout)
        self.js = json

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Read Description', style=discord.ButtonStyle.green, )
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        apodDescriptionEmbed = discord.Embed(title = "**" + self.js["title"] + "**")
        apodDescriptionEmbed.set_footer(text=self.js["explanation"])
        apodDescriptionEmbed.set_thumbnail(url= "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/NASA_Worm_logo.svg/2560px-NASA_Worm_logo.svg.png")
        await interaction.response.edit_message(embed = apodDescriptionEmbed)

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)

class nasa(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def apod(self,ctx):
        base_url = "https://api.nasa.gov/planetary/apod?api_key="
        
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url + p.NASA_API_KEY) as r:
                self.js = await r.json()
        
        if(self.js["media_type"] == "image"):
            apodImageEmbed = discord.Embed(title = "**" + self.js["title"] + "**")

            if("hdurl" in self.js):
                apodImageEmbed.set_image(url = self.js["hdurl"])
                apodImageEmbed.set_footer(text = "NASA Astronomy Picture of the Day | Date: {date}".format(date = self.js["date"]), icon_url= "https://cdn.discordapp.com/attachments/849172801076199495/1049776014131200021/nasa-logo-web-rgb.png")
            else:
                apodImageEmbed.set_image(self.js["url"])
                apodImageEmbed.set_footer(text = "NASA Astronomy Picture of the Day | Date: {date} |".format(date = self.js["date"]), icon_url= "https://cdn.discordapp.com/attachments/849172801076199495/1049776014131200021/nasa-logo-web-rgb.png")

        await ctx.send(embed=apodImageEmbed, view = ReadDescription(self.js))



#async def sendMessage():
    #guild = client.get_guild(785260019209863220)
    #channel = guild.get_channel(785260019209863223)
    #async guild.channel.send("sent on start")
async def setup(bot):
    await bot.add_cog(nasa(bot))