#831621574675267597
import sqlite3
import discord
from discord.ext import commands
import config
import os
from os import system
import platform
from data.script.userdata import DataHandler
from data.script.serverdata import DataHandlerServeur
from data.script.reactiondata import DataHandlerReaction
from data.script.economydata import DataHandlerEconomy
from data.script.inventorydata import DataHandlerInventory
from data.script.data_config import DataHandlerConfig
import requests
import time
from datetime import datetime
from discord import File
from easy_pil import Editor, load_image_async, Font, load_image
from discord.app_commands import Choice
from discord import app_commands
import xml.etree.ElementTree as ET
from pypresence import Presence
import asyncio
from io import BytesIO
from PIL import Image

color = int(0xdb9721)
datauser = DataHandler(r"data/userdata.db")
serverdata = DataHandlerServeur(r"data/serveurdata.db")
reactiondata = DataHandlerReaction(r"data/reaction.db")
economydata = DataHandlerEconomy(r"data/economydata.db")
inventory = DataHandlerInventory(r"data/inventory.db")
configdata = DataHandlerConfig(r"data/config.db")

y = True


if platform.system() == "Windows":
    def clearcmd():
        os.system("cls")
if platform.system() == 'Linux':
    def clearcmd():
        os.system("clear")

def plugin_money_active(server: str):
    if serverdata.ifmoneyactivate(server=str(server)) == "y":
        return y
    else:
        return False

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-',
                   description="Bot by Xerty", intents=intents)
bot.remove_command('help')
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

# ------- commande slash -------


class Select(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Aide débutant",
                emoji="🆕",
                description="De l'aide pour connaitre les commande de base"
            ),
            discord.SelectOption(
                label="Aide Economie",
                emoji="🪙",
                description="De l'aide sur les commande concernant l'economie"  #56
            ),
            discord.SelectOption(
                label="Aide Administration",
                emoji="🛠️",
                description="De l'aide sur les outils d'administration"
            ),
            discord.SelectOption(
                label="Aide Jobs",
                emoji="👜",
                description="De l'aide sur le system de jobs"
            )
        ]
        super().__init__(placeholder="Sélectione une option",
                         max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Aide débutant":
            embed = discord.Embed(
                title="**Voici les commande les plus importante :**", color=color
            )
            embed.add_field(
                name="`/money`",
                value="Permet de savoir combien tu a de boblux",
                inline=False
            ),
            embed.add_field(
                name="`/shops`",
                value="Permet de voir les shops si il y en a sur le server",
                inline=False
            )
            embed.add_field(
                name="`/leadboard`",
                value="Permet de savoir si tu est top 1 server ou pas 🚫",
                inline=False

            )
            embed.add_field(
                name="**Pour plus de pricision n'hesite pas a aller voir notre **",
                value="**[wiki](https://bobluxcorp.000webhostapp.com/wiki/)**",
                inline=False
            )
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "Aide Administration":
            embed = discord.Embed(
                title="**Voici les commande d'administration :**", color=color
            )
            embed.add_field(
                name="`/clear {amount}`",
                value="Permet de clear {amount} message ou {all} qui permet de tout clear",
                inline=False
            )
            embed.add_field(
                name="`/create_shops`",
                value="Permet de créer un shops avec les option [name] [description]",
                inline=False
            )
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "Aide Economie":
            embed = discord.Embed(
                title="**Voici les commande concernant l'economie :**", color=color
            )
            embed.add_field(
                name="`/active_money`",
                value="Permet d'activer le plugin d'economie'",
                inline=False
            )
            embed.add_field(
                name="`/shop {shop}`",
                value="Permet de voir les item d'un shop !",
                inline=False
            )
            embed.add_field(
                name="`/buy {shop} {item}`",
                value="Permet d'achter un item si tu a asser d'argent !",
                inline=False
            )
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == "Aide Jobs":
            embed = discord.Embed(
                title="**Voici les commande concernant le systeme de Jobs :**", color=color
            )
            embed.add_field(
                name="`/active_jobs`",
                value="Permet d'activer le system de Jobs'",
                inline=False
            )
            embed.add_field(
                name="`/admin_shop`",
                value="Permet de regarder les métier disponible a l'achat !'",
                inline=False
            )
            embed.add_field(
                name="`/admin_buy`",
                value="Permet de'acheter l'item d'un métier !'",
                inline=False
            )
            await interaction.response.edit_message(embed=embed)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Select())


@bot.tree.command(name="help", description="cette commande permet d'avoir de l'aide sur divers sujet")
async def help(interaction: discord.Interaction):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        embed = discord.Embed(title="Voici Les options d'aides !", color=color)
        await interaction.response.send_message(embed=embed, view=SelectView(), ephemeral=True)


@bot.tree.command(name="test", description="commande de test")
async def test(interaction: discord.Interaction):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        await interaction.response.send_message(f"Version : {config.version} La commande fonctionne bien !", ephemeral=True)

@app_commands.checks.has_permissions(administrator=True)
@bot.tree.command(name="say", description="Permet de faire dire quel que chose au bot")
async def say(interaction: discord.Interaction, message: str):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        await interaction.response.send_message(f"{message}")

@bot.tree.command(name="bug", description="Permet de report un bug")
async def bug (interaction: discord.Interaction, bug: str):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        try:
            t = time.localtime()
            current_hour = time.strftime("%H%M")
            current_time = int(time.time())

            report = datauser.get_report(user=str(interaction.user.name), server=str(interaction.guild))
            if report is None or current_time - report >= 2400:  # 2400 secondes = 40 minutes
                # Utilisateur peut signaler un bug
                datauser.report(user=str(interaction.user.name), server=str(interaction.guild), time=current_time)
                report_channel = bot.get_channel(1203382221889740800) 
                await report_channel.send(f'bug : {bug} | Report by {interaction.user.mention}')
                await interaction.response.send_message('Le bug a été correctement envoyer !.')
            else:
                await interaction.response.send_message('Vous pouvez envoyer un report toutes les 40 min uniquement.', ephemeral=True)
        except Exception as e:
            print("Error executing query:", e)

@app_commands.checks.has_permissions(administrator=True)
@bot.tree.command(name="active_card", description="Permet d'activer la welcome card")
async def activecard(interaction: discord.Interaction, channel: discord.TextChannel):
    try:
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.response.send_message("Tu est ban !", ephemeral=True)
        else:
            if serverdata.getchannelcard(server=str(interaction.guild)) == "y":
                interaction.response.send("Le plugin est déja activé !")
            else:
                    await interaction.response.send_message("Tu a activé le plugin `welcome_card`")
                    serverdata.setimage(name=str(interaction.guild), wc="y", wcc=str(channel.id))
    except Exception as e:
                print("Error executing query:", e)

@bot.tree.command(name="money", description="Permet de connaitre ton argent")
async def money(interaction: discord.Interaction):
    if plugin_money_active(interaction.guild) == True:
        user = str(interaction.user.name)
        server = str(interaction.guild)
        money = str(datauser.getusermoney(name=user, server=server))
        await interaction.response.send_message(f"Vous avez {money} <:boblux:1009422910303256686> ")
    else:
        await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)

@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.choices(type=[
        Choice(name="message",value="message"),
        Choice(name="embed",value="embed"),
    ])

@bot.tree.command(name="reaction_role", description="Permet de créer un message reaction rôle")
async def reactionrole(interaction: discord.Interaction, type: str, message: str, emoji: str, role: discord.Role):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        channel = str(interaction.channel.id)
        server = str(interaction.guild.name)
        if type == "embed":
            embed = discord.Embed(title=message, color=color)
            await interaction.response.send_message(embed=embed)
            msg = await interaction.original_response()
            await msg.add_reaction(emoji)
            messageid=str(msg.id)
            channelid=str(msg.channel.id)
            server=str(msg.guild.name)
            reactiondata.create_reaction(type="embed",message=message,role=str(role),id=messageid,server=server,channel=channelid, emoji=str(emoji))

        elif type == "message":
            await interaction.response.send_message(message)
            msg = await interaction.original_response()
            await msg.add_reaction(emoji)
            messageid=str(msg.id)
            channelid=str(msg.channel.id)
            server=str(msg.guild.name)
            reactiondata.create_reaction(type="message",message=message,role=str(role),id=messageid,server=server,channel=channelid, emoji=str(emoji))

@app_commands.checks.has_permissions(administrator=True)
@bot.tree.command(name="active_money", description="Permet d'activer le plugin d'économie ")
async def active_money(interaction: discord.Interaction):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        if plugin_money_active(interaction.guild) == True:
            await interaction.response.send_message("Le plugin est déja activé !", ephemeral=True)
        else:
            money = "y"
            serverdata.activmoney(name=str(interaction.guild), money="y")
            await interaction.response.send_message(f"Vous avez activer le plugin d'économie ! :tada:", ephemeral=True)

@app_commands.checks.has_permissions(administrator=True)
@bot.tree.command(name="give_money", description="Permet de give de l'argent a quel qu'un ")
async def give_money(interaction: discord.Interaction, user: str, money: str):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        if plugin_money_active(server=interaction.guild) == True:
            member = str(f'{user[2:-1]}')
            username = str(bot.get_user(int(member)))
            server = str(interaction.guild)
            datauser.give_money(server=server,user=username,money=money)
            await interaction.response.send_message(f"Vous avez give {user}  {money} <:boblux:1009422910303256686>", ephemeral=y)
        else:
            await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)
@app_commands.checks.has_permissions(administrator=True)
@bot.tree.command(name="set_money", description="Permet définir l'argent a quel qu'un")
async def set_money(interaction: discord.Interaction, user: str, money: str):
    if plugin_money_active(server=interaction.guild) == True:
        member = str(f'{user[2:-1]}')
        username = str(bot.get_user(int(member)))
        server = str(interaction.guild)
        datauser.set_money(server=server,user=username,money=money)
        await interaction.response.send_message(f"Vous avez mit l'argent de  {user} à {money} <:boblux:1009422910303256686>", ephemeral=y)
    else:
        await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)

@app_commands.checks.has_permissions(administrator=True)
@bot.tree.command(name="disable_money", description="Permet de désactiver le plugin d'économie ")
async def disable_money(interaction: discord.Interaction):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        if serverdata.ifmoneyactivate(server=str(interaction.guild)) == "n":
            await interaction.response.send_message("Le plugin n'est pas encore activé, activez le en faisent /active_money", ephemeral=True)
        else:
            user = str(interaction.user.name)
            server = str(interaction.guild.name)
            serverdata.activmoney(name=str(interaction.guild), money="n")
            servitems = economydata.get_item_serv(server=str(interaction.guild))
            for item in servitems:
                iteme = str(item['name'])
                print(iteme)
                inventory.remove_item(server=str(interaction.guild), item=iteme)
            try:
                economydata.delete_all_shops(server=str(interaction.guild.name))
                economydata.delete_all_items(server=str(interaction.guild.name))
                economydata.delete_all_channel(server=server)
                for member in interaction.guild.members:
                    datauser.remove_user(server=server, user=member)
            except Exception as e:
                print("Error executing query:", e)
            await interaction.response.send_message(f"Vous avez désactiver le plugin d'économie !", ephemeral=True)

@app_commands.checks.has_permissions(administrator=True)
@bot.tree.command(name="active_jobs", description="Permet d'activer le plugin de Jobs")
async def active_jobs(interaction: discord.Interaction):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        if serverdata.ifjobsactivate(server=str(interaction.guild)) == "n":
           
            serverdata.active_jobs(serveur=str(interaction.guild), jobs="y")

            await interaction.response.send_message("Vous avez activer le plugin de jobs ! :tada:", ephemeral=True)
            mineur = await interaction.guild.create_role(name="Mineur")
            bucheron = await interaction.guild.create_role(name="Bucheron")
            pecheur = await interaction.guild.create_role(name="Pecheur")
            overwritesmineur = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False
                ),
                interaction.guild.get_role(mineur.id): discord.PermissionOverwrite(
                    read_messages=True
                )
            }
            overwritesbucheron = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False
                ),
                interaction.guild.get_role(bucheron.id): discord.PermissionOverwrite(
                    read_messages=True
                )
            }
            overwritespecheur = {
                interaction.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False
                ),
                interaction.guild.get_role(pecheur.id): discord.PermissionOverwrite(
                    read_messages=True
                )
            }

            category = await interaction.guild.create_category(name="Jobs")
            mine = await interaction.guild.create_text_channel(name="Mine•👷", category=category, position=0, overwrites=overwritesmineur)
            foret = await interaction.guild.create_text_channel(name="Foret•🌲", category=category, position=1, overwrites=overwritesbucheron)
            lac = await interaction.guild.create_text_channel(name="Lac•🎣", category=category, position=2, overwrites=overwritespecheur)
            economydata.add_channel(id=str(mine.id), server=str(interaction.guild), money="30")
            economydata.add_channel(id=str(lac.id), server=str(interaction.guild), money="30")
            economydata.add_channel(id=str(foret.id), server=str(interaction.guild), money="30")
            economydata.create_channeljobs(server=str(interaction.guild), idlac=str(lac.id), idmine = str(mine.id), idforet=str(foret.id), idcategory=str(category.id), idrolemine=str(mineur.id), idrolelac=str(pecheur.id), idroleforet=str(bucheron.id))

        else:
            await interaction.response.send_message("Le plugin de jobs est déja  activer 🚫", ephemeral=y)

"""
@bot.tree.command(name="create_shop", description="Permet ajouter un channel ou on peut gagner de l'argent")
async def add_money(interaction: discord.Interaction, name: str):
    interaction.response.send_message("",ephemeral=y)
"""

@bot.tree.command(name="welcome_role", description="Permet d'activer le plugin de welcome role")
async def add_money(interaction: discord.Interaction, role: discord.guild.Role):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        try:
            server_info = serverdata.get_server_info(server=str(interaction.guild))
            for info in server_info:
                if info['wr'] == "y":
                    await interaction.response.send_message("Le plugin a été déja activé !",ephemeral=True)
                else:
                    await interaction.response.send_message("Le plugin a été activé",ephemeral=y)
                    serverdata.active_wr(server=str(interaction.guild), wr="y")
                    serverdata.set_role(server=str(interaction.guild), roleid=str(role.id))
        except Exception as e:
            print("Error executing query:", e)

@bot.tree.command(name="disable_welcome_role", description="Permet désactiver le plugin de welcome role")
async def add_money(interaction: discord.Interaction):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        try:
            server_info = serverdata.get_server_info(server=str(interaction.guild))
            for info in server_info:
                if info['wr'] == "n":
                    await interaction.response.send_message("Le plugin a pas été activé !",ephemeral=True)
                else:
                    await interaction.response.send_message("Le plugin a été désactivé",ephemeral=y)
                    serverdata.active_wr(server=str(interaction.guild), wr="n")
                    serverdata.set_role(server=str(interaction.guild), roleid=None)
        except Exception as e:
            print("Error executing query:", e)
@app_commands.checks.has_permissions(administrator=True)
@bot.tree.command(name="disable_card", description="Permet de désactiver la welcome card")
async def disablecard(interaction: discord.Interaction):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        if DataHandlerServeur.getchannelcard(server=str(interaction.guild)) == "n":
            interaction.response.send("Le plugin est pas encore activé !")
        else:
            await interaction.response.send_message("Tu a désactivé le plugin `welcome_card`")
            serverdata.setimage(name=str(interaction.guild),wc="n", wcc=None)

@app_commands.checks.has_permissions(administrator=True)
@bot.tree.command(name="disable_jobs", description="Permet d'activer le plugin de Jobs")
async def disable_jobs(interaction: discord.Interaction):
    if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
        await interaction.response.send_message("Tu est ban !", ephemeral=True)
    else:
        if serverdata.ifjobsactivate(server=str(interaction.guild)) == "y":
            serverdata.active_jobs(serveur=str(interaction.guild), jobs="n")
            channels = economydata.get_channeljobs(server=str(interaction.guild))
            for channel in channels:
                try:
                    idlac = str(channel['lac'])
                    idmine = str(channel['mine'])
                    idforet = str(channel['foret'])
                    idcategory = str(channel['category'])

                    economydata.delete_channel(server=str(interaction.guild), id=idlac)
                    economydata.delete_channel(server=str(interaction.guild), id=idmine)
                    economydata.delete_channel(server=str(interaction.guild), id=idforet)

                    idrolelac = str(channel['idrolelac'])
                    idrolemine = str(channel['idrolemine'])
                    idroleforet = str(channel['idroleforet'])

                    rolemine = discord.utils.get(interaction.guild.roles, id=int(idrolemine))
                    rolelac = discord.utils.get(interaction.guild.roles, id=int(idrolelac))
                    roleforet = discord.utils.get(interaction.guild.roles, id=int(idroleforet))

                    lac = bot.get_channel(int(idlac))
                    foret = bot.get_channel(int(idforet))
                    mine = bot.get_channel(int(idmine))
                    category = bot.get_channel(int(idcategory))
                    await lac.delete()
                    await mine.delete()
                    await foret.delete()
                    await category.delete()

                    await rolelac.delete()
                    await roleforet.delete()
                    await rolemine.delete()
                    for member in interaction.guild.members:
                        datauser.set_item(server=str(interaction.guild), user=str(member.name), item="mine", response=None)
                        datauser.set_item(server=str(interaction.guild), user=str(member.name), item="lac", response=None)
                        datasuser.set_item(server=str(interaction.guild), user=str(member.name), item="foret", response=None)

                except Exception as e:
                    print("Error executing query:", e)
                economydata.delete_channeljobs(server=str(interaction.guild))
                await interaction.response.send_message("Le system de jobs a bien été désactiver !")

        else:
            await interaction.response.send_message("Le plugin de jobs n'est pas encore activé !")

# --------- SUPER command ---------
@bot.command()
async def ripdelete(ctx):
    try:
        if ctx.message.author.id == 831621574675267597:
            await ctx.author.send("Sniff...")
            for server in bot.guilds:
                await server.leave()
        else:
            ctx.reply("???? je ne connais pas cette commande X)")
    except Exception as e:
        print("Error executing query:", e)

@bot.command()
async def getservers(ctx):
    try:
        if ctx.message.author.id == 831621574675267597:
            servers = bot.guilds
            test = int(len(servers))
            embed = discord.Embed(title=f"**Il y a {test} server : **", color=color)

            for server in servers:
                embed.add_field(
                    name=server.name,
                    value=f"{len(server.members)} membre | id : {server.id}",
                    inline=False
                ),
            await ctx.send(embed=embed)
        else:
            await ctx.reply("SUS")
    except Exception as e:
        print("Error executing query:", e)

@bot.command()
async def leaveservers(ctx, id:str):
    try:
        if ctx.message.author.id == 831621574675267597:
            server = await bot.fetch_guild(int(id))
            await server.leave()
            await ctx.reply("Ler server a bien été quiter", ephemeral=True)
        else:
            await ctx.reply("????")
    except Exception as e:
        print("Error executing query:", e)



# --------- Hybrid command ---------

@bot.hybrid_command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx: commands.Context, amount: str):
    if amount == "all":
        await ctx.reply(content="Tout le salon a été clear !", ephemeral=True)
        async for message in ctx.channel.history(limit=None):
            await message.delete()
    else:
        await ctx.send(content=f"j'ai clear {str(amount)} message !", ephemeral=True)
        await ctx.channel.purge(limit=int(amount))

# --------- Event ---------

@bot.event
async def on_ready():
    print("eu ???")
    guilde = str(len(bot.guilds))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guilde} serveurs"))
    clearcmd()
    for filname in os.listdir(r'./src'):
        if filname.endswith('.py'):
            await bot.load_extension(f'src.{filname[:-3]}')
    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print(e)

    print(f"""
			 ____   ____  ____  _     _    ___   __
 			|  _ \ / __ \|  _ \| |   | |  | \ \ / /
 			| |_) | |  | | |_) | |   | |  | |\ V / 
 			|  _ <| |  | |  _ <| |   | |  | | > <  
 			| |_) | |__| | |_) | |___| |__| |/ . \ 
 			|____/ \____/|____/|______\____//_/ \_\
                                        
                                        
				  Version : {config.version}
				  Statut : Running
				  Synced : {len(synced)} commands
		""")
    
    print("press [ctrl+c] to quit")

@bot.event
async def on_guild_update(before, after):
    if before.name != after.name:
        old = str(before.name)
        new = str(after.name)
        serverdata.update_name(oldname=old, newname=new)
        datauser.update_server(server=old, newname=new)
        inventory.update_server(old=old, new=new)
        economydata.update_itemsserver(server=old, new=new)
        economydata.update_chserver(server=old, new=new)
        economydata.update_shopsserver(server=old, new=new)

@bot.event
async def on_user_update(before, after):
    try:
        if before.name != after.name:
            username = str(before.name)
            newname = str(after.name)
            datauser.update_username(user=username, newname=newname)
            for guild in bot.guilds:
                member = guild.get_member(after.id)
                if member is not None:
                    inventory.update_username(server=str(guild.name), old=username, new=newname)
        else:
            print("tout vas bien")
    except Exception as e:
        print("Error executing query:", e)



@bot.event
async def on_member_join(member):
    guild = str(member.guild)
    if serverdata.ifwcactivate(server=guild) == "y":
        chanelid = serverdata.getchannelcard(guild)
        chanel = bot.get_channel(int(chanelid))
        await chanel.send(f"<@{member.id}> a rejoint le serveur :tada:")
        pos = sum(
            m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None
        )

        background = Editor("wlcbg.jpg")
        
        if member.avatar:
            profile_image = await load_image_async(str(member.avatar.url))
        else:
            profile_image = Image.open("C:/Users/HP/Desktop/dev/Python/Boblux/BobluxV0.2/graphic/default_avatar.jpg")
            # Convertir l'image en un format compatible avec easy_pil
            profile_image_bytes = BytesIO()
            profile_image.save(profile_image_bytes, format='PNG')
            profile_image_bytes.seek(0)
            
            profile_image = Editor(profile_image_bytes)

        profile = profile_image.resize((250, 250)).circle_image()
        poppins = Font.poppins(size=40, variant="bold")
        poppins_small = Font.poppins(size=30, variant="light")

        background.paste(profile, (410, 95))
        background.ellipse((410, 95), 250, 250, outline="orange", stroke_width=4)

        background.text(
            (555, 375), f"Bienvenue sur | {member.guild.name} |", color="#9E380F", font=poppins, align="center"
        )
        background.text(
            (555, 425), f"{member.name}", color="white", font=poppins_small, align="center"
        )
        background.text(
            (555, 457), f"Tu es le {pos}ième Membre", color="black", font=poppins_small, align="center"
        )

        file = File(fp=background.image_bytes, filename="wlcbg.jpg")
        await chanel.send(file=file)
        datauser.cu(
            name=str(member.name),
            id=str(member.id),
            money="100",
            server=str(member.guild)
        )
        

    else:
        datauser.cu(
            name=str(member.name),
            id=str(member.id),
            money="100",
            server=str(member.guild)
        )
    if serverdata.wr_activate(server=str(guild)) == "y":
        roleid = int(serverdata.get_role(server=guild))
        roleadd = discord.utils.get(member.guild.roles, id=roleid)
        await member.add_roles(roleadd)

@bot.event
async def on_guild_join(guild):
    guilde = len(bot.guilds)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guilde} serveurs"))
    members = str(len(guild.members))
    wr = "n"
    wc = "n"
    wm = "n"
    money = "n"
    jobs = "n"
    name = str(guild.name)
    id = str(guild.id)
    serverdata.cs(
        membercount=members,
        wr=wr,
        wc=wc,
        wm=wm,
        name=name,
        id=id,
        money=money,
        jobs=jobs
    )
    inventory.create_inventory_server(server=str(guild.name))
    for user in guild.members:
        datauser.cu(
            name=str(user.name),
            id=str(user.id),
            money="100",
            server=str(guild.name)
        )
        inventory.create_server_user_data(server=str(guild.name),user=str(user.name),id=str(user.id))

@bot.event
async def on_guild_remove(guild):
    guilde = len(bot.guilds)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{guilde} serveurs"))
    serverdata.remove_server(
        server=str(guild.name)
    )
    economydata.delete_all_shops(server=str(guild.name))
    economydata.delete_all_channel(server=str(guild.name))
    economydata.delete_all_items(server=str(guild.name))
    inventory.delete_server(server=str(guild.name))
    for member in guild.members:
        datauser.remove_user(
            server=str(guild.name),
            user=str(member.name)
        )

@bot.event
async def on_raw_reaction_add(payload):
    messageid = str(payload.message_id)
    channel_id = payload.channel_id
    memberid = payload.user_id
    guild = bot.get_guild(payload.guild_id)
    guildstr = str(bot.get_guild(payload.guild_id))
    messages = reactiondata.getmessageid(server=guildstr, id=messageid)
    for message in messages:
        if message["id"] == messageid:
            role = reactiondata.getrole(server=guildstr, id=messageid)
            member = guild.get_member(memberid)
            roleadd = discord.utils.get(guild.roles, name=role)
            await member.add_roles(roleadd)
        else:
            pass   

@bot.event
async def on_raw_reaction_remove(payload):
    messageid = str(payload.message_id)
    channel_id = payload.channel_id
    memberid = payload.user_id
    guildstr = str(bot.get_guild(payload.guild_id))
    guild = bot.get_guild(payload.guild_id)
    messages = reactiondata.getmessageid(server=guildstr, id=messageid)
    for message in messages:
        if message["id"] == messageid:
            role = reactiondata.getrole(server=guildstr, id=messageid)
            member = guild.get_member(memberid)
            roleadd = discord.utils.get(guild.roles, name=role)
            await member.remove_roles(roleadd)
        else:
            pass
@bot.event
async def on_command(ctx):
    with open('logs.txt', 'r') as f:
        content = f.read()
        writefile = open('logs.txt','w')
        command = str(ctx.command)
        user = str(ctx.message.author)
        id = str(ctx.message.author.id)
        now = datetime.now()
        serveur = str(ctx.message.guild)

        time = now.strftime("[%H:%M:%S]")
        date = now.strftime("[%d-%m-%Y]")
        
        newcontent = f"{content}{user} avec l'id : [{id}] sur le serveur [{serveur}] a éxécuter la command {command} a {time} le {date}\n--------------------------------\n"
        writefile.write(newcontent)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Mmmmmmh, j'ai bien l'impression que cette commande n'existe pas x/")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("JE crois que tu a oublier quel que chose la")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Tu n'as pas les permissions pour faire cette commande.")
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Oups vous ne pouvez utilisez cette commande.")
    if isinstance(error, discord.errors.Forbidden):
        await ctx.send("Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande")

@bot.tree.error
async def on_app_command_error(interaction: discord.Integration, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("Tu n'as pas les permissions pour faire cette commande.", ephemeral=True)
    if isinstance(error, app_commands.CommandNotFound):
        await interaction.response.send_message("Mmmmmmh, j'ai bien l'impression que cette commande n'existe pas x/", ephemeral=True)
    if isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message("Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande", ephemeral=True)

@bot.event
async def on_app_command_completion(interaction: discord.Interaction, command):
    with open('logs.txt', 'r') as f:
        content = f.read()
        writefile = open('logs.txt','w')
        command = str(command.name)
        user = str(interaction.user.name)
        id = str(interaction.user.id)
        now = datetime.now()
        serveur = str(interaction.user.guild.name)

        time = now.strftime("[%H:%M:%S]")
        date = now.strftime("[%d-%m-%Y]")
        
        newcontent = f"{content}{user} avec l'id : [{id}] sur le serveur [{serveur}] a éxécuter la command {command} a {time} le {date}\n--------------------------------\n"
        writefile.write(newcontent)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if str(message.author) == "Boblux#0843":
        pass
    else:
        if economydata.is_channel_money(server=str(message.guild.name), id=str(message.channel.id)) == None:
            pass
        else:
            if serverdata.ifmoneyactivate(server=str(message.guild.name)) == "y":
                if int(economydata.is_channel_money(server=str(message.guild.name), id=str(message.channel.id))) == int(message.channel.id):
                    user = str(message.author.name)
                    server = str(message.guild.name)
                    money = economydata.channel_money(server=server, id=str(message.channel.id))
                    datauser.give_money(server=server,user=user,money=money)
                else:
                    pass
            else:
                pass


# --------SUS-------
@bot.command()
async def sus(ctx, message=None):
    if message == "WTIIS":
        await ctx.message.author.send("Tu a trouvé l'easter egg")
    else:
        await ctx.send("*W*hen *T*he *I*mposter *I*s *S*us")

bot.run(config.token)