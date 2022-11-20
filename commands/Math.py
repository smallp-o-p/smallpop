import aiohttp
from discord.ext import commands
import json

api_address = 'http://api.mathjs.org/v4/'


class Math(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command(name="eval")
    async def expression(self, ctx, *args: str):
        exprs = ",".join(args).split(",")
        request = {"expr": exprs, "precision": 14}
        async with aiohttp.ClientSession() as session:
            async with session.post(api_address, data=json.dumps(request)) as response:
                answer = await response.json()
        await ctx.reply("Result(s):\n```\n{}\n```".format("\n".join(answer["result"])))


async def setup(bot):
    await bot.add_cog(Math(bot))




