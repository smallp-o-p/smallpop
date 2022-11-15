import asyncio
from discord.ext import commands


class Fun(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command(name="foo")
    async def boop(self, ctx):
        member = ctx.author
        async with ctx.channel.typing():
            await asyncio.sleep(1)
            await ctx.reply(f'Hello {member.name}')


async def setup(bot):
    await bot.add_cog(Fun(bot))
