
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
from data.script.inventorydata import DataHandlerInventory
import sqlite3

color = int(0xdb9721)
datauser = DataHandler(r"data/userdata.db")
serverdata = DataHandlerServeur(r"data/serveurdata.db")
reactiondata = DataHandlerReaction(r"data/reaction.db")
economyata = DataHandlerEconomy(r"data/economydata.db")
inventory = DataHandlerInventory(r"data/inventory.db")

y = True

if platform.system() == "Windows":
    def clearcmd():
        os.system("cls")
if platform.system() == 'Linux':
    def clearcmd():
        os.system("clear")

def plugin_money_active(server: str):
    if serverdata.ifmoneyactivate(server=str(server)) == "y":
        return True
    else:
        return False

class CogEconomy(commands.Cog, name="testmoney"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shop", description="Permet d'aller voir un shop")
    async def shop(self, interaction: discord.Interaction, shop: str):
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.send("Tu est ban !", ephemeral=True)
        else:
            if plugin_money_active(interaction.guild) == True:
                shops = economyata.get_shops(server=str(interaction.guild))
                if shops == []:
                    await interaction.response.send_message("Il ny a pas encrde de shop sur se server !", ephemeral=y)
                else:
                    for shopname in shops:
                        if str(shop) == shopname['name']:
                            embed=discord.Embed(title=f"🛒 Shop | {shopname['name']}", color=color)
                            items = economyata.get_items(server=str(interaction.guild), shop=shop)
                            if items == []:
                                await interaction.response.send_message(embed=embed, ephemeral=y) 
                            else:
                                for item in items:
                                    embed.add_field(
                                        name=item['name'],
                                        value=f"{item['description']} | {item['value']} <:boblux:1009422910303256686>"
                                    )
                                await interaction.response.send_message(embed=embed)
                        else:
                            await interaction.response.send_message("Se shop n'exciste pas !",ephemeral=y)
            else:
                await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)    

    @app_commands.command(name="shops", description="Permet de voir les shops du server !")
    async def shops(self, interaction: discord.Interaction):
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.send("Tu est ban !", ephemeral=True)
        else:
            if plugin_money_active(interaction.guild) == True:
                shops = economyata.get_shops(server=str(interaction.guild))
                if shops == []:
                    await interaction.response.send_message("Il ny a pas encore de shop sur se server !", ephemeral=y)
                else:
                    embed = discord.Embed(title="🛒 Les shops du server :")
                    for shop in shops:
                        embed.add_field(
                            name=str(shop['name']),
                            value=str(shop['description']),
                            inline=True
                        )
                    await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)
        
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="create_shop", description="Permet créer un shop")
    async def create_shop(self, interaction: discord.Interaction, name: str, description: str):
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.send("Tu est ban !", ephemeral=True)
        else:
            if plugin_money_active(server=interaction.guild) == True:
                    shops = economyata.get_shops(server=str(interaction.guild))
                    if shops == []:
                        economyata.create_shop(server=str(interaction.guild), name=str(name), description=description)
                        await interaction.response.send_message(f"Le shop **{str(name)}** a été créer !",ephemeral=y)
                    else:
                        for shopname in shops:
                            if str(name) == shopname['name']:
                                await interaction.response.send_message("Se nom est déja utilisé sur server 🚫")
                            else:
                                economyata.create_shop(server=str(interaction.guild), name=str(name), description=description)
                                await interaction.response.send_message(f"Le shop **{str(name)}** a été créer !",ephemeral=y)
            else:
                await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)
        
    @app_commands.command(name="leadboard", description="Permet de voir le leadboard")
    async def leadboard(self, interaction: discord.Interaction):
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.send("Tu est ban !", ephemeral=True)
        else:
            if plugin_money_active(interaction.guild) == True:
                print("1")
                con = sqlite3.connect(r"data/userdata.db")
                con.row_factory = sqlite3.Row
                cursor = con.cursor()
                query = f"SELECT * FROM userdata WHERE server = ? ORDER BY cast(money as int) DESC"
                cursor.execute(query, (str(interaction.guild),))
                result = cursor.fetchall()
                cursor.close()
                embed = discord.Embed(title=f"--| Leadboard de ***{interaction.guild}*** |--")
                who = 0
                for row in result:
                    print("1")
                    who = who+1
                    user = row[3]
                    embed.add_field(
                        name=f"{who} • {user}",
                        value=f"{row[1]} <:boblux:1009422910303256686>"
                    )
                    if who == 10:
                        break
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)


    @app_commands.choices(type=[
    Choice(name="role",value="role"),
    Choice(name="autre",value="other"),
])
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="create_item", description="Permet de créer un item")
    async def create_item(self, interaction: discord.Interaction, name: str, shop: str, value: str, description: str, type: str, role: str=None):
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.send("Tu est ban !", ephemeral=True)
        else:    
            if plugin_money_active(interaction.guild) == True:
                shops = economyata.get_shops(server=str(interaction.guild))
                if shops == []:
                    await interaction.response.send_message("Il n'y a pas encore de shop sur le server !",ephemeral=y)
                else:
                    for shopname in shops:
                        if str(shop) == shopname['name']:
                            if type == "other":
                                economyata.create_item(server=str(interaction.guild), name=name, shop=shop, is_role="n", value=value, description=description)
                                await interaction.response.send_message(f"L'item {name} a {value} <:boblux:1009422910303256686> a été correctement créer",ephemeral=y)
                                inventory.add_item(server=str(interaction.guild.name), item=name)
                                inventory.set_item(server=str(interaction.guild), count="0", item=name)
                            if type == "role":
                                economyata.create_item(server=str(interaction.guild), name=name, shop=shop, is_role="y", value=value, description=description)
                                economyata.make_role(server=str(interaction.guild), item=name, shop=shop, roleid=role[3:-1])
                                await interaction.response.send_message(f"L'item {name} a {value} <:boblux:1009422910303256686> a été correctement créer",ephemeral=y)
                                inventory.add_item(server=str(interaction.guild.name), item=name)

                        else:
                            await interaction.response.send_message("Se shop néxiste pas",ephemeral=y)
            else:
                await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="add_money_channel", description="Permet ajouter un channel ou on peut gagner de l'argent")
    async def addmoney(self, interaction: discord.Interaction, channel: discord.TextChannel, montant: int):
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.send("Tu est ban !", ephemeral=True)
        else:
            if plugin_money_active(interaction.guild) == True:
                economyata.add_channel(id=str(channel.id), money=str(montant), server=str(interaction.guild))
                await interaction.response.send_message(f"1 message dans <#{channel.id}> = {montant} <:boblux:1009422910303256686> ", ephemeral=y)
            else:
                await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)
        
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="delete_shop", description="Permet suprimer un shop")
    async def delete_shop(self, interaction: discord.Interaction, shop:str):
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.send("Tu est ban !", ephemeral=True)
        else:
            if plugin_money_active(server=interaction.guild) == True:
                    shops = economyata.get_shops(server=str(interaction.guild))
                    if shops == []:
                        await interaction.response.send_message(f"Il n'y a pas de shop sur server :rofl:",ephemeral=y)
                    else:
                        servitems = economyata.get_item_serv(server=str(interaction.guild))
                        for item in servitems:
                            try:
                                inventory.remove_item(server=str(interaction.guild), item=item['name'])
                            except Exception as e:
                                    print("Error executing query 1:", e)
                        for shopname in shops:
                            if str(shop) == shopname['name']:
                                economyata.delete_shop(server=str(interaction.guild), shop=shop)
                                economyata.delete_all_shop_items(server=str(interaction.guild), shop=shop)

                                await interaction.response.send_message(f"Le shop {shop} a bien été suprimer")
                            else:
                                await interaction.response.send_message(f"Se shop n'existe pas 🚫",ephemeral=y)
            else:
                await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)

    @app_commands.command(name="buy", description="Permet dacheter un item d'un shop")
    async def buy(self, interaction: discord.Interaction, shop: str, item: str):
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.send("Tu est ban !", ephemeral=True)
        else:
            if plugin_money_active(interaction.guild) == True:
                shops = economyata.get_shops(server=str(interaction.guild))
                if shops == []:
                    await interaction.response.send_message(f"Il n'y a encore pas de shop sur server :rofl:",ephemeral=y)
                else:
                    for shopname in shops:
                        if shop == shopname['name']:
                            items = economyata.get_items(server=str(interaction.guild), shop=shop)
                            if items == []:
                                await interaction.response.send_message("Il n'y a pas d'item dans se shop :rofl:")
                            else:
                                item_exists = False
                                for iteme in items:
                                    if item == iteme['name']:
                                        item_exists = True
                                        break

                                if not item_exists:
                                    await interaction.response.send_message("Cet item n'existe pas !!")
                                else:
                                    usermoney = int(datauser.getusermoney(server=str(interaction.guild), name=str(interaction.user.name)))
                                    print(usermoney)
                                    if int(iteme['value']) <= usermoney:
                                        user = str(interaction.user.name)
                                        server = str(interaction.guild)
                                        price = iteme['value']
                                        datauser.remove_money(server=server, user=user, money=price)
                                        print("la")
                                        print(iteme['is_role'])
                                        if str(iteme['is_role']) != "n":
                                            print("la")
                                            role = iteme['roleid']
                                            try:
                                                print(inventory.get_count(server=str(interaction.guild), user=str(interaction.user.name), item=str(iteme['name'])))
                                                if inventory.get_count(server=str(interaction.guild), user=str(interaction.user.name), item=str(iteme['name'])) == "None":
                                                    inventory.give_item(server=server, user=user, item=item, count="1")
                                                    member = interaction.guild.get_member(interaction.user.id)
                                                    role = discord.utils.get(interaction.guild.roles, id=int(role))
                                                    await member.add_roles(role)
                                                else:
                                                    await interaction.response.send_message("Tu ne peut pas achter 2 fois un role !")
                                            except Exception as e:
                                                print("Error executing query 1:", e)
                                            await interaction.response.send_message("Tu as acheté ton item")
                                        else:
                                            print("test")
                                            try:
                                                print("heuuu")
                                                if (inventory.get_count(server=str(interaction.guild), user=str(interaction.user.name), item=str(iteme['name'])) == "None") or (inventory.get_count(server=str(interaction.guild), user=str(interaction.user.name), item=str(iteme['name'])) == "0"):
                                                    inventory.give_item(server=server, user=user, item=item, count="1")
                                                    await interaction.response.send_message("Vous avais achter votre item !", ephemeral=True)
                                                else:
                                                    inventory.give_item2(server=server, user=user, item=item)
                                                    await interaction.response.send_message("Vous avais achter votre item !", ephemeral=True)
                                            except Exception as e:
                                                print("Error executing query 2:", e)
                                    else:
                                        await interaction.response.send_message(f"Vous n'avez que {usermoney} <:boblux:1009422910303256686> donc vous n'avait pas asser d'argent pour achter cette item !",ephemeral=True)
                                                                
                        else:
                            await interaction.response.send_message("Se shop n'existe pas !")

            else:
                await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)
        
    @app_commands.command(name="inventory", description="Permet de voir ton inventaire")
    async def inventory(self, interaction: discord.Interaction):
        if str(datauser.is_ban(user=str(interaction.user.name), server=str(interaction.guild.name))) == "y":
            await interaction.send("Tu est ban !", ephemeral=True)
        else:
            if plugin_money_active(server=interaction.guild.name) == True:
                try:
                    servitems = economyata.get_item_serv(server=str(interaction.guild))
                    if servitems == []:
                        await interaction.response.send_message(f"Il n'y a encore pas d'item sur server :sweat_smile:",ephemeral=y)
                    else:
                        embed=discord.Embed(title=f"Inventory | {str(interaction.user.name)}", color=color)
                        mine = datauser.have_item(server=str(interaction.guild), user=str(interaction.user.name), item="mine")
                        foret = datauser.have_item(server=str(interaction.guild), user=str(interaction.user.name), item="foret")
                        lac = datauser.have_item(server=str(interaction.guild), user=str(interaction.user.name), item="lac")
                        if lac == "y":
                            embed.add_field(
                                name=str("Canne a pêche"),
                                value=str("Cett item te permet d'acceder au lac"),
                                inline=False
                            )
                        if mine == "y":
                            embed.add_field(
                                name=str("**Pioche**"),
                                value=str("Cett item te permet d'acceder a la mine"),
                                inline=False
                            )
                        elif foret == "y":
                            embed.add_field(
                                name=str("**Pioche**"),
                                value=str("Cett item te permet d'acceder a la foret"),
                                inline=False
                            )
                        for item in servitems:
                            item_count = inventory.get_count(server=str(interaction.guild), user=str(interaction.user.name), item=str(item['name']))
                            print(item_count)
                            if item_count == "None" or int(item_count) == 0:
                                await interaction.response.send_message("Tu n'a pas encore achter d'item", ephemeral=y)
                            else:                           
                                embed.add_field(
                                        name=str(item['name']),
                                        value=str(item_count),
                                        inline=False
                                    )
                        if lac == "y" or mine=="y" or foret == "y":
                            await interaction.response.send_message(embed=embed, ephemeral=y)
                        else:
                            await interaction.response.send_message(embed=embed, ephemeral=y)
                except Exception as e:
                    print("Error executing query:", e)
            else:
                await interaction.response.send_message("Le plugin de money n'est pas activer, tu peut activer le plugin de money avec la commande /active_money", ephemeral=y)
async def setup(bot):
    await bot.add_cog(CogEconomy(bot))