import discord, json, requests, emoji, unicodedata
from discord.ext import commands
from discord.ui import Select, View
import Private as p




class WeatherClass(commands.Cog):
    def __inti__(self, bot):
        self.bot = bot

    #Gets the weather based off a users input
    #Input format: -weather City name, State code (if in US), Country code
    #Country code refers to the ISO 1833 country code list
    @commands.command()
    async def weather(self, ctx, *args):
        #The first steps of this command take the user input and converts the given city to it's coresponding Lattitude and Logittude based using the OpenWeather API
    
        #BaseURL for getting Lat and Lon
        baseURL = "http://api.openweathermap.org/geo/1.0/direct?q=" 

        #technically the command can take an infinite number of arguments, this is because some cities can be made up of more then one name
        #Ex: West Warwick
        #If this we didn't do it this way, citynames containing more then one word would have to be contained using " "
        #Which isn't user friendly


        #Using the arguments, we reduce any extra spaces by combining each argument with a single space
        #Ex: West                     Warwick,              RI, US
        #Becomes: West Warwick, RI, US
        inputArgsReader = ' '.join(args)

        #Next, we create an array by splitting each input by using ,
        positionArray = inputArgsReader.split(",")
    

        #If the positionArray is = 3, then it is in the US (since only US locations use the state codes)
        if(len(positionArray) == 3):
            url = baseURL + positionArray[0] + "," + positionArray[1] + "," + positionArray[2] + "&limit=10&appid=" + p.OPEN_WEATHER_API_KEY
            response = requests.get(url)
            print(url)

        #If the positionArray is = 2, it could be anywhere, The second input could be a state or a country code.
        elif(len(positionArray) == 2):
            url = baseURL + positionArray[0] + "," + positionArray[1] + "&limit=10&appid=" + p.OPEN_WEATHER_API_KEY
            response = requests.get(url)

        #If the positionArray is 1, then the user just entered a City name. This could be dangerous? The output might not be the city they were looking for
        elif(len(positionArray) == 1):

            url = baseURL + positionArray[0] + "&limit=10&appid=" + p.OPEN_WEATHER_API_KEY
            response = requests.get(url)
            
        
    
        #If something goes wrong here, The user input was incorrect. Throw an Excetion
    
        file = response.json()
   
        print("Response Length: "+ str(len(file)))

        try:
             #if no results, say that nothing was found
            if (len(file) == 0):
                await ctx.send("Dumbass")


            #If one result, send the information directly to the getWeather function, no selection needed
            elif len(file) == 1:
                    place = file[0]

                    #if there is a state in the location, send it to getWeather, if there is no state the stateName variable in the function defaults to ""
                    if "state" in place:
                        await ctx.send(embed = getWeather(place["lat"],place["lon"],place["name"],place["state"]))
                    else:
                        await ctx.send(embed = getWeather(place["lat"],place["lon"],place["name"]))


            #if more then one result, create a selection view where the user will be asked
            #to select on of the results. After an option is selected, display the weather for that city.
            else:
                #Creates a DropDownView object
                view = DropdownView()

                #list of new and duplicate country and states.
                #This is used to make sure duplicates aren't put into the selection list
                newState = []
                newCountry = []
                dupState = []
                dupCountry = []
                for i in range(len(file)):
                    place = file[i]

                    #if this instance of file mentions a state
                    if "state" in place:

                        #if the state has already been added to the newState list, do not create a new dropdown
                        if place["state"] not in newState:
                            newState.append(place["state"])


                            if(emoji.is_emoji(flag_for(place["country"]))):
                                #dropdown creation
                                view.dropdown.add_option(label = place["name"] + ", " + place["state"] + ", " + place["country"], emoji = flag_for(place["country"]))
                            else:
                                #dropdown creation for places without flag emoji
                                view.dropdown.add_option(label = place["name"] + ", " + place["state"] + ", " + place["country"])
                        else:
                            dupState.append(i)
                
                    #if a state is not mentioned, try to find duplicate countries
                    else:
                        if place["country"] not in newCountry:
                            newCountry.append(i)
                            if(emoji.is_emoji(flag_for(place["country"]))):
                                view.dropdown.add_option(label = place["name"] + ", " + place["country"], emoji = flag_for(place["country"]))
                            else:
                                view.dropdown.add_option(label = place["name"] + ", " + place["country"])
                        else:
                            dupCountry.append(i)

                await ctx.send("**multiple results found:**", view = view)

        except:
             await ctx.send("Something went wrong. Did you put the command in correctly?")

#Required for cog set up. Adds the cog to the bot class in the Mini Weston V3 file.
async def setup(bot):
    await bot.add_cog(WeatherClass(bot))

def flag_for(code):
    """Return unicode flag emoji given a 2-digit country code."""
    return "".join(
        unicodedata.lookup(f"REGIONAL INDICATOR SYMBOL LETTER {char}")
        for char in code
    )

class Dropdown(discord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='Select a location...', min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
    # Use the interaction object to send a response message containing
    # the user's favourite colour or choice. The self object refers to the
    # Select object, and the values attribute gets a list of the user's
    # selected options. We only want the first one.
        baseURL = "http://api.openweathermap.org/geo/1.0/direct?q="
        positionArray = self.values[0].split(",")
        #If the positionArray is = 3, then it is in the US (since only US locations use the state codes)
        if(len(positionArray) == 3):
            url = baseURL + positionArray[0] + "," + positionArray[1] + "," + positionArray[2] + "&limit=10&appid=" + p.OPEN_WEATHER_API_KEY
            response = requests.get(url)
            print("Geo URL: "+ url)

        #If the positionArray is = 2, it could be anywhere, The second input could be a state or a country code.
        elif(len(positionArray) == 2):
            url = baseURL + positionArray[0] + "," + positionArray[1] + "&limit=10&appid=" + p.OPEN_WEATHER_API_KEY
            response = requests.get(url)
            print("Geo URL: "+ url)

        #If the positionArray is 1, then the user just entered a City name. This could be dangerous? The output might not be the city they were looking for
        elif(len(positionArray) == 1):

            url = baseURL + positionArray[0] + "&limit=10&appid=" + p.OPEN_WEATHER_API_KEY
            response = requests.get(url)
            print("Geo URL: "+ url)
            
        file = response.json()
        place = file[0]
        if "state" in place:
            await interaction.response.send_message(embed = getWeather(place["lat"],place["lon"],place["name"], place["state"]))
        else: 
            await interaction.response.send_message(embed = getWeather(place["lat"],place["lon"],place["name"]))

        
class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.
        #also allows us to add more views to the dropdown object class
        self.dropdown = Dropdown()
        self.add_item(self.dropdown)


def getWeather(lat,lon,cityName,stateName = ""):
        
        #Weather request URL  
        url = "https://api.openweathermap.org/data/2.5/weather?" + "appid=" + p.OPEN_WEATHER_API_KEY + "&lat=" + str(lat) + "&lon=" + str(lon) + "&units=imperial"
        print("Weather URL: "+url)
        response = requests.get(url)
        file = response.json()
        data = file["main"]
        description = file["weather"]
        country = file["sys"]
        weather = file["wind"]
        temp = data["temp"]
        tempmin = data["temp_min"]
        tempmax = data["temp_max"]
        humidity = data["humidity"]
        symbolCode = description[0]["id"]
        
        if symbolCode in range(200, 805, 1):
            if symbolCode in range(200,233,1):
                #lightning
                Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823546117824523/cloud-with-lightning.png"
            if symbolCode in range(300,322,1):
                #rain cloud, drizzling
                Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823545169911940/cloud-with-rain.png"
            if symbolCode in range(500,532,1):

                if(symbolCode == 511):
                    #snowflake, freezing rain
                    Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823546432393297/snowflake.png"
                else:
                    #rain cloud
                    Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823545169911940/cloud-with-rain.png"
            if symbolCode in range(600,623,1):
                #snowflake
                Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823546432393297/snowflake.png"

            if symbolCode in range(701,782,1):
                #fog
                Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823544813404160/fog.png"
            if symbolCode == 800:
                #sunny
                Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823545778094111/sun.png"
            if symbolCode in range(801,805,1):
                if symbolCode == 801:
                    #partly cloudy, more sun
                    Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823545480286218/sun-behind-cloud.png"
                if symbolCode == 802:
                    #partly cloudy, less sun
                    Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1043291154214559764/partly-cloudy.png"
                if symbolCode == 803 or symbolCode == 804:
                    #clouds
                    Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823546763755651/cloudy.png"
        else: 
            #if Code is not in range, set the URL to sunny
            Wurl = "https://cdn.discordapp.com/attachments/785260019209863223/1042823545778094111/sun.png"

        
        embed=discord.Embed(title=str(round(temp,2)) + "°F" , description = str(round(((temp-32) * 0.56),2)) + "°C", color=0xfbff00)

        #if stateName is not "" mention it in the author list of the embed
        #if "" the place does not have a state, use the other author listing
        if (str(stateName) != ""):
            embed.set_author(name=str(cityName) + ", " + str(stateName) + ", " + str(country["country"]))
        else:
            embed.set_author(name=str(cityName) + ", " + str(country["country"]))
        embed.set_thumbnail(url=Wurl)
        embed.add_field(name="Condition: ", value=str(description[0]["description"]), inline=False)
        embed.add_field(name="Min " + str(tempmin) + "°F", value = "(" + str(round(((tempmin - 32) * .56),2)) + "°C)", inline=True)
        embed.add_field(name="Max " + str(tempmax) + "°F", value = "(" + str(round(((tempmax - 32) * .56),2)) + "°C)", inline=True)
        embed.add_field(name="Humidity", value= str(humidity)+"%", inline=False)
        embed.add_field(name="Wind", value=str(weather["speed"]) + " MPH" , inline=True)
        embed.set_footer(text="Lat: " + str(lat) + " " + "Lon: " + str(lon))
        return embed


