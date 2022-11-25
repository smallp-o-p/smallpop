import discord
from discord.ext import commands


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        em = discord.Embed(title="listen here fucko",
                           description="there's an error",
                           color=discord.Color.red())
        em.add_field(name="error:", value=error)
        await ctx.send(embed=em)


async def setup(bot):
    await bot.add_cog(Listener(bot))
