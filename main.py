import os
import discord
from discord.ext import commands
from datetime import datetime
from keep_alive import keep_alive

keep_alive()

intents = discord.Intents.default()
intents.members = True  # Enables member-related events
intents.message_content = True  # Enables message content events

bot = commands.Bot(command_prefix='!', intents=intents)

# Define your logging channel ID here
LOG_CHANNEL_ID = 1285589621379436544  # Replace with your actual log channel ID

# Helper function to send log messages
async def send_log(embed):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed)
    else:
        print("Log channel not found.")

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

def get_time_info():
    now = datetime.utcnow()
    gmt_time = now.strftime('%d/%m/%Y, %H:%M:%S')
    return gmt_time

# Command: Kick a member
@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = 'No reason provided'
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention} for {reason}')

    gmt_time = get_time_info()
    embed = discord.Embed(title='Member Kicked', color=discord.Color.orange())
    embed.add_field(name='**User**', value=f'{member} ({member.id})\n')
    embed.add_field(name='**Kicked By**', value=f'{ctx.author}\n')
    embed.add_field(name='**Reason**', value=f'{reason}\n')
    embed.add_field(name='**GMT Time**', value=f'{gmt_time}\n')

    await send_log(embed)

# Command: Ban a member
@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = 'No reason provided'
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention} for {reason}')

    gmt_time = get_time_info()
    embed = discord.Embed(title='Member Banned', color=discord.Color.red())
    embed.add_field(name='**User**', value=f'{member} ({member.id})\n')
    embed.add_field(name='**Banned By**', value=f'{ctx.author}\n')
    embed.add_field(name='**Reason**', value=f'{reason}\n')
    embed.add_field(name='**GMT Time**', value=f'{gmt_time}\n')

    await send_log(embed)

# Command: Unban a member
@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, member_id: int):
    banned_users = await ctx.guild.bans()
    member = discord.utils.get(banned_users, id=member_id)
    if member:
        await ctx.guild.unban(member.user)
        await ctx.send(f'Unbanned {member.user.mention}')

        gmt_time = get_time_info()
        embed = discord.Embed(title='Member Unbanned', color=discord.Color.green())
        embed.add_field(name='**User**', value=f'{member.user} ({member.user.id})\n')
        embed.add_field(name='**Unbanned By**', value=f'{ctx.author}\n')
        embed.add_field(name='**GMT Time**', value=f'{gmt_time}\n')

        await send_log(embed)
    else:
        await ctx.send('User not found in the banned list.')

# Command: Mute a member
@bot.command(name='mute')
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = 'No reason provided'
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if mute_role is None:
        mute_role = await ctx.guild.create_role(name='Muted')

        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mute_role)
    await ctx.send(f'Muted {member.mention} for {reason}')

    gmt_time = get_time_info()
    embed = discord.Embed(title='Member Muted', color=discord.Color.blue())
    embed.add_field(name='**User**', value=f'{member} ({member.id})\n')
    embed.add_field(name='**Muted By**', value=f'{ctx.author}\n')
    embed.add_field(name='**Reason**', value=f'{reason}\n')
    embed.add_field(name='**GMT Time**', value=f'{gmt_time}\n')

    await send_log(embed)

# Command: Unmute a member
@bot.command(name='unmute')
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if mute_role is not None:
        await member.remove_roles(mute_role)
        await ctx.send(f'Unmuted {member.mention}')

        gmt_time = get_time_info()
        embed = discord.Embed(title='Member Unmuted', color=discord.Color.purple())
        embed.add_field(name='**User**', value=f'{member} ({member.id})\n')
        embed.add_field(name='**Unmuted By**', value=f'{ctx.author}\n')
        embed.add_field(name='**GMT Time**', value=f'{gmt_time}\n')

        await send_log(embed)
    else:
        await ctx.send('Mute role not found.')

# Start the bot
bot.run(os.getenv('DISCORD_TOKEN'))
