
from asyncio import tasks
from io import StringIO
from os import name, stat
from typing import overload
import discord
import random
from discord.client import Client
from discord.enums import Status
from discord.ext import commands
from discord.ext import tasks
import youtube_dl
import csv


adminID = [226067872084918272,356190294645145610,314426905812008963,215322500047962113,226065427732627459]

deciderID =[332321662513053696,255776481832206337,376381640039202827]
intents = discord.Intents.all()
ReactRolefile = open('React_Role_documentation.txt', 'r+')

 
#Client (our bot)
client = commands.Bot(command_prefix='-', intents = intents)

client.remove_command('help')

#Role name correlates with Role id, where x is in role x is in roleid, this array keeps the name of all the roles correlated with its react role message
rolename = []
#roleid (should really be called message id, but it's the ID of all the messages with react role implimentations)
roleid = []
#User and User ID will be used in the reinstate command
userid = []
user = []
finnArray = []
statusArray = []
pollEmojis = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]


westonid = 356088181671854081
mattid = 215322800047962113 

#April fools day
#voicechannelID = [739289572604903445,827063625863921684,827063824703946782,827063852093014067,827063889509220362,827063920069050388,827063946522394654,827063971739205652,827063998700322836,827064047597780992]

#NDOM default 
voicechannelID = [739289069862780970,738604934894714941,738605079237754980,753356829362356306,799175016876998697,738605353385852978,792590301239181322,738606157865943083,786424105044803624,739289572604903445,814707296755777566]
statusesUsed = []

#testing channel 
# voicechannelID = [811110785472266240,811110585714343976,811110632525922354,811110528528809984,785260019209863224,811070630924779530,811070728199733268,811070757625921577,811110152744730625,811110454243491861,811110484014923786,811110504021753858,811110555720613918,811110727547879425,811110627660529664,811110778312196107]


#Testing channel
#guildID = (785260019209863220)

#NDOM 
guildID = (355505175085187073)



#On start up
@client.event
async def on_ready():
    general_channel = client.get_channel(738603332637294642)
    
     
    with open('React_Role_documentation.txt', encoding="UTF-8") as csvfile:
        file = csv.reader(csvfile)
        
        for rec in file:
            rolename.append(rec[0]) 
            roleid.append(rec[1]) 
    csvfile.close         
    print("React Roll system")
    print(rolename)
    print(roleid)

    with open('Finn_images.txt') as csvfile:
        file = csv.reader(csvfile)
        for rec in file:
            finnArray.append(rec[0])
    print('Finn Images')
    print(finnArray)
    csvfile.close

    with open('Status_documentation.txt', encoding= "UTF-8") as csvfile:
        file = csv.reader(csvfile)

        for rec in file:
            statusArray.append(rec[0])
    print('Status system')
    print(statusArray)
    csvfile.close



    await general_channel.send('Hell yeah brother (Mini Weston online)')
    await client.wait_until_ready()
    background_task.start()



@tasks.loop(seconds= 86400)
async def background_task():
    startUpInt = random.randint(0, len(statusArray))
    startUpStatus = ""
    general_channel = client.get_channel(738603332637294642)

    if len(statusesUsed) >= len(statusArray):
        statusesUsed.clear()
        await general_channel.send("All statuses used. CLEARING.")

    while startUpInt in statusesUsed:
        startUpInt = random.randint(0, len(statusArray))
    else:
        statusesUsed.append(startUpInt)

    startUpStatus = statusArray[startUpInt] 

    await client.change_presence(status = discord.Status.do_not_disturb, activity= discord.Game(startUpStatus))
    await general_channel.send("Status changed to: " + startUpStatus)
    
def isAdmin(uID):
    if uID in adminID:
        return True 
    else:
        return False

def isWeston(uID):
    if uID == westonid:
        return True
    else: 
        return False

@client.command(name = 'status')
async def version(context):
    if context.message.author.id in adminID:
        await context.message.channel.send(statusesUsed)
    else:
        await context.message.channel.send("Shut up")

@client.command(name = 'changestatus')
async def changestatus(context, number):
    if context.author.id in adminID:
        startUpInt = int(number)
        startUpInt = startUpInt - 1
        startUpStatus = ""
        general_channel = client.get_channel(738603332637294642)
        if startUpInt < len(statusArray):    

            if len(statusesUsed) >= len(statusArray):
                statusesUsed.clear()
                await general_channel.send("All statuses used. CLEARING.")
            statusesUsed.append(startUpInt)

            startUpStatus = statusArray[startUpInt]

            await client.change_presence(status = discord.Status.do_not_disturb, activity= discord.Game(startUpStatus))
            await context.channel.send("Status changed to: " + startUpStatus)
        else:
            await context.channel.send("Send a proper number next time")
    else:
        await context.channel.send ("Shut up, nerd")


@changestatus.error
async def changestatusRandom(context, error):


    if isinstance(error, commands.MissingRequiredArgument):

        if context.message.author.id in adminID:
            startUpInt = random.randint(0, len(statusArray))
            startUpStatus = ""
            general_channel = client.get_channel(738603332637294642)
            

            if len(statusesUsed) >= len(statusArray):
                statusesUsed.clear()
                await general_channel.send("All statuses used. CLEARING.")

            while startUpInt in statusesUsed:
                startUpInt = random.randint(0, len(statusArray))
            else:
                statusesUsed.append(startUpInt)

            startUpStatus = statusArray[startUpInt]

            await client.change_presence(status = discord.Status.do_not_disturb, activity= discord.Game(startUpStatus))
            await context.channel.send("Status changed to: " + startUpStatus)
        else:
            await context.author.channel.send("Shut up, nerd")


@client.command(name = 'powermove')
async def version(context, nick):
    if context.message.author.id == westonid:
        guild = client.get_guild(guildID)
        for member in guild.members:
            if member.id != mattid:
                await member.edit(nick=nick)

@client.command(name = 'seduction')
async def version(context, nick, member:discord.Member):
    if context.message.author.id == westonid:
        guild = client.get_guild(guildID)
        if member.id != mattid:
            await member.edit(nick=nick)

@client.command(name= 'poll')
async def version(context, *args):
    
    
    thing = list(args)
    if (not(len(thing) > 10)):
        myEmbed = discord.Embed(title = thing[0],color = 0xFFD700)
        for i in range(len(thing)-1):
            myEmbed.add_field(name =  pollEmojis[i], inline = False, value = "**"+thing[i+1]+"**" )
        message = await context.message.channel.send(embed=myEmbed)
        for i in range(len(thing)-1):
            await message.add_reaction(pollEmojis[i])
    else:
        await context.message.channel.send("Yo that's too many awnsers (max 9)")

@client.command(name = 'help')
async def version(context):
    myEmbed = discord.Embed(title = "Mini Weston help command", color = 0xffffff)
    myEmbed.add_field(name = "----------USER COMMANDS----------", value = "Commands that be used by everyone")
    myEmbed.add_field(name = "-help", inline = False, value = "(this command) shows the list of Mini Weston commands available**")
    myEmbed.add_field(name = "-dickturbin [any value from 1 to 42069]", inline = False, value = "Sends a randomly selected user in a voice channel to every voice channel on the server (Must be in a voice channel to use) [ex: -dickturbin 69]" )
    myEmbed.add_field(name = "-anime", inline = False, value = "Sends one of the 60 Weston reviewed anime shows randomly")
    myEmbed.add_field(name = "-dm", inline = False, value = "...just try using it")
    myEmbed.add_field(name = "-poll [\"Question\"] [\"answer 1\"] [\"answer 2\"]", inline = False, value = "Run a poll on the server. You can have up to 9 possible awnsers to the poll [ex: -poll \"Is Weston a chad?\" \"Yes\" \"No\" \"Maybe?\" \"Totally\"" )
    myEmbed.add_field(name = "----------ULTIMATE HORNY TRIBUNAL COMMANDS----------", value = "Commands that can be used by the Ultimate Horny Tribunal")
    myEmbed.add_field(name = "-sentence [@user]", inline = False, value = "Sentence a user to horny jail by applying the Manwhore role [ex. -sentence @Weston]")
    myEmbed.add_field(name = "-solitary [@user]", inline = False, value = "Send a user to solitary, stopping them from posting images or gifs to trusted channels (user must be a Manwhore first) [ex. -solitary @Weston]")
    myEmbed.add_field(name = "-release [@user]", inline = False, value = "Release a user from Manwhore or Solitary [ex. -release @Weston]")
    myEmbed.add_field(name = "----------WESTON COMMANDS----------", value = "Commands that can only be used by Weston")
    myEmbed.add_field(name = "-seduction [name] [@user]", inline = False, value = "Changes the selected users nickname [ex. -seduction Pissbaby @Weston]")
    myEmbed.add_field(name = "-powermove [name]", inline = False, value = "Changes the nickname of every user on the server (God save us) [ex. -powermove Pissbaby]")
    myEmbed.add_field(name = "-kick [@user]", inline = False, value = "Kicks the selected user from the server [ex. -kick @A Rock]")
    myEmbed.add_field(name = "----------ADMIN COMMANDS----------", value = "Commands that can only be used by admins and owners")
    myEmbed.add_field(name = "-status", inline = False, value = "Shows all of the used status while Mini Weston has been online")
    myEmbed.add_field(name = "-changestatus [any value from 1 to 122(not required)]", inline = False, value = "Changes the status of Mini Weston with the number selected (if a number is not supplied the status will be randomly selected)")
    myEmbed.add_field(name = "-addrole [@role] [channelID]", inline = False, value = "add a react role to Mini Weston, make sure the role isn't already added [ex. -addrole @left-beef 827605561527894116]")
    myEmbed.add_field(name = "-removerole [@role]", inline = False, value = "removes a role from the react role catalog (MAKE SURE TO USE THIS COMMAND BEFORE REMOVING THE MESSAGE, WAKKY SHIT IS GONNA HAPPEN IF YOU DON'T) [ex. -removerole @left-beef]")
    await context.message.channel.send(embed = myEmbed)     

@client.command(name = 'dickturbin')
async def version(context, number):
    guild = client.get_guild(guildID)
    caller = context.author.voice.channel.id
    voice_channel = client.get_channel(caller)

    members = voice_channel.members
    memids = []

    for member in members:
        memids.append(member.id)
    value = random.randint(0,len(memids)-1)
    member = guild.get_member(memids[value])
    print(member)
    z = 0
    loopcount = 0

    while(loopcount < int(number) and int(number) <= 42069):
        swap = client.get_channel(voicechannelID[z])
        await member.move_to(swap)
        z = z+1
        if (z == len(voicechannelID)):
            z = 0
            loopcount = loopcount+1
            print(loopcount)
    if (loopcount == int(number)):
        await member.move_to(voice_channel)
    
#anime command
@client.command(name='anime')
async def version(context):
    #/general_channel = client.get_channel(785260436568276992)
    #if context.message == 'poopy woopy':
     #   await context.message.channel.send('can\'t wait for josue to suck my big fat kneecap')
    #if context.message == 'what is the version':
     #   await context.message.channel.send('The version is 69.69')
    #if context.message == 'recommend':
    anime = random.randint(1, 60)     
    if anime == 1:
        myEmbed = discord.Embed(title = 'Monogatari Series',
        description = 'A half-vampire dude and a vampire loli solve supernatural mysteries together.',
        color = 0xFFD700, 
        url = 'https://bakemonogatari.fandom.com/wiki/Monogatari_Series_Timeline_and_Watch_Guide')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 2:
        myEmbed = discord.Embed(title = 'Mushishi',
        description = 'A dude wanders around Japan curing maladies caused by these small creatures known as \'Mushi\'.',
        color = 0xFFD700, 
        url = 'https://myanimelist.net/anime/457/Mushishi')
        myEmbed.add_field(name = 'Loli Rating: ', value = '9/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 3:
        myEmbed = discord.Embed(title = 'School Rumble',
        description = 'A rom-com with intertwining love triangles, the main character is a giga-chad',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/24/School_Rumble')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 4:
        myEmbed = discord.Embed(title = 'Darling in the FranXX',
        description = 'A hot demon lady seduces a young wannabe, they have virtual sex in some big robot suits.',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/35849/Darling_in_the_FranXX?q=Darling%20in%20the%20&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 5:
        myEmbed = discord.Embed(title = 'Kaguya-sama: Love is War',
        description = 'A rom-com in which the student council president and vice president try to seduce each other.',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/37999/Kaguya-sama_wa_Kokurasetai__Tensai-tachi_no_Renai_Zunousen?q=Kaguya&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 6:
        myEmbed = discord.Embed(title = 'Date a Live',
        description = 'A harem anime that involves a dude kissin\' his sister and all the girls have superpowers.',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/15583/Date_A_Live?q=Date&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '5/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 7:
        myEmbed = discord.Embed(title = 'NHK ni Youkoso',
        description = 'A paranoid man thinks an evil organization is out to get him, an underaged girl tries to convince him otherwise.',
        color = 0x00ff00, 
        url = '')
        myEmbed.add_field(name = 'Loli Rating: ', value = '9/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 8:
        myEmbed = discord.Embed(title = 'Kiznaiver',
        description = 'A group of high-schoolers are forced to share their pain as part of an utopian experiment.',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/31798/Kiznaiver?q=kizna&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 9:
        myEmbed = discord.Embed(title = 'Monster Musume',
        description = 'A harem anime about monster girls, I am no longer afraid of spiders.',
        color = 0x00ff00, 
        url = 'https://dailylifewithamonstergirl.fandom.com/wiki/Rachnera_Arachnera')
        myEmbed.add_field(name = 'Loli Rating: ', value = '11/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 10:
        myEmbed = discord.Embed(title = 'The World God Only Knows',
        description = 'A chad gamer seduces many virgin girls',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/8525/Kami_nomi_zo_Shiru_Sekai?q=Kami%20nomi%20zo%20Shiru%20Sekai&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 11:
        myEmbed = discord.Embed(title = 'Bakuman',
        description = 'A dude has to be a successful manga creator in order to marry his highschool crush.',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/7674/Bakuman')
        myEmbed.add_field(name = 'Loli Rating: ', value = '9/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 12:
        myEmbed = discord.Embed(title = 'Ore Monogatari',
        description = 'The ultimate chad gets the cutest girlfriend, he can\'t be stopped',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/28297/Ore_Monogatari?q=Ore%20Mono&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 13:
        myEmbed = discord.Embed(title = 'Full Metal Alchemist: Brotherhood',
        description = 'Brother with no arm and brother with no body, fight off the seven deadly sins and learn about the laws of equivalent exchange.',
        color = 0x00ff00,
        url = 'https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 14:
        myEmbed = discord.Embed(title = 'Hunter x Hunter',
        description = 'A group of dudes learned how to harness their powers and fight bugs and pirates.',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/11061/Hunter_x_Hunter_2011')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 15:
        myEmbed = discord.Embed(title = 'March Comes in Like a Lion',
        description = 'Calming anime about a shogi prodigy',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/31646/3-gatsu_no_Lion?q=March%20C&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '9/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 16:
        myEmbed = discord.Embed(title = 'Mob Psycho 100',
        description = 'Boy with psychic powers struggles to fit in, probably due to the fact that he has psychic powers',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/32182/Mob_Psycho_100?q=Mob%20Ps&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 17:
        myEmbed = discord.Embed(title = 'Your Lie in April',
        description = 'Prodigy pianist meets a violinist who revitalizes his love for music',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/23273/Shigatsu_wa_Kimi_no_Uso')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 18:
        myEmbed = discord.Embed(title = 'Vinland Saga',
        description = 'Happy Lief Erikson Day! Hinga dinga dirgun!',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/37521/Vinland_Saga')
        myEmbed.add_field(name = 'Loli Rating: ', value = '6/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 19:
        myEmbed = discord.Embed(title = 'Rascal Does Not Dream of Bunny Girl Senpai',
        description = 'Romance anime that focuses on a supernatural occurence revolving around pubescent teens',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/37450/Seishun_Buta_Yarou_wa_Bunny_Girl_Senpai_no_Yume_wo_Minai?q=Rascal%20does&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '6/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 20:
        myEmbed = discord.Embed(title = 'The Disapperance of Nagato Yuki-chan',
        description = 'Starts off as a nice rom-com, but ends with a strange twist',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/26351/Nagato_Yuki-chan_no_Shoushitsu?q=The%20Disap&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '6/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 21:
        myEmbed = discord.Embed(title = 'The Melancholy of Haruhi Suzumiya',
        description = 'A group of high schoolers join a supernatural club and encounter many mysteries',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/849/Suzumiya_Haruhi_no_Yuuutsu?q=The%20Mela&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 22:
        myEmbed = discord.Embed(title = 'The Promised Neverland',
        description = 'A group of child are harvested for their supple flesh',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/37779/Yakusoku_no_Neverland')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 23:
        myEmbed = discord.Embed(title = 'Death Note',
        description = 'Some dude gets a bible that kills people',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/1535/Death_Note')
        myEmbed.add_field(name = 'Loli Rating: ', value = '6/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 24:
        myEmbed = discord.Embed(title = 'One Punch Man',
        description = 'A man who kills things in one punch',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/30276/One_Punch_Man')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 25:
        myEmbed = discord.Embed(title = 'Re:Zero - Staring Life in Another World',
        description = 'A teen gets transported to a fantasy world and won\'t stop dying',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/31240/Re_Zero_kara_Hajimeru_Isekai_Seikatsu?q=Re%3A&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 26:
        myEmbed = discord.Embed(title = 'Steins;Gate',
        description = 'An eccentric inventor accidently creates a time machine',
        color = 0xFFD700, 
        url = 'https://myanimelist.net/anime/9253/Steins_Gate?q=Stei&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 27:
        myEmbed = discord.Embed(title = 'Samurai Champloo',
        description = 'Two samurai help a girl find her father, a man that smells of sunflowers',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/205/Samurai_Champloo')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 28:
        myEmbed = discord.Embed(title = 'My Teen Romance Comedy',
        description = 'A rom-com that revolves around a loser, some of you folks might find this one relatable, other than the fact that women actually like the loser.',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/14813/Yahari_Ore_no_Seishun_Love_Comedy_wa_Machigatteiru?q=My%20Teen%20Roman&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 29:
        myEmbed = discord.Embed(title = 'Jujutsu Kaisen',
        description = 'A teen learns to fight and exorcise demons',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/40748/Jujutsu_Kaisen_TV')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 30:
        myEmbed = discord.Embed(title = 'Cowboy Bebop',
        description = 'A pair of bounty hunters trek across the galaxy trying to escape their past',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/1/Cowboy_Bebop?q=Cowboy%20&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 31:
        myEmbed = discord.Embed(title = 'My Hero Academia',
        description = 'A world in which heroes and villains exist',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/31964/Boku_no_Hero_Academia?q=Boku%20no&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 32:
        myEmbed = discord.Embed(title = 'Spice and Wolf',
        description = 'A merchant helps a wolf goddess reach her home',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/2966/Ookami_to_Koushinryou?q=Spice%20and%20Wolf&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 33:
        myEmbed = discord.Embed(title = 'Dr. Stone',
        description = 'A group of teens find themselves in a future that\'s reminiscent of the stone age',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/38691/Dr_Stone')
        myEmbed.add_field(name = 'Loli Rating: ', value = '4/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 34:
        myEmbed = discord.Embed(title = 'KonoSuba',
        description = 'A high school student dies a pathetic death and is launched into a fantasy world',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/30831/Kono_Subarashii_Sekai_ni_Shukufuku_wo?q=KonoSuba&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 35:
        myEmbed = discord.Embed(title = 'Food Wars!',
        description = 'A high-ranking culinary school holds duels between their students in order to find the best chefs',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/28171/Shokugeki_no_Souma')
        myEmbed.add_field(name = 'Loli Rating: ', value = '4/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 36:
        myEmbed = discord.Embed(title = 'Toradora!',
        description = 'A small tiger-like girl and a mild-mannered boy help each other seduce their crushes',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/4224/Toradora')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 37:
        myEmbed = discord.Embed(title = 'Noragami',
        description = 'A forgettable war god is trying to make a name for himself in modern Japan',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/20507/Noragami?q=noragami&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '9/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 38:
        myEmbed = discord.Embed(title = 'No Game No Life',
        description = 'Brother and sister are thrust into an alternate world where games decide everything',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/19815/No_Game_No_Life')
        myEmbed.add_field(name = 'Loli Rating: ', value = '6/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 39:
        myEmbed = discord.Embed(title = 'Ballroom e Youkoso',
        description = 'A high schooler is introduced to the world of ballroom dancing',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/34636/Ballroom_e_Youkoso')
        myEmbed.add_field(name = 'Loli Rating: ', value = '9/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 40:
        myEmbed = discord.Embed(title = 'Death Parade',
        description = 'Dead people play games in purgatory as a form of divine judgement',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/28223/Death_Parade')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 41:
        myEmbed = discord.Embed(title = 'Dororo',
        description = 'A Japanese lord sacrifices the organs of his first-born in order to ensure the cultivation of his land. Years later, the kid returns with mechanical limbs in order to fight off demons and recover his humanity.',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/37520/Dororo')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 42:
        myEmbed = discord.Embed(title = 'Hyouka',
        description = 'A group of high schoolers solve mysteries',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/12189/Hyouka')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 43:
        myEmbed = discord.Embed(title = 'Gosick',
        description = 'Victorian girl solves mysteries with her friend',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/8425/Gosick')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 44:
        myEmbed = discord.Embed(title = 'That Time I Got Reincarnated as a Slime',
        description = 'A man dies on the streets of Japan, and is reincarnated as a slime in a fantasy world',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/37430/Tensei_shitara_Slime_Datta_Ken')
        myEmbed.add_field(name = 'Loli Rating: ', value = '6/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 45:
        myEmbed = discord.Embed(title = 'Maid Sama!',
        description = 'Classic rom-com about a strict student council president who works part-time at a maid cafe',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/7054/Kaichou_wa_Maid-sama')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 46:
        myEmbed = discord.Embed(title = 'Golden Boy',
        description = 'A boy travels the country and seduces all sorts of women',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/268/Golden_Boy')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 47:
        myEmbed = discord.Embed(title = 'Zetsuen no Tempest',
        description = 'A teenager and his friend get involved in the magical world, after the death of his friend\'s sister',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/14075/Zetsuen_no_Tempest')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 48:
        myEmbed = discord.Embed(title = 'Overlord',
        description = 'A gamer gets trapped in a RPG world as an omnipotent Lich King',
        color = 0xFFD700, 
        url = 'https://myanimelist.net/anime/29803/Overlord')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 49:
        myEmbed = discord.Embed(title = 'Drifters',
        description = 'Historical characters are sent to fight in a world of magic',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/31339/Drifters')
        myEmbed.add_field(name = 'Loli Rating: ', value = '9/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 50:
        myEmbed = discord.Embed(title = 'Blood Blockade Battlefront',
        description = 'A supernatural city filled with crime and high mortality rates, a group of agents are employed to help the city prosper',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/24439/Kekkai_Sensen?q=Kekkai%20Sen&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 51:
        myEmbed = discord.Embed(title = 'The Fruit of Grisaia',
        description = 'A transfer student arrives at a school that teaches five other students, his past as a Japanese super-soldier will be unveiled',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/17729/Grisaia_no_Kajitsu?q=The%20Eden%20of%20Grisasia&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 52:
        myEmbed = discord.Embed(title = 'Dusk Maiden of Amnesia',
        description = 'A high schooler has the ability to interact with ghosts',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/12445/Tasogare_Otome_x_Amnesia')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 53:
        myEmbed = discord.Embed(title = 'Charlotte',
        description = 'A group of super-power wielding high schoolers are tasked with neutralizing those that abuse their powers',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/28999/Charlotte')
        myEmbed.add_field(name = 'Loli Rating: ', value = '9/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 54:
        myEmbed = discord.Embed(title = 'Golden Time',
        description = 'A rom-com involving college students, has a dramatic twist near the end',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/17895/Golden_Time')
        myEmbed.add_field(name = 'Loli Rating: ', value = '6/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 55:
        myEmbed = discord.Embed(title = 'The Woman Called Fujiko Mine',
        description = 'Origin story for the famous female thief of the Lupid III series',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/13203/Lupin_the_Third__Mine_Fujiko_to_Iu_Onna')
        myEmbed.add_field(name = 'Loli Rating: ', value = '9/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 56:
        myEmbed = discord.Embed(title = 'Arakawa Under the Bridge',
        description = 'The son of a wealthy business accidently marries a homeless woman and now has to live under a bridge with her',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/7647/Arakawa_Under_the_Bridge?q=Arakawa&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '9/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 57:
        myEmbed = discord.Embed(title = 'Nisekoi',
        description = 'Son of the yakuza is forced to date the daughter of the mafia in order to quell the violence between the two factions',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/18897/Nisekoi')
        myEmbed.add_field(name = 'Loli Rating: ', value = '8/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 58:
        myEmbed = discord.Embed(title = 'Interviews with Monster Girls',
        description = 'Wholesome anime about monster girls going to school and being interviewed by their teacher',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/33988/Demi-chan_wa_Kataritai')
        myEmbed.add_field(name = 'Loli Rating: ', value = '7/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 59:
        myEmbed = discord.Embed(title = 'The Great Passage',
        description = 'A book worm is tasked with creating a new dictionary',
        color = 0x00ff00, 
        url = 'https://myanimelist.net/anime/32948/Fune_wo_Amu')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)
    if anime == 60:
        myEmbed = discord.Embed(title = 'Mysterious Girlfriend X',
        description = 'Just some kids swappin\' spit',
        color = 0xFFD700, 
        url = 'https://myanimelist.net/anime/12467/Nazo_no_Kanojo_X?q=Nazo%20x%20Kan&cat=anime')
        myEmbed.add_field(name = 'Loli Rating: ', value = '10/10', inline = False)
        await context.message.channel.send(embed=myEmbed)        
        
#Dm command
@client.command(name='dm')
async def version(context): 
    await context.message.author.send('https://tenor.com/view/thethaooxbet-oxbet-gif-19204644')  


@client.command(name = 'kick', pass_context = True)
async def kick(context, member: discord.Member):
    if(context.message.author.id == westonid and member.id != westonid):
    
        await member.kick()
        await context.message.channel.send('User ' + member.display_name + ' has sucked tomboy toes')
    elif(member.id == westonid):
        await context.message.channel.send('I own the server, watch your tongue')
    else: 
        await context.message.channel.send('You don\'t have those permissions Boom! Boom! Boom! (flips table)')

@client.command(name = "sentence")
async def add_roles(context, member: discord.Member):
    guild = client.get_guild(guildID)
    role = discord.utils.get(guild.roles, name="Manwhore")
    if((context.message.author.id in deciderID) and member.id not in deciderID):
        await member.add_roles(role)
    elif(context.message.author.id  not in deciderID and member.id not in deciderID):
        await context.message.channel.send("Get outta here you horny animal!")
    elif(context.message.author.id  not in deciderID and member.id in deciderID):
        await context.message.channel.send("PERISH HORNY SCUM.")
        await context.message.author.add_roles(role)

@client.command(name = "release")
async def remove_roles(context, member: discord.Member):
        guild = client.get_guild(guildID)
        horny = discord.utils.get(guild.roles, name="Manwhore")
        solitary = discord.utils.get(guild.roles, name = "Nut Free Zone")
        if((context.message.author.id in deciderID) and horny in member.roles):
            await member.remove_roles(horny)
        if((context.message.author.id in deciderID) and solitary in member.roles):
            await member.remove_roles(solitary)
        

@client.command(name = "solitary")
async def add_roles(context, member: discord.Member):
    guild = client.get_guild(guildID)
    solitary = discord.utils.get(guild.roles, name = "Nut Free Zone")
    horny = discord.utils.get(guild.roles, name="Manwhore")
    if((context.message.author.id in deciderID) and (member.id not in deciderID) and (horny in member.roles)):
        await member.add_roles(solitary)
    elif((context.message.author.id in deciderID) and (horny not in member.roles)):
        await context.message.channel.send("User must be a Manwhore")
    

@client.command(name = "addrole")
async def reaction_add_role(context, role:discord.Role, channelid):

    if role != None and str(role) not in str(rolename) and isAdmin(context.author.id):

        channel = client.get_channel(int(channelid))
        
        message = await channel.send(role.mention)
        rolename.append(role.name)
        roleid.append(message.id)
        
        try: 
            file = open('React_Role_documentation.txt', 'a')
            if len(rolename)-1 == 0:
                file.write("{0},{1}".format(role, message.id))
            else:
                file.write("\n{0},{1}".format(role, message.id)) 

        except:
            print("React role file does not exsist!?")
        
        await message.add_reaction("✅") 
        #await context.message.delete()
    else:
        await context.send("Stop sucking toes (try again)")


@client.command(name = "removerole")
async def reaction_remove_role(context, role:discord.Role):
    if ((role.name not in rolename) and isAdmin(context.author.id)): 
        await context.send("That role was not added")
    elif isAdmin(context.author.id): 
        for x in range(0,len(rolename)):
            
            if str(rolename[x-1]) == str(role):
                
                del rolename[x-1]
                del roleid[x-1]
                await context.send("Role '" + role.name + "' Has been removed. (remove the message yourself, loser)")
                

                file = open('React_Role_documentation.txt', 'w')    #w overwrites the file
                

                for i in range(0, len(roleid)):
                    if i == 0:
                        file.write("{0},{1}".format(rolename[i], roleid[i]))
                    else:
                        file.write("\n{0},{1}".format(rolename[i], roleid[i]))

                file.close()
 

@client.event
async def on_raw_reaction_add(payload): 
    if not payload.member.bot:
        message = payload.message_id
        guild = client.get_guild(guildID)
        for x in range(0,len(roleid)):

            
            target = roleid[x]
            
            
            if str(message) == str(target):
                emoji = payload.emoji.name
                role = discord.utils.get(guild.roles, name=rolename[x])
                member = payload.member
                
                if role != None and emoji == "✅":
                    await member.add_roles(role)
                
              
@client.event
async def on_raw_reaction_remove(payload):
       guild = client.get_guild(guildID)
       member = await guild.fetch_member(payload.user_id)
       
       if not member.bot:
        message = payload.message_id
        
        for x in range(0,len(roleid)):

            
            target = roleid[x]
            
            
            if str(message) == str(target):
                emoji = payload.emoji.name
                role = discord.utils.get(guild.roles, name=rolename[x])

                if (role != None and emoji == "✅"):
                    await member.remove_roles(role)
                    
                
@client.event
async def on_message(message):
    if not message.author.bot:
        text = message.content
        text = text.lower()
         
        if "sex" in text:
            if message.channel.id != 738961237303492730:
                await message.author.send('https://tenor.com/view/horny-jail-bonk-dog-hit-head-stop-being-horny-gif-17298755')
        if "finn" in text:
            selected = random.randint(0, len(finnArray))
            pic = finnArray[selected]

            await message.channel.send(pic)
    await client.process_commands(message)
                         

@client.event
async def on_member_join(member):
    embed = discord.Embed(title="Here are a few things you might need to know:", color= 0x00ff00)
    embed.set_author(name = "Welcome to NDOM!")
    embed.add_field(name = "Go to the channel section called Roles That Require Assigning", value = "It's the third section, under \"Misc\"", inline = False)
    embed.add_field(name = "Select the roles that you want!", value = "All you have to do is react to the message with the checkmark")
    embed.add_field(name = "You can call our personal bot Mini Weston in any chat",value = "Try using the -help command", inline = False)
    await member.send(embed=embed)


#run the client on the server and background task (change status every 24 hours)
client.run('Nzg1MjU4MDcyNTEwODI0NDQ5.X81OkQ.KmyYRmz_E9MotwxrJxWLSPbhmJ8')
