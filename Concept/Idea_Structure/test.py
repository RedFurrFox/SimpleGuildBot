from guilded import Embed, Color, Colour
from guilded.ext import commands

prefix = "."
guilded_token = ""

client = commands.Bot(commands.when_mentioned_or(prefix), case_insensitive=False, help_command=None)

def main():

	@client.event
	async def on_ready():
		print("The bot named {0} ({1}) is online!".format(client.user.name,client.user.id))

	@client.event
	async def on_member_join(member):
		print("New member named {0} ({1}) joined {2}".format(member.name,member.id,member.server))

	@client.event
	async def on_message():
		pass

if __name__ == "__main__":
	main()
	client.run(guilded_token)
