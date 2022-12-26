from discord.ext import commands
import discord


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ch",
                      help="Creates a channel or channels. \n"
                           "Format: [category, vc/txt, *channelnames] \n" 
                      "Example: $ch MyCategory vc one two three \n"
                      "This will create voice channels 'one', 'two', 'three' under category MyCategory")
    @commands.has_guild_permissions(manage_channels=True)
    async def maketxtchannels(self, ctx, category: str = commands.parameter(description="Category to create"),
                              type: str = commands.parameter(default="vc", description="vc for voice or txt for text"),
                              *names: str):
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
            if type == "txt":
                for channel in names:
                    channel.replace(" ", "-")
                    await guild.create_text_channel(name=channel, category=category)
            if type == "vc":
                for channel in names:
                    channel.replace(" ", "-")
                    await guild.create_voice_channel(name=channel, category=category)

    @commands.command(name="delch")
    @commands.has_guild_permissions(manage_channels=True)
    async def deletechannel(self, ctx, *channels):
        guild = ctx.guild
        for channel in channels:
            found = discord.utils.get(guild.channels, name=channel)
            if not found:
                await ctx.send("Channel **{}** not found.".format(channel))
            else:
                await found.delete()
                await ctx.send("Channel **{}** deleted.".format(channel))

    @commands.command(name="mute")
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx, member: discord.Member, time : str):
        guild = ctx.guild
        rolecheck = discord.utils.get(guild.roles, name="Muted")
        if not rolecheck:
            rolecheck = await guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False))
        await member.add_roles(rolecheck)
        await ctx.send(member.mention + " muted lol")

    @commands.command(name="sync")
    async def sync(self,ctx) -> None:
        await ctx.bot.tree.sync()
        await ctx.reply("Synced!")


async def setup(bot):
    await bot.add_cog(Admin(bot))


