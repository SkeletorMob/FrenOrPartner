# bot.py
import os
from dotenv import load_dotenv
import discord
from discord import app_commands
import sqlite3
from lucky_functions import calculate_lucky_name, calculate_lucky_bday

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

conn = sqlite3.connect('users.db')
conn.execute('''CREATE TABLE IF NOT EXISTS users
                 (discord_id TEXT, guild_id TEXT, username TEXT,
                  lucky_name INTEGER, lucky_bday INTEGER,
                  UNIQUE(discord_id, guild_id))''')

# Load presidents once at startup
presidents_list = []
with open('presidents.csv') as f:
    for line in f:
        if line.strip():
            fields = line.strip().split(',')
            pres_name = fields[1]
            pres_bday = fields[2]
            presidents_list.append({
                'name': pres_name,
                'lucky_name': calculate_lucky_name(pres_name.lower()),
                'lucky_bday': calculate_lucky_bday(pres_bday)
            })


@tree.command(name="luckybyname", description="Calculate your lucky number from your name")
async def luckybyname(interaction: discord.Interaction, name: str):
    result = calculate_lucky_name(name.lower())
    conn.execute('''INSERT INTO users (discord_id, guild_id, username, lucky_name)
                     VALUES (?, ?, ?, ?)
                     ON CONFLICT(discord_id, guild_id)
                     DO UPDATE SET username=excluded.username, lucky_name=excluded.lucky_name''',
                 (str(interaction.user.id), str(interaction.guild.id), interaction.user.name, result))
    conn.commit()
    await interaction.response.send_message(f"Your lucky number by name is: {result}")


@tree.command(name="luckybydate", description="Calculate your lucky number from your birthdate")
async def luckybydate(interaction: discord.Interaction, birthdate: str):
    result = calculate_lucky_bday(birthdate)
    conn.execute('''INSERT INTO users (discord_id, guild_id, username, lucky_bday)
                     VALUES (?, ?, ?, ?)
                     ON CONFLICT(discord_id, guild_id)
                     DO UPDATE SET username=excluded.username, lucky_bday=excluded.lucky_bday''',
                 (str(interaction.user.id), str(interaction.guild.id), interaction.user.name, result))
    conn.commit()
    await interaction.response.send_message(f"Your lucky number by birthdate is: {result}")


@tree.command(name="compatiblefriends", description="Find server members matching your lucky number")
@app_commands.choices(match_type=[
    app_commands.Choice(name="Friend (by name)", value="friend"),
    app_commands.Choice(name="Collaborator (by birthdate)", value="collaborator"),
])
async def compatiblefriends(interaction: discord.Interaction, match_type: app_commands.Choice[str]):
    guild_id = str(interaction.guild.id)
    user_id = str(interaction.user.id)

    row = conn.execute('SELECT lucky_name, lucky_bday FROM users WHERE discord_id=? AND guild_id=?',
                        (user_id, guild_id)).fetchone()
    if not row:
        await interaction.response.send_message("Run /luckybyname or /luckybydate first!")
        return

    lucky_name, lucky_bday = row

    if match_type.value == "friend":
        if lucky_name is None:
            await interaction.response.send_message("Run /luckybyname first!")
            return
        column, target, label = "lucky_name", lucky_name, "name"
    else:
        if lucky_bday is None:
            await interaction.response.send_message("Run /luckybydate first!")
            return
        column, target, label = "lucky_bday", lucky_bday, "birthdate"

    matches = conn.execute(f'SELECT username FROM users WHERE guild_id=? AND {column}=? AND discord_id != ?',
                            (guild_id, target, user_id)).fetchall()

    if matches:
        names = "\n".join(f"     {m[0]}" for m in matches)
    else:
        names = "     no one yet"

    await interaction.response.send_message(f"Server members sharing lucky {label} ({target}):\n{names}")


@tree.command(name="compatiblepresidents", description="Find presidents matching your lucky number")
@app_commands.choices(match_type=[
    app_commands.Choice(name="Friend (by name)", value="friend"),
    app_commands.Choice(name="Collaborator (by birthdate)", value="collaborator"),
])
async def compatiblepresidents(interaction: discord.Interaction, match_type: app_commands.Choice[str]):
    guild_id = str(interaction.guild.id)
    user_id = str(interaction.user.id)

    row = conn.execute('SELECT lucky_name, lucky_bday FROM users WHERE discord_id=? AND guild_id=?',
                        (user_id, guild_id)).fetchone()
    if not row:
        await interaction.response.send_message("Run /luckybyname or /luckybydate first!")
        return

    lucky_name, lucky_bday = row

    if match_type.value == "friend":
        if lucky_name is None:
            await interaction.response.send_message("Run /luckybyname first!")
            return
        matches = [p['name'] for p in presidents_list if p['lucky_name'] == lucky_name]
        label = "name"
        target = lucky_name
    else:
        if lucky_bday is None:
            await interaction.response.send_message("Run /luckybydate first!")
            return
        matches = [p['name'] for p in presidents_list if p['lucky_bday'] == lucky_bday]
        label = "birthdate"
        target = lucky_bday

        if matches:
            names = "\n".join(f"     {m}" for m in matches)
        else:
            names = "     no one"

    await interaction.response.send_message(f"Presidents sharing your lucky {label} ({target}):\n{names}")


@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")


client.run(os.environ["DISCORD_BOT_TOKEN"])