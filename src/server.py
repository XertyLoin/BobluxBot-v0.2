from discord import app_commands
import discord
from discord.ext import commands

class CogServer(commands.Cog, name="testmoneyfs"):
    def __init__(self, bot):
        self.bot = bot
        
    #@commands.Cog.listener()
    #async def on_ready(self):
        
        #print(f'synced from economy: {len(synced)}')
    @app_commands.command(name="test2", description="test")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong :rofl:")

async def setup(bot):
    await bot.add_cog(CogServer(bot))
    
    