import discord
from discord.ext import commands


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        em = discord.Embed(title="Something went wrong!",
                           description="Please read the error message to see what the issue is. :)",
                           color=discord.Color.red())
        em.add_field(name="Error:", value=error)
        await ctx.send(embed=em)


async def setup(bot):
    await bot.add_cog(Listener(bot))
