import time
import json
import random
import asyncio
import guilded
import requests
import virustotal_python
from guilded import Embed
from guilded.ext import commands
from base64 import urlsafe_b64encode

# Database Compiler
with open("database.json", "r+") as rawDB:
	compiledDB = json.load(rawDB)["db"]

# Dictionary
guilded_token = ""  # Required!
vt_token = ""   # leave it empty if you don't have one.
webhooks = [
	"",
	""
]  # Leave it empty if you don't want to get bot notifications.
empty = ["", " "]  # DO NOT MODIFY THIS!

# Webhook Sender
def webhook(msg):
	payload = {"content": f"{msg}\n{'=-' * 13 + '='}"}
	for links in webhooks:
		if links in empty:
			pass
		else:
			requests.post(url=links, data=payload)


robo = commands.Bot(commands.when_mentioned_or(compiledDB["bot-config"]["prefix"]), case_insensitive=False, help_command=None)


def main():
	@robo.event
	async def on_ready():
		print(compiledDB["language"]["d_a1"])
		webhook(compiledDB["language"]["d_a1"])

	@robo.event
	async def on_disconnect():
		print(compiledDB["language"]["d_a2"])
		webhook(compiledDB["language"]["d_a2"])

	@robo.event
	async def on_member_join(joiner):
		if joiner.id in compiledDB["security"]["join-kick"]:
			await asyncio.sleep(compiledDB["bot-config"]["security-timeout"])
			await joiner.kick()
			b_user = compiledDB['security']['join-kick'][joiner.id]
			webhook(f"**{compiledDB['language']['d_a4']}**\n**- Recorded Name:** {b_user['name']}\n**- UserID:** {joiner.id}\n**- Reason:** {b_user['reason']}\n\n**Auto-kick executed!**")
		elif joiner.id in compiledDB["security"]["join-ban"]:
			await asyncio.sleep(compiledDB["bot-config"]["security-timeout"])
			await joiner.ban(f"Blacklisted User. Reason: {b_user['reason']}")
			b_user = compiledDB['security']['join-ban'][joiner.id]
			webhook(f"**{compiledDB['language']['d_a4']}**\n**- Recorded Name:** {b_user['name']}\n**- UserID:** {joiner.id}\n**- Reason:** {b_user['reason']}\n\n**Auto-ban executed!**")
		else:
			pass

	@robo.command(name="h", aliases=["he", "hel", "help", "helps", "helped"])
	async def help_page(ctx, category=None):
		if category is None:
			h_embed = Embed(title="Help page", description="Here's my bot command categories:", colour=guilded.Colour.blue())
			h_embed.add_field(name="Fun", value="List of bot entertainment commands.", inline=False)
			h_embed.add_field(name="Utils", value="List of bot utility commands.", inline=False)
			h_embed.add_field(name="Mod", value="List of bot moderation commands.", inline=False)
		else:
			if category.lower() in ["f", "fu", "fun", "funs", "funny", "funn", "funi"]:
				h_embed = Embed(title="Help page / Fun", colour=guilded.Colour.blue())
				h_embed.add_field(name="Topic", value="Generate a random topics.")
				h_embed.add_field(name="Say", value="Repeat what you said.")
				h_embed.add_field(name="SSay", value="Repeat what you said but no embeds.")
				h_embed.add_field(name="Rate", value="Rate someone.")
				h_embed.add_field(name="Dice", value="Randomly choose numbers from 1 to 6.")
				h_embed.add_field(name="CoinToss", value="Randomly choose heads or tails.")
				h_embed.add_field(name="GayMeter", value="Generate a gay percentage of people")
			elif category.lower() in ["u", "ut", "uti", "util", "utils", "utility", "utili", "utilit"]:
				h_embed = Embed(title="Help page / Utils", colour=guilded.Colour.blue())
				h_embed.add_field(name="Help", value="Show this help page.")
				h_embed.add_field(name="Ping", value="Shows the processing time of the server.")
				h_embed.add_field(name="CheckID", value="Check if the given userid is in the blacklist.")
				h_embed.add_field(name="URLScan", value="Scan suspicious links and return a useful info about the given url.")
				h_embed.add_field(name="WebCode", value="Shows the given website code definition.")
				h_embed.add_field(name="Compare", value="Compare two strings.")
				h_embed.add_field(name="Version", value="Show the code's version.")
				h_embed.add_field(name="SourceCode", value="Show the source code of this bot.")
			elif category.lower() in ["m", "mo", "mod", "mods", "moderation", "mode", "moder", "modera", "moderat", "moderati", "moderatio", "moderations", "modding", "modd"]:
				h_embed = Embed(title="Help page / Mod", description="Coming Soon.", colour=guilded.Colour.blue())
			else:
				h_embed = Embed(title="Help page / Error page", description="Unknown category type.", colour=guilded.Colour.red())
		h_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=h_embed)

	@robo.command(name="topic", aliases=["topi","top", "to"])
	async def topic_command(ctx):
		gen_topic = random.choice(compiledDB["dialogs"]["topics"])
		topic_embed = Embed(title="Topic command", description=gen_topic, colour=guilded.Colour.teal())
		topic_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=topic_embed)

	@robo.command(name="say", aliases=["sa", "says", "sayin", "saying", "said"])
	async def say_command(ctx, *, message=None):
		if message is not None:
			say_embed = Embed(title="Say command", description=message, colour=guilded.Colour.teal())
		else:
			say_embed = Embed(title="Say command / Error page", description=f"Please specify what do you want to say.\nExample: `{compiledDB['bot-config']['prefix']}say Hello World!`", colour=guilded.Colour.red())
		say_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=say_embed)

	@robo.command(name="ssay", aliases=["ssa", "ss", "ssays", "ssayin", "ssaying", "ssaid"])
	async def ssay_command(ctx, *, message=None):
		if message is not None:
			await ctx.reply(f"{message}")
		else:
			say_embed = Embed(title="SSay command / Error page", description=f"Please specify what do you want to say.\nExample: `{compiledDB['bot-config']['prefix']}ssay Hello World!`", colour=guilded.Colour.teal())
			say_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
			await ctx.reply(embed=say_embed)

	@robo.command(name="rate", aliases=["rat", "ra", "rated", "rati", "ratin", "rating", "rates"])
	async def rate_command(ctx, *, message=None):
		gen_num = random.randint(-3,15)
		if message is not None:
			rate_embed = Embed(title="Rate command", description=f"I'll rate **{message}** a {gen_num}/10", colour=guilded.Colour.teal())
		else:
			rate_embed = Embed(title="Rate command", description=f"I'll rate **{ctx.author.display_name}** a {gen_num}/10", colour=guilded.Colour.teal())
		rate_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=rate_embed)

	@robo.command(name="dice", aliases=["dic", "di", "die", "dices", "dici", "dicin", "dicing"])
	async def dice_command(ctx):
		dice_embed = Embed(title="Dice command", description=f"{random.randint(1,6)}", colour=guilded.Colour.teal())
		dice_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=dice_embed)

	@robo.command(name="cointoss", aliases=["cointos", "cointo", "coint", "coin", "coi", "coins"])
	async def cointoss_command(ctx):
		cointoss_embed = Embed(title="Dice command", description=f"{random.choice(['Heads', 'Tails'])}", colour=guilded.Colour.teal())
		cointoss_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=cointoss_embed)

	@robo.command(name="gaymeter", aliases=["gaymete", "gaymet", "gayme", "gaym", "gay", "ga"])
	async def gaymeter_command(ctx, message=None):
		gen_num = random.randint(0, 101)
		if message is not None:
			rate_embed = Embed(title="Rate command", description=f"**{message}** is {gen_num}% gay", colour=guilded.Colour.teal())
		else:
			rate_embed = Embed(title="Rate command", description=f"**{ctx.author.display_name}** is {gen_num}% gay", colour=guilded.Colour.teal())
		rate_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=rate_embed)

	@robo.command(name="ping", aliases=["pin", "pi", "p", "pings", "pingi", "pingin", "pinging"])
	async def ping_command(ctx):
		ping_embed = Embed(title="Ping command", description=f"**Pong!** at {round(robo.latency*1000)}ms.", colour=guilded.Colour.teal())
		ping_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=ping_embed)

	@robo.command(name="checkid", aliases=["checki", "check", "chec", "che", "ch", "cid"])
	async def checkid_command(ctx, message=None):
		if message is not None:
			IDInUse = message
		else:
			IDInUse = ctx.author.id
		if IDInUse in compiledDB["security"]["join-kick"] or compiledDB["security"]["join-ban"]:
			checkid_embed = Embed(title="CheckID command", description=f"{IDInUse} was found in the blacklisted users.", colour=guilded.Colour.red())
		else:
			checkid_embed = Embed(title="CheckID", description=f"{IDInUse} was not found in the blacklisted users.", colour=guilded.Colour.green())
		checkid_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=checkid_embed)

	@robo.command(name="urlscan", aliases=["urlsca", "urlsc", "urls", "url", "ur", "scan", "scanurl", "scans"])
	async def urlscan_command(ctx, message=None):
		if vt_token not in empty:
			if message is not None:
				cache = 0
				if message.startswith("[") and message.endswith(")"):
					cache += 1
				if cache == 1:
					sliced_url = message.split("(")[1]
					url = sliced_url.replace(")", "")
				else:
					url = message
				with virustotal_python.Virustotal(API_KEY=vt_token) as vtotal:
					try:
						vtotal.request("urls", data={"url": url}, method="POST")
						# Safe encode URL in base64 format
						# https://developers.virustotal.com/reference/url
						url_id = urlsafe_b64encode(url.encode()).decode().strip("=")
						report = vtotal.request(f"urls/{url_id}")
						# print(json.dumps(report.data, indent=2))
						dumpjson = json.dumps(report.data, indent=2)
						readjson = json.loads(dumpjson)
						# scan parser type: rescan
						total_votes_harmless = readjson["attributes"]["total_votes"]["harmless"]
						total_votes_malicious = readjson["attributes"]["total_votes"]["malicious"]
						threat_names = readjson["attributes"]["threat_names"]
						reputation = readjson["attributes"]["reputation"]
						title = readjson["attributes"]["title"]
						last_analysis_harmless = readjson["attributes"]["last_analysis_stats"]["harmless"]
						last_analysis_malicious = readjson["attributes"]["last_analysis_stats"]["malicious"]
						last_analysis_suspicious = readjson["attributes"]["last_analysis_stats"]["suspicious"]
						last_analysis_undetected = readjson["attributes"]["last_analysis_stats"]["undetected"]
						scan_type = readjson["type"]
						scan_id = readjson["id"]
						scan_link = readjson["links"]["self"]
						# print(dumpjson+"\n\n\n")
						urlscan_embed = guilded.Embed(title="Scan Command", description=f'Url target scan: "{url} :: {title}"\n\nTotal votes: \n - harmless: {total_votes_harmless}\n - malicious: {total_votes_malicious}\n\nReputation: {reputation}\n\nThreat names:\n - {threat_names}\n\nScan-harmless: {last_analysis_harmless}\nScan-malicious: {last_analysis_malicious}\nScan-suspicious: {last_analysis_suspicious}\nScan-undetected: {last_analysis_undetected}\n\nScan Type: {scan_type}\nScan ID:\n - {scan_id}\nScan Link:\n - {scan_link}', color=guilded.Colour.dark_magenta())
					except virustotal_python.VirustotalError as err:
						urlscan_embed = guilded.Embed(title="Scan Command", description=f"Failed to send URL: {url} for analysis and get the report: {err}", colour=guilded.Colour.red())
			else:
				urlscan_embed = Embed(title="URLScan command / Error page", description=f"This command requires links to scan.\nExample: `{compiledDB['bot-config']['prefix']}urlscan guilded.gg`", colour=guilded.Colour.red())
		else:
			urlscan_embed = Embed(title="URLScan command / Error page", description="URL scanning feature is disabled.\nError Code: NO_VTTOKEN_FOUND", colour=guilded.Colour.red())
		urlscan_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=urlscan_embed)

	@robo.command(name="webcode", aliases=["webcod", "webco", "webc", "web", "we", "statuscode", "statuscodes", "statcode", "code", "codes"])
	async def webcode_command(ctx, message=None):
		if message is not None:
			if message in compiledDB["status-code"]:
				res_parser1 = compiledDB["status-code"][message]
				res_parser2 = res_parser1.split("-")[0] + " - " + res_parser1.split("-")[1]
				res_parser3 = res_parser1.split("-")[2]
				webcode_embed = Embed(title="Webcode command", description=f'**{res_parser2}**\n{res_parser3}', colour=guilded.Colour.teal())
			else:
				if message.lower() == "attribution":
					webcode_embed = Embed(title="Webcode command", description=compiledDB["status-code"][message], colour=guilded.Colour.teal())
				else:
					res_parser1 = compiledDB["status-code"]["invalid-code"]
					res_parser2 = res_parser1.split("-")[0] + " - " + res_parser1.split("-")[1]
					res_parser3 = res_parser1.split("-")[2]
					webcode_embed = Embed(title="Webcode command", description=f'**{res_parser2}**\n{res_parser3}', colour=guilded.Colour.teal())
		else:
			webcode_embed = Embed(title="Webcode command / Error page", description=f"This command requires a code for it to work.\nExample: `{compiledDB['bot-config']['prefix']}webcode 200`", colour=guilded.Colour.red())
		webcode_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=webcode_embed)

	@robo.command(name="compare", aliases=["compar", "compa", "comp","com", "co", "compari", "comparin", "comparing", "compares"])
	async def compare_command(ctx, var1=None, var2=None):
		if var1 is not None and var2 is not None:
			if var1 == var2:
				compare_embed = Embed(title="Compare command", description="Matched!", colour=guilded.Colour.green())
			else:
				compare_embed = Embed(title="Compare command", description="Not matched!", colour=guilded.Colour.red())
		else:
			compare_embed = Embed(title="Compare command / Error page", description=f"This command requires two strings.\nExample: `{compiledDB['bot-config']['prefix']}compare 123456789 123456789`", colour=guilded.Colour.red())
		compare_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=compare_embed)

	@robo.command(name="version", aliases=["versio", "versi", "vers", "ver", "ve", "versions"])
	async def version_command(ctx):
		version_embed = Embed(title="Version command", description=f"This bot is running on **{compiledDB['dev-area']['version']}**.", colour=guilded.Colour.teal())
		version_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=version_embed)

	@robo.command(name="sourcecode", aliases=["sourcecod", "sourceco", "sourcec", "source", "sourc", "sources"])
	async def sourcecode_command(ctx):
		sourcecode_embed = Embed(title="sourcecode command", description=f"This bot is an open-source project.\nVisit https://github.com/RedFurrFox/SimpleGuildBot for more info.\n\nBot Script is being maintained by RedFurrFox.", colour=guilded.Colour.gold())
		sourcecode_embed.set_footer(text=f"{ctx.author.display_name} {compiledDB['language']['d_a3']}")
		await ctx.reply(embed=sourcecode_embed)

	@robo.command(name="whoami")
	async def whoami_command(ctx):
		if ctx.author.id not in ["m7zwexld"]:
			pass
		else:
			await ctx.reply(embed=Embed(title="WhoAmI command", description=f"The person who created me. Hello master {ctx.author.display_name}!", colour=guilded.Colour.gold()))

if __name__ == "__main__":
	main()
	robo.run(guilded_token)
