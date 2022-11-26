from discord.ext import commands
import discord


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="txtch")
    async def maketxtchannels(self, ctx, category: str = None, *names: str):
        guild = ctx.guild
        if not category:
            for channel in names:
                channel.replace(" ", "-")
                await guild.create_text_channel(name=channel)
        else:
            catcheck = discord.utils.get(guild.categories, name=category)
            if not catcheck:
                newcat = await guild.create_category(name=category)
                category = newcat
            else:
                category = catcheck
        for channel in names:
            channel.replace(" ", "-")
            await guild.create_text_channel(name=channel, category=category)


async def setup(bot):
    await bot.add_cog(Admin(bot))


