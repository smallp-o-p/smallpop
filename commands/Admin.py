from discord.ext import commands
import discord


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="txtch")
    async def maketxtchannels(self, ctx, category: str, *names: str):
        guild = ctx.guild
        if category == "None":
            for channel in names:
                channel.replace(" ", "-")
                await guild.create_text_channel(name=channel)
        else:
            catcheck = discord.utils.get(guild.categories, name=category)
            if not catcheck:
                category = await guild.create_category(name=category)
            else:
                category = catcheck
            for channel in names:
                channel.replace(" ", "-")
                await guild.create_text_channel(name=channel, category=category)

    @commands.command(name="delch")
    async def deletechannel(self, ctx, *channels):
        guild = ctx.guild
        for channel in channels:
            found = discord.utils.get(guild.channels, name=channel)
            if not found:
                await ctx.send("Channel **{}** not found.".format(channel))
            else:
                await found.delete()
                await ctx.send("Channel **{}** deleted.".format(channel))




async def setup(bot):
    await bot.add_cog(Admin(bot))


