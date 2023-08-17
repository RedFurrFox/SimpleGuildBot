from guilded import Color, Colour, Embed
from guilded.ext import commands
import json, aiosqlite, asyncio, os


def main():
	with open("bot_configs.json", "r") as raw_configs:
		jconfigs = json.load(raw_configs)

	client = commands.Bot(commands.when_mentioned_or(jconfigs["interface-config"]["prefix"]), case_insensitive=False, help_command=None)

	@client.event
	async def on_member_join():
		pass

	client.run(configs["tokens"]["guilded_token-REQUIRED"])


if __name__ == "__main__":
	if os.path.isfile("bot_configs.json"):
		with open("bot_configs.json", "r") as r:
			configs = json.load(r)
		if configs["tokens"]["guilded_token-REQUIRED"] in ["", " "]:
			raise Exception('Config the bot first before running it at "bot_configs.json"')
		else:
			main()
	else:
		with open("bot_configs.json", "w") as w:
			w.write("""{
	"tokens": {
		"guilded_token-REQUIRED": ""
	},
	"interface-config": {
		"prefix": "."
	}
}""")
		raise FileNotFoundError('File named "bot_configs.json" not found on initial start. Please open that file and reconfig it before re-running the bot.')
