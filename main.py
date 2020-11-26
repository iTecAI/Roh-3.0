import discord
from roh import Roh
import random

client = discord.Client()
bot = Roh('data.json')
allowed_channels = [781487902244470784]
running = False
running_ct = 0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global running, running_ct
    if message.author == client.user:
        return

    if 'roh' in message.content.lower():
        running = True
        running_ct = 0
    
    if (running_ct > 10 and random.randint(0,20) == 15) or ('bye' in message.content and running):
        running = False
        await message.channel.send('Bye.')
        bot._store()

    if message.channel.id in allowed_channels and running:   
        await message.channel.send(bot.interpret(message.content))

with open('token','r') as f:
    client.run(f.read())