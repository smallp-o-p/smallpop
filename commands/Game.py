from discord.ext import commands
import discord
import sqlite3
from discord import app_commands

connection = sqlite3.connect(r"C:\Users\legio\PycharmProjects\pythonProject\dbs\sensdata.db")
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS sens(game text, multiplier float)')
connection.commit()


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addsens",
                      help="Maps a game name to its sensitivity multiplier to be used in sensitivity calculation. \n"
                           "Format: [shorthand, sens multiplier]")
    async def addSens(self, ctx, shorthand: str, multiplier: float):
        cursor.execute("insert into sens values(?,?)", (shorthand, multiplier))
        connection.commit()
        await ctx.reply("Game: **{}** added.".format(shorthand))

    @commands.command(name="getmult")
    async def GetMultiplier(self, ctx, game: str):
        cursor.execute("select multiplier from sens where game ='{}'".format(game))
        result = cursor.fetchone()[0]
        embed = discord.Embed(title="Sensitivity Multiplier")
        embed.add_field(name=game, value=result)
        await ctx.reply(embed=embed)

    @commands.command(name="printrow")
    async def printrows(self, ctx):
        cursor.execute("select game from sens")
        data = cursor.fetchall()
        await ctx.reply("Games supported: {}".format(data))

    @app_commands.command(name="cm",
                          description="gamesens -> cm/360")
    async def cm(self, interaction: discord.Interaction, game: str, dpi: int, sens: float):
        cursor.execute("select multiplier from sens where game ='{}'".format(game))
        result = cursor.fetchall()
        if len(result) == 0:
            await interaction.response.send_message("Invalid game, please check the list of games that are currently supported!", ephemeral=True, view=discord.ui.View(timeout=30))
        else:
            increment = sens * result[0][0]
            cmper360 = ((360 / increment) / dpi)*2.54
            await interaction.response.send_message("Your cm/360 is {}".format(round(cmper360, 2)))


async def setup(bot):
    await bot.add_cog(Game(bot))
