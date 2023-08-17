import asyncio, os, guilded, json
from guilded.ext import commands

with open('bot_configx.json', "r") as raw_bot_config:
	bot_config = json.load(raw_bot_config)

guilded_token = bot_config['tokens']['guilded_token']

bot = commands.Bot(commands.when_mentioned_or(bot_config['bot_configs']['prefix']), case_insensitive=False, help_command=None)

async def cogs_loader():
	for file_name in os.listdir('./cogs'):
		if file_name.endswith('_cog.py'):
			await bot.load_extension(f'cogs.{file_name[:-7]}')

async def main():
	await cogs_loader()
	await bot.start(guilded_token)

asyncio.run(main())
