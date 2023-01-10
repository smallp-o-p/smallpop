import discord
from discord.ext import commands
from pytube import YouTube


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play") # basic for now
    async def play(self, ctx: discord.ext.commands.Context, link: str):
        userstat = ctx.message.author.voice
        if not userstat:
            await ctx.reply("You're not in a voice channel!")
        else:
            vc = await userstat.channel.connect()
            await ctx.reply("Joining!")
            if "youtube.com/watch?" not in link:
                await ctx.reply("Only links are supported for now, sorry! Disconnecting...")
                await vc.disconnect()
            else:
                yt = YouTube(url=link)
                embed = discord.Embed(title=f"Now playing: {yt.title}")
                embed.add_field(name="Creator:", value=yt.author)
                embed.set_image(url=yt.thumbnail_url)
                stream = yt.streams.get_by_itag(251)
                stream.download(output_path=r"C:\Users\legio\PycharmProjects\pythonProject\funnypictures",
                                filename="{}.mp4".format(yt.title.lower().replace(" ", "_")))
                vc.play(discord.FFmpegOpusAudio(
                    executable=r"C:\Users\legio\PycharmProjects\pythonProject\FFMPEG\bin\ffmpeg.exe",
                    source=r"C:\Users\legio\PycharmProjects\pythonProject\funnypictures\{}.mp4".format(
                        yt.title.lower().replace(" ", "_"))))
                await ctx.send(embed=embed)

    @commands.command(name="leave")
    async def leave(self, ctx: discord.ext.commands.Context):
        vc = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if not vc:
            await ctx.reply("I'm not in a channel at the moment.")
        else:
            await vc.disconnect(force=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Voice(bot))
