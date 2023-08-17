from guilded import Embed, Colour, Color
from guilded.ext import commands
class help(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print("Help command loaded!")

	@commands.command()
	async def help(self, ctx):
		help_embed = Embed(title="help command", description=f"**Pong!**\nTook me around {round(self.bot.latency * 1000)}ms. to respond.",colour=Colour.teal())
		help_embed.set_footer(icon_url=ctx.author.profile,text=f"{ctx.author.display_name} requested this bot command.")
		await ctx.reply(embed=help_embed)

async def setup(bot):
	await bot.add_cog(help(bot))
