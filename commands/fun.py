import aiohttp
from discord.ext import commands
import asyncio
import discord
import inspirobot

weather_token = open(r".\tokens\weathertoken.txt").readline()

weather_base_url = "http://api.openweathermap.org/data/2.5/weather?"


class Fun(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command(name="foo")
    async def boop(self, ctx):
        member = ctx.author
        async with ctx.channel.typing():
            await asyncio.sleep(1)
            await ctx.reply(f'Hello {member.name}')

    @commands.command(name="weather")
    async def getweather(self, ctx, city: str, unit: str = None):
        weather_url = weather_base_url + "appid=" + weather_token + "&q=" + city
        async with aiohttp.ClientSession() as session:
            async with session.get(weather_url) as answer:
                x = await answer.json()
                y = x["main"]
                embed = discord.Embed(title="Weather in " + city.capitalize() + "!")
                if x["cod"] == "404":
                    await ctx.reply("City not found...")
                if not unit or unit.lower() == "metric":
                    embed.add_field(name="Temperature {x}:".format(x="(°C)"),
                                    value=round((float(y["temp"]) - 273.15), 1))
                    embed.add_field(name="Pressure {y}:".format(y="(hPa)"), value=y["pressure"])
                    embed.add_field(name="Humidity (%):", value=y["humidity"])
                    await ctx.reply(embed=embed)
                if unit.lower() == "imperial":
                    embed.add_field(name="Temperature {x}:".format(x="(°F)"),
                                    value=round(1.8 * (float(y["temp"]) - 273.15) + 32, 1))
                    embed.add_field(name="Pressure {y}:".format(y="(Hg)"),
                                    value=round(float(y["pressure"]) * 0.02953, 1))
                    embed.add_field(name="Humidity (%):", value=y["humidity"])
                    await ctx.reply(embed=embed)

    @commands.command(name="inspiration")
    async def inspire(self, ctx):
        quote = inspirobot.generate()
        embed = discord.Embed(title="Feeling down? Here is some inspiration.", color= discord.Color.random())
        embed.set_image(url=quote.url)
        await ctx.reply(embed=embed)

    @commands.command(name="sadge")
    async def sadge(self,ctx):
        embed = discord.Embed(title="Sadge")
        embed.set_image(url="attachment://sadge.png")
        await ctx.reply(file=discord.File(r".\funnypictures\sadge.png", filename="sadge.png"), embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
