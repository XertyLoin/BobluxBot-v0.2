from discord import app_commands
import discord
from discord.ext import commands
from discord.app_commands import Choice
import sys
import os
from os import system
import platform
sys.path.insert(0, '/home/xerty/Bureau/Boblux/BobluxV2.0')
from data.script.userdata import DataHandler
from data.script.serverdata import DataHandlerServeur
from data.script.reactiondata import DataHandlerReaction
from data.script.economydata import DataHandlerEconomy
import sqlite3

y = True
color = int(0xdb9721)
datauser = DataHandler(r"data/userdata.db")
serverdata = DataHandlerServeur(r"data/serveurdata.db")
reactiondata = DataHandlerReaction(r"data/reaction.db")
economyata = DataHandlerEconomy(r"data/economydata.db")

if platform.system() == "Windows":
    def clearcmd():
        os.system("cls")
if platform.system() == 'Linux':
    def clearcmd():
        os.system("clear")

class CogJobs(commands.Cog, name="cogjobs"):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="admin_shop", description="Permet d'aficher le shop admin")
    async def admin_shop(self, interaction: discord.Integration):
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.response.send_message("Tu est ban !", ephemeral=True)
        else:
            if serverdata.ifjobsactivate(server=str(interaction.guild)) == "y":
                embed=discord.Embed(title=f"🛒 Admin Shop ", color=color)
                items = economyata.get_admin_items()
                for item in items:
                    embed.add_field(
                        name=item['name'],
                        value=f"{item['description']} | {item['price']} <:boblux:1009422910303256686>"
                    )
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("Le plugin de jobs n'est pas activer 🚫", ephemeral=y)
    @app_commands.choices(item=[
    Choice(name="Pioche - 1500 Boblux|Permet davoir le role de Mineur",value="m"),
    Choice(name="Canne a Peche - 1500 Boblux | Permet d'avoir le métier de Pecheur",value="p"),
    Choice(name="Hache - 1500 Boblux | Permet d'avoir le métier de Bucheron",value="b"),
    ])
    @app_commands.command(name="admin_buy", description="Permet d'achter un item du shop admin")
    async def admin_buy(self, interaction: discord.Interaction, item: str):
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.response.send_message("Tu est ban !", ephemeral=True)
        else:
            if serverdata.ifjobsactivate(server=str(interaction.guild)) == "y":
                usermoney = int(datauser.getusermoney(server=str(interaction.guild), name=str(interaction.user.name)))
                if 1500 <= usermoney:
                    print(datauser.have_item(server=str(interaction.guild), user=str(interaction.user.name), item="mine"))
                    if item == "m":
                        if datauser.have_item(server=str(interaction.guild), user=str(interaction.user.name), item="mine") == "y":
                            await interaction.response.send_message("Vous avais déja acheter cette item !")
                        else:
                            datauser.remove_money(server=str(interaction.guild),user=str(interaction.user.name), money="1500")
                            await interaction.response.send_message("Vous avais acheter la pioche :tada:")
                            member = interaction.guild.get_member(interaction.user.id)
                            role = discord.utils.get(interaction.guild.roles, name="Mineur")
                            await member.add_roles(role)
                            datauser.set_item(server=str(interaction.guild), user=str(interaction.user.name), item="mine", reponse="y")
                    if item == "b":
                        if datauser.have_item(server=str(interaction.guild), user=str(interaction.user.name), item="foret") == "y":
                            await interaction.response.send_message("Vous avais déja acheter cette item !")
                        else:                        
                            datauser.remove_money(server=str(interaction.guild),user=str(interaction.user.name), money="1500")
                            await interaction.response.send_message("Vous avais acheter la hache :tada:")
                            member = interaction.guild.get_member(interaction.user.id)
                            role = discord.utils.get(interaction.guild.roles, name="Bucheron")
                            await member.add_roles(role)
                            datauser.set_item(server=str(interaction.guild), user=str(interaction.user.name), item="foret", reponse="y")
                    if item == "p":
                        if datauser.have_item(server=str(interaction.guild), user=str(interaction.user.name), item="lac") == "y":
                            await interaction.response.send_message("Vous avais déja acheter cette item !")
                        else:
                            datauser.remove_money(server=str(interaction.guild),user=str(interaction.user.name), money="1500")
                            await interaction.response.send_message("Vous avais acheter la canne a peche :tada:")
                            member = interaction.guild.get_member(interaction.user.id)
                            role = discord.utils.get(interaction.guild.roles, name="Pecheur")
                            await member.add_roles(role)
                            datauser.set_item(server=str(interaction.guild), user=str(interaction.user.name), item="lac", reponse="y")
                else: 
                    await interaction.response.send_message("Tu n'a pas asser d'argent pour acheter sa !", ephemeral=True)
            else:
                await interaction.response.send_message("Le plugin de jobs n'est pas encore activer !", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CogJobs(bot))
    