from discord.ext import commands
import discord
import sqlite3
from discord import app_commands

connection = sqlite3.connect(r"filepath")
cursor = connection.cursor()
cursor.execute("select game from sens") # gets all the games in the db
games = [item[0] for item in cursor.fetchall()]


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

    @app_commands.command(name="cm",
                          description="gamesens -> cm/360")
    async def cm(self, interaction: discord.Interaction, game: str, dpi: int = None, sens: float = None):
        if game.lower() == "help":
            await interaction.response.send_message("Games supported: {}".format(games)) # i should just make a help command that covers everything, but that's for later :)
        if game not in games:
            await interaction.response.send_message(
                "Invalid game, please check the list of games that are currently supported!", ephemeral=True,
                view=discord.ui.View(timeout=30))
        else:
            cursor.execute("select multiplier from sens where game ='{}'".format(game))
            increment = sens * cursor.fetchall()[0][0]
            cmper360 = ((360 / increment) / dpi) * 2.54
            await interaction.response.send_message("Your cm/360 is {}".format(round(cmper360, 2)))

    @app_commands.command(name="conv", description="game1->game2")
    async def conv(self, interaction: discord.Interaction, game1: str, sens: float, game2: str):
        if game1 not in games or game2 not in games:
            await interaction.response.send_message(
                "Game **{}** not found!".format(game1 if game1 not in games else game2))
        else:
            results = cursor.execute(
                "select multiplier from sens where game = '{}' UNION select multiplier from sens where game = '{}'".format(
                    game2, game1)).fetchall()
            # list of tuples that contain the multipliers of both games
            ratio = results[1][0] / results[0][0] # it puts game2 multiplier in [0] and game1 multiplier in [1]
            result = round(sens * ratio, 3)
            await interaction.response.send_message("({}) {} -> ({}) {}".format(sens, game1, result, game2))


async def setup(bot):
    await bot.add_cog(Game(bot))
