import discord
from discord.ext import commands, tasks
import os
from keep_alive import keep_alive
from sqlalchemy import create_engine, select
import sqlalchemy as db
import random

#connecting the database

engine = create_engine('sqlite:///name_list', echo=True)
metadata_obj = db.MetaData()
name_list = db.Table('name_list', metadata_obj, db.Column('name', db.String))

conn = engine.connect()

metadata_obj.create_all(engine)

#bot prefix & intents

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#activity, logged in

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(
                                     type=discord.ActivityType.watching,
                                     name='Hello World!'))
    print('Logged in as {0.user}'.format(client))


#welcoming with random message when a user joins the server

@client.event
async def on_member_join(member):
    welcome_messages = [
        f'{member.mention} slid into this server',
        f'Hello there {member.mention}. The server welcomes you',
        f'{member.mention} has joined the server'
    ]
    welcome_channel = client.get_channel(898188608593330177)
    await welcome_channel.send(random.choice(welcome_messages))


#error handling

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all the required values!')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('Command does not exist!')
    else:
        pass


#ping pong

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


#sends a message on the same channel

@client.event
async def on_raw_reaction_add(payload):
    message = await client.get_channel(payload.channel_id
                                       ).fetch_message(payload.message_id)
    emoji = payload.emoji
    user = payload.user_id

    channel = client.get_channel(payload.channel_id)
    await channel.send(
        f'<@{user}> reacted with {emoji} to {message.author.mention}')


#create a role and add the role to the user

@client.command()
async def newrole(ctx, *, role):
    await ctx.guild.create_role(name=role)
    role = discord.utils.get(ctx.guild.roles, name=f'{role}')
    await ctx.author.add_roles(role)
    await ctx.send(
        f' The role "{role.mention}" has been added to {ctx.author.mention}')


#new name registering

@client.command()
async def register(ctx, *, new_name):

    s = select(name_list.c.name).where(name_list.c.name == new_name)
    result1 = conn.execute(s)
    a = 0     #supplied a variable to initiate the for loop
    for row in result1:
        a = a + 1
    if a == 0:
        ins = name_list.insert().values(name=str(new_name))
        result2 = conn.execute(ins)
        await ctx.send(f'"{new_name}" has been Registered Successfully!')
    else:
        await ctx.send(
            f'Error! "{new_name}" has already been Registered. Use a different Name!'
        )       #error message


#check name_list(only for admins)

@client.command()
@commands.has_permissions(administrator=True)
async def names(ctx):
    s = select(name_list.c.name)
    result = conn.execute(s)

    for row in result:
        names = str(row)
        names = names[2:-3]
        await ctx.send(names)


keep_alive()      #don't mind this

client.run(os.environ["TOKEN"])     #token stored as environment variable