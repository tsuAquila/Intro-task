import discord
from discord.ext import commands, tasks
import os
from keep_alive import keep_alive

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


#activity, logged in


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Activity(
                                     type=discord.ActivityType.watching,
                                     name='Over this Server'))
    print('Logged in as {0.user}'.format(client))


#member join


@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(898188608593330177)
    await welcome_channel.send(f'{member.mention} has joined the server')


#error_handling


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


#message_reaction

@client.event
async def on_reaction_add(reaction, user):
    channel= client.get_channel(898188608593330177)
    await channel.send(f'{user} {reaction}')


#add created role to the user

@client.command()
async def newrole(ctx, *, role):
  await ctx.guild.create_role(name = role)
  role = discord.utils.get(ctx.guild.roles, name=f'{role}')
  await ctx.author.add_roles (role)
  await ctx.send(f' The {role.mention} has been added to {ctx.author.mention}')


keep_alive()

client.run(os.environ['TOKEN'])
