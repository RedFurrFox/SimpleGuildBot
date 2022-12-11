# Modules
try:
  import os
  import yaml
  import json
  import random
  import colorama
  import guilded.embed
  import virustotal_python
  from guilded.ext import commands
  from base64 import urlsafe_b64encode
except:
  # Auto-install required modules
  os.system("pip install pyyaml")
  os.system("pip install colorama")
  os.system("pip install guilded.py")
  os.system("pip install virustotal-python")
  # Recalling modules for new installed modules
  import yaml
  import colorama
  import virustotal_python
  from guilded.ext import commands
  import guilded.embed, guilded.ext


# Color Types
class color:
  r = colorama.Fore.RED
  y = colorama.Fore.LIGHTYELLOW_EX
  g = colorama.Fore.LIGHTGREEN_EX
  b = colorama.Fore.LIGHTBLUE_EX
  c = colorama.Fore.LIGHTCYAN_EX
  m = colorama.Fore.LIGHTMAGENTA_EX
  x = colorama.Fore.RESET


# Pointer Types
class pointer:
  a = f"{color.y}[{color.g}+{color.y}]{color.x}"
  b = f"{color.y}[{color.r}-{color.y}]{color.x}"
  c = f"{color.y}[{color.c}>{color.y}]{color.x}"
  d = f"{color.y}[{color.m}={color.y}]{color.x}"
  e = f"{color.y}[{color.b}:{color.y}]{color.x}"


# Space/Tab Types
class space:
  a = "   "
  b = "      "


# Posix type
if os.name == 'posix':
  nav = "/"
else:
  nav = "\\"

  
# Spacer
def line():
  print(color.g)
  print("=-" * 40)
  print(color.x)


# Terminal Logger Handler
def log_handler(space_T, pointer_T, message):
  if space_T == "a":
    space_T = space.a
  elif space_T == "b":
    space_T = space.b
  elif space_T == "x":
    space_T = ""
  else:
    exit("Invalid data for func. log_handler/space_T")
  if pointer_T == "a":
    pointer_T = pointer.a
  elif pointer_T == "b":
    pointer_T = pointer.b
  elif pointer_T == "c":
    pointer_T = pointer.c
  elif pointer_T == "d":
    pointer_T = pointer.d
  elif pointer_T == "e":
    pointer_T = pointer.e
  elif pointer_T == "x":
    pointer_T = ""
  else:
    exit("Invalid data for func. log_handler/pointer_T")
  print(f'''{(space_T)}{pointer_T} {message}''')


# Terminal cleaner
def terminal_cleaner():
  if os.name == "posix":
    os.system("clear")
  else:
    os.name("cls")
  
  
# Definition configs
Token_for_guilded_in_use = ""
Token_for_virustotal_in_use = ""
VirToken = ""


# Script Banner
terminal_cleaner()
print(f"""
\t  {color.r}___  {color.b}_               _        {color.y}___        {color.g}_  _     _  {color.c}___       {color.g}_   
\t {color.r}/ __|{color.b}(_) _ __   _ __ | | ___  {color.y}/ __| {color.g}_  _ (_)| | __| |{color.c}| _ ) {color.g}___ | |_ 
\t {color.r}\\__ \\{color.b}| || '  \\ | '_ \\| |/ -_){color.y}| (_ |{color.g}| || || || |/ _` |{color.c}| _ \\{color.g}/ _ \\|  _|
\t {color.r}|___/{color.b}|_||_|_|_|| .__/|_|\\___| {color.y}\\___| {color.g}\\_,_||_||_|\\__,_|{color.c}|___/{color.g}\\___/ \\__|
\t                {color.b}|_|                           {color.m}Created By: RedFurrFox{color.x}\n""")


# Settings Reader
with open(f"Settings{nav}settings.yaml", "r") as file:
  reader = yaml.safe_load(file)
  guilded_token = reader["Required"]["GuildedBot_API_Token"]
  virustotal_token = reader["Required"]["VirusTotal_API_Token"]
  prefix = reader["Required"]["Default_prefix"]
  embed_color = reader["Required"]["Embed_Color"]
  mod_channel = reader["Security"]["Mod_channel"]
  blacklisted_ban = reader["Security"]["Join_ban"]
  blacklisted_kick = reader["Security"]["Join_kick"]
  topic_template = reader["Templates"]["Topic"]
  b_template = reader["Templates"]["8ball"]

  
# Prefix Initiator
bot = commands.Bot(commands.when_mentioned_or(prefix), case_insensitive=True, help_command=None)


# Events
@bot.event
async def on_ready():
  cache_1 = 1   # Avoid info printing repitation when bot went offline then go online
  log_handler(space_T="a", pointer_T="a", message="The Bot Is Online!")
  if cache_1 == 1:
    cache_1 = cache_1 + 1
    log_handler(space_T="b", pointer_T="d", message=f'VirusTotal token path in use: "{Token_for_virustotal_in_use}".')
    log_handler(space_T="b", pointer_T="d", message=f'Guilded token path in use: "{Token_for_guilded_in_use}".')
    log_handler(space_T="b", pointer_T="d", message=f'SimpleGuildBot is currently running on "{bot.user.name} :: {bot.user.id}".')
    line()
    log_handler(space_T="x", pointer_T="e", message="Bot Data Logs:")
  else:
    pass


@bot.event
async def on_disconnect():
  log_handler(space_T="a", pointer_T="a", message="The Bot Is Offline!")


@bot.event
async def on_member_join(member):
  # Join ban
  if member.id in blacklisted_ban:
    log_handler(space_T="a", pointer_T="c", message="Blacklisted User Joined! Banning.")
    log_handler(space_T="b", pointer_T="d", message=f'User: "{member.name} :: {member.id}"')
    await member.ban(reason="Blacklisted User")
  else:
    pass
  # Join kick
  if member.id in blacklisted_kick:
    log_handler(space_T="a", pointer_T="c", message="Blacklisted User Joined! Kicking.")
    log_handler(space_T="b", pointer_T="d", message=f'User: "{member.name} :: {member.id}"')
    await member.kick()
  else:
    pass


# Commands
@bot.command(name="help", aliases=["h", "commands", "command"])
async def help(ctx):
  log_handler(space_T="a", pointer_T="c", message="Help command triggered")
  await ctx.send(embed=guilded.Embed(title="Help Page", description= f"Prefix = {prefix}\n\nHere's my bot commands:\n{prefix}help - show this help command\n{prefix}ping - ping the server where this bot currently run\n{prefix}topic - generate a random topic\n{prefix}8ball - randomly answer yes, no and other stuff\n{prefix}cointoss - randomly choose heads or tails\n{prefix}urlscan - scan a suspicious link (Currently not available)\n{prefix}code - shows the meaning of a status code from a website\n{prefix}source - shows the source code for this bot", color=embed_color))


@bot.command(name="ping", aliases=["p"])
async def ping(ctx):
  data = f"{round(bot.latency * 1000)}ms"
  log_handler(space_T="a", pointer_T="c", message="Ping command triggered.")
  log_handler(space_T="b", pointer_T="d", message=f'Data: "{data}"')
  await ctx.send(embed=guilded.Embed(title="Ping Command", description=f"Pong! at {data}", color=embed_color))
  del(data)


@bot.command(name="topic", aliases=["t", "topics"])
async def topic(ctx):
  data = random.choice(topic_template)
  log_handler(space_T="a", pointer_T="c", message="Topic command triggered.")
  log_handler(space_T="b", pointer_T="d", message=f'Data: "{data}"')
  await ctx.send(embed=guilded.Embed(title="Conversation Starter Command", description=data, color=embed_color))
  del(data)


@bot.command(name="8ball", aliases=["b", "ball"])
async def b(ctx, *, guess):
  data = random.choice(b_template)
  log_handler(space_T="a", pointer_T="c", message="8ball command triggered.")
  log_handler(space_T="b", pointer_T="d", message=f'Data: "{guess} :: {data}"')
  await ctx.send(embed=guilded.Embed(title="8Ball Command", description=data, color=embed_color))
  del(data)


@bot.command(name="cointoss", aliases=["toss", "coin"])
async def cointoss(ctx):
  data = random.choice['heads', 'tails']
  log_handler(space_T="a", pointer_T="c", message="Coin-toss command triggered.")
  log_handler(space_T="b", pointer_T="d", message=f'Data: "{data}"')
  await ctx.send(embed=guilded.Embed(title="Coin Toss Command", description=data, color=embed_color))
  del (data)


@bot.command(name="code", aliases=["statuscode", "httpcode", "responsecode"])
async def code(ctx, *, status_code):
  log_handler(space_T="a", pointer_T="c", message="Status code command triggered.")
  log_handler(space_T="b", pointer_T="d", message=f'Data: "{status_code}"')
  try:
    with open(os.path.join(f"Settings{nav}status_codes",
                           status_code + ".txt")) as status:
      result = status.read()
  except FileNotFoundError:
    with open(os.path.join(f"Settings{nav}status_codes", "invalid_code.txt"),
              "r") as invalid:
      result = invalid.read()
  if status_code == "ATTRIBUTION" or status_code == "LICENSE" or status_code == "invalid_code":
    with open(os.path.join(f"Settings{nav}status_codes", "invalid_code.txt"),
              "r") as invalid:
      result = invalid.read()
  await ctx.send(embed=guilded.Embed(
    title="Status Code Info Command", description=result, color=embed_color))


@bot.command(name="urlscan", aliases=["scan", "check", "inspect"])
async def scan(ctx, *, url):
  log_handler(space_T="a", pointer_T="c", message="Scan command triggered.")
  log_handler(space_T="b", pointer_T="d", message=f'Data: "{url}"')
  for val in url:
    if val == "[":
      await ctx.send(embed=guilded.Embed(title="Scan Command (Tip)", description=f"Invalid link format! Try typing your link without website protocol(i.e.: http and https or www) to make it valid.", color=embed_color))
      pass
  with virustotal_python.Virustotal(API_KEY=VirToken) as vtotal:
    try:
        resp = vtotal.request("urls", data={"url": url}, method="POST")
        # Safe encode URL in base64 format
        # https://developers.virustotal.com/reference/url
        url_id = urlsafe_b64encode(url.encode()).decode().strip("=")
        report = vtotal.request(f"urls/{url_id}")
        # print(json.dumps(report.data, indent=2))
        dumpjson = json.dumps(report.data, indent=2)
        readjson = json.loads(dumpjson)
        # json scan info parser type: rescan
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
        await ctx.send(embed=guilded.Embed(title="Scan Command", description=f'Url target scan: "{url} :: {title}"\n\nTotal votes: \n - harmless: {total_votes_harmless}\n - malicious: {total_votes_malicious}\n\nReputation: {reputation}\n\nThreat names:\n - {threat_names}\n\nScan-harmless: {last_analysis_harmless}\nScan-malicious: {last_analysis_malicious}\nScan-suspicious: {last_analysis_suspicious}\nScan-undetected: {last_analysis_undetected}\n\nScan Type: {scan_type}\nScan ID:\n - {scan_id}\nScan Link:\n - {scan_link}', color=embed_color))
    except virustotal_python.VirustotalError as err:
        await ctx.send(embed=guilded.Embed(title="Scan Command", description=f"Failed to send URL: {url} for analysis and get the report: {err}", color=embed_color))


@bot.command(name="source", aliases=["s", "sourcecode"])
async def source(ctx):
  log_handler(space_T="a", pointer_T="c", message="Source command triggered.")
  await ctx.send(embed=guilded.Embed(
    title="Source Code",
    url="https://github.com/RedFurrFox/SimpleGuildBot",
    description=f'Bot script is being maintained by RedFurrFox',
    color=embed_color))


# Token
try:
  line()
  log_handler(space_T="x", pointer_T="e", message="Start Data Logs:")
  if virustotal_token == "":
    log_handler(space_T="a", pointer_T="b", message='No virustotal token found in settings! Trying secrets named "VTToken".')
    Token_for_virustotal_in_use = "Secrets"
    VirToken = os.environ['VTToken']
  else:
    Token_for_virustotal_in_use = "Settings"
    VirToken = virustotal_token
  if guilded_token == "":
    log_handler(space_T="a", pointer_T="b", message='No guilded token found in settings! Trying secrets named "GToken".')
    Token_for_guilded_in_use = "Secrets"
    bot.run(os.environ['GToken'])
  else:
    Token_for_guilded_in_use = "Settings"
    bot.run(guilded_token)
except Exception as error:
  exit(f"{space.a}{pointer.b} WARNING: Unexpected Error Encountered!\n{error}\n\n")
