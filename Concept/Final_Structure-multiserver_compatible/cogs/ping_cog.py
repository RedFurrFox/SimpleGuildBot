from guilded import Embed, Colour, Color
from guilded.ext import commands
class ping(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("Ping command loaded!")

	@commands.command()
	async def ping(self, ctx):
		ping_embed = Embed(title="Ping command", description=f"**Pong!**\nTook me around {round(self.bot.latency * 1000)}ms. to respond.",colour=Colour.teal())
		ping_embed.set_footer(icon_url=ctx.author.profile,text=f"{ctx.author.display_name} requested this bot command.")
		await ctx.reply(embed=ping_embed)

async def setup(bot):
	await bot.add_cog(ping(bot))
