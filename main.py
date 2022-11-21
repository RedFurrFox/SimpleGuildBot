# Modules
try:
	import os
	import yaml
	import random
	import colorama
	import guilded.embed
	from guilded.ext import commands
except:
	os.system("pip install pyyaml")
	os.system("pip install colorama")
	os.system("pip install guilded.py")


# Colors
class color:
	r = colorama.Fore.RED
	y = colorama.Fore.LIGHTYELLOW_EX
	g = colorama.Fore.LIGHTGREEN_EX
	b = colorama.Fore.LIGHTBLUE_EX
	c = colorama.Fore.LIGHTCYAN_EX
	m = colorama.Fore.LIGHTMAGENTA_EX
	x = colorama.Fore.RESET


# Script Banner
print(f"""
\t  {color.r}___  {color.b}_               _        {color.y}___        {color.g}_  _     _  {color.c}___       {color.g}_   
\t {color.r}/ __|{color.b}(_) _ __   _ __ | | ___  {color.y}/ __| {color.g}_  _ (_)| | __| |{color.c}| _ ) {color.g}___ | |_ 
\t {color.r}\\__ \\{color.b}| || '  \\ | '_ \\| |/ -_){color.y}| (_ |{color.g}| || || || |/ _` |{color.c}| _ \\{color.g}/ _ \\|  _|
\t {color.r}|___/{color.b}|_||_|_|_|| .__/|_|\\___| {color.y}\\___| {color.g}\\_,_||_||_|\\__,_|{color.c}|___/{color.g}\\___/ \\__|
\t                {color.b}|_|                           {color.m}Created By: RedFurrFox
\n""")


# Pointer
class pointer:
	a = f"{color.y}[{color.g}+{color.y}]{color.x}"
	b = f"{color.y}[{color.r}-{color.y}]{color.x}"
	c = f"{color.y}[{color.c}>{color.y}]{color.x}"


# Settings Reader
with open("Settings/settings.yaml", "r") as file:
	reader = yaml.safe_load(file)
	token = reader["Required"]["Bot_Token"]
	prefix = reader["Required"]["Default_prefix"]
	embed_color = reader["Required"]["Embed_Color"]
	topic_template = reader["Templates"]["Topic"]
	b_template = reader["Templates"]["8ball"]

# Prefix Initiator
bot = commands.Bot(command_prefix=prefix)


# Notifier
@bot.event
async def on_ready():
	print(f"{pointer.a} The Bot Is Ready!")


@bot.event
async def on_disconnect():
	print(f"{pointer.b} The Bot Is Offline!")


# Commands
@bot.command()
async def h(ctx):
	print(f"   {pointer.c} Help command triggered")
	await ctx.send(embed=guilded.Embed(title="Help Page",
	                                   description=f"Prefix = {prefix}\n\nHere's my bot commands:\n{prefix}h - show this help command\n{prefix}ping - ping the server where this bot currently run\n{prefix}topic - generate a random topic\n{prefix}b - short for 8ball\n{prefix}source - shows the source code for this bot",
	                                   color=embed_color))


@bot.command()
async def ping(ctx):
	print(f"   {pointer.c} Ping command triggered")
	await ctx.send(embed=guilded.Embed(title="Ping Command", description=f"Pong! at {round(bot.latency * 1000)}ms",
	                                   color=embed_color))


@bot.command()
async def topic(ctx):
	print(f"   {pointer.c} Topic command triggered")
	await ctx.send(
		embed=guilded.Embed(title="Topic Command", description=random.choice(topic_template), color=embed_color))


@bot.command()
async def b(ctx):
	print(f"   {pointer.c} 8ball command triggered")
	await ctx.send(embed=guilded.Embed(title="B Command", description=random.choice(b_template), color=embed_color))


@bot.command()
async def source(ctx):
	print(f"   {pointer.c} Source command triggered")
	await ctx.send(embed=guilded.Embed(title="Source Code", url="https://github.com/RedFurrFox/SimpleGuildBot",
	                                   description=f'Bot script is being maintained by RedFurrFox', color=embed_color))


# Token
bot.run(os.environ['Token'])
# bot.run(token)