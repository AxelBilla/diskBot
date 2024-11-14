#https://discord.com/oauth2/authorize?client_id=1306356201017184298

import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from random import randint
from private.config import token

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
dir = os.path.dirname(__file__)

@bot.event
async def on_ready():
    await bot.tree.sync()    

@bot.tree.command(name='disk', description="Display a random line from the server's saved pickup lines.")
async def returnHorn(ctx):
    file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.json", "r")
    wordList=file.readlines()
    if len(wordList)==0:
        await ctx.response.send_message("I don't have anything to say.")
    else:
        await ctx.response.send_message(wordList[randint(0,int(len(wordList)-1))])

@bot.tree.command(name='add_disk', description="Add a new line to the server's saved pickup lines.")
@app_commands.checks.has_permissions(administrator=True)
async def addHorn(ctx, txt: str):
    path = dir+"/serverData/" + str(ctx.guild.id)
    if not os.path.exists(path):
        os.makedirs(path)
        open(path+"/data.json","w")
    file = open(path + "/" + "data.json", "a")
    file.write(txt+"\n")
    await ctx.response.send_message(f"\"{txt}\" was successfully added!", ephemeral=True)
    
@bot.tree.command(name='del_disk', description="Remove a line by its content or id from the server's saved pickup lines (* to remove every line).")
@app_commands.checks.has_permissions(administrator=True)
async def addHorn(ctx, txt: str):
    file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.json", "r")
    wordList=file.readlines()
    check=True
    if len(wordList)==0:
        await ctx.response.send_message("You currently do not have any saved pickup lines.", ephemeral=True)
    elif txt=="*":
        wordList=[]
        fileWrite = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.json", "w")
        fileWrite.writelines(wordList)
        await ctx.response.send_message(f"Saved pick up lines successfully cleared!", ephemeral=True)
    else:
        for i in range(len(wordList)):
            if wordList[i]==txt+"\n" or str(i+1)==txt:
                wordList.pop(i)
                fileWrite = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.json", "w")
                fileWrite.writelines(wordList)
                await ctx.response.send_message(f"\"{txt}\" was successfully removed!", ephemeral=True)
                check=False
                break
        if check:
            await ctx.response.send_message(f"\"{txt}\" couldn't be found!")

@bot.tree.command(name='see_disk', description="Display a list of a server's saved pickup lines.")
@app_commands.checks.has_permissions(administrator=True)
async def checkHorn(ctx):
    file = open(dir+"/serverData/" + str(ctx.guild.id) + "/" + "data.json", "r")
    wordList=file.readlines()
    outString=""
    if len(wordList)==0:
        await ctx.response.send_message("You currently do not have any saved pickup lines.", ephemeral=True)
    else:
        for i in range(len(wordList)):
            wordList[i]=wordList[i].strip("\n")
            outString=outString+f"[{i+1}]: \"{wordList[i]}\"\n"
        await ctx.response.send_message(outString, ephemeral=True)

bot.run(token)