import os, json, asyncio, logging, requests, random
from nextguild import Client, Events, Embed

colors = {
	"Light_Red": 16762315,
	"Light_Orange": 16770244,
	"Light_Yellow": 16775885,
	"Light_Green": 12451017,
	"Light_Blue": 12578815,
	"Light_Violet": 15132410,
	"Light_Grey": 13882323,
	"Dark_Red": 16711680,
	"Dark_Orange": 16747520,
	"Dark_Yellow": 16766720,
	"Dark_Green": 32768,
	"Dark_Blue": 255,
	"Dark_Violet": 9699539,
	"Dark_Grey": 6908265,
	"White": 16777215,
	"Black": 0,
	"no_color": ""
}

def random_all():
	return random.choice(list(colors.values()))

def random_light():
	c_l = []
	for light in colors:
		if light.startswith("Light"):
			c_l.append(colors[light])
	return random.choice(c_l)

def random_dark():
	c_d = []
	for dark in colors:
		if dark.startswith("Dark"):
			c_d.append(colors[dark])
	return random.choice(c_d)


def main():
	robo = Client(token=guilded_api)
	events = Events(robo)

	@events.on_ready
	async def on_ready(bot):
		global bot_id
		bot_id = bot.user_id
		print(f"{bot.name}({bot_id}) is online!")

	"""@events.on_disconnect
	async def on_disconnect(bot):
		print(f"{bot.name} went offline!")"""

	@events.on_message
	async def command_handler(message):
		if message.created_by == bot_id:
			return

		if message.content.lower().startswith(prefix):
			list_contents = message.content.lower().split(" ")
			hint = list_contents[0][prefix_count:]

			if hint in cached_commands:
				counted_list_contents = len(list_contents)
				user_info = robo.get_server_member(server_id=message.server_id, user_id=message.created_by)
				# robo.send_message(message.channel_id, content=json.dumps(user_info, indent=2))

				if hint in available_commands["help"]:
					if counted_list_contents == 1:
						h_emb = Embed(title="Help Page", description="Here's my bot command categories:", color=random_light(), footer_icon=user_info["user"]["avatar"], footer=f"{user_info['user']['name']} at {message.created_at.split('T')[0]}.")
						h_emb.add_field(name="Fun", value="List of bot entertainment commands.")
						h_emb.add_field(name="Utils", value="List of bot utility commands.")
						h_emb.add_field(name="Mod", value="List of bot moderation commands.")
					else:
						if list_contents[1] in ["f", "fu", "fun", "funs", "funny", "funn", "funi"]:
							h_emb = Embed(title="Help page / Fun", color=random_light(), footer_icon=user_info["user"]["avatar"], footer=f"{user_info['user']['name']} at {message.created_at.split('T')[0]}.")
							h_emb.add_field(name="Topic", value="Generate a random choice of topics.", inline=True)
							h_emb.add_field(name="8Ball", value="Generate an random choice of answer.", inline=True)
							h_emb.add_field(name="Joke", value="Generate a random choice of joke", inline=True)
							h_emb.add_field(name="Say", value="Repeat what you said.", inline=True)
							h_emb.add_field(name="SSay", value="Repeat what you said but no embeds.", inline=True)
							h_emb.add_field(name="Dispo", value="Send a disposable message", inline=True)
							h_emb.add_field(name="Rate", value="Rate someone.", inline=True)
							h_emb.add_field(name="Dice", value="Randomly choose numbers from 1 to 6.", inline=True)
							h_emb.add_field(name="CoinToss", value="Randomly choose heads or tails.", inline=True)
							h_emb.add_field(name="GayMeter", value="Generate a gay percentage of people", inline=True)
							h_emb.add_field(name="LoveMeter", value="Generate a love percentage of people", inline=True)
						elif list_contents[1] in ["u", "ut", "uti", "util", "utils", "utility", "utili", "utilit"]:
							h_emb = Embed(title="Help page / Utils", color=random_light(), footer_icon=user_info["user"]["avatar"], footer=f"{user_info['user']['name']} at {message.created_at.split('T')[0]}.")
							h_emb.add_field(name="Help", value="Show this help page.", inline=True)
							h_emb.add_field(name="Ping", value="Shows the processing time of the server.", inline=True)
							h_emb.add_field(name="QR", value="Generate a QR code.", inline=True)
							h_emb.add_field(name="URLScan", value="Scan suspicious links and return a useful info about the given url.", inline=True)
							h_emb.add_field(name="WebCode", value="Shows the given website code definition.", inline=True)
							h_emb.add_field(name="Compare", value="Compare two strings.", inline=True)
							h_emb.add_field(name="Version", value="Show the code's version.", inline=True)
							h_emb.add_field(name="SourceCode", value="Show the source code of this bot.", inline=True)
						elif list_contents[1] in ["m", "mo", "mod", "mods", "moderation", "mode", "moder", "modera", "moderat", "moderati", "moderatio", "moderations", "modding", "modd"]:
							h_emb = Embed(title="Help page / Mod", color=random_light(), footer_icon=user_info["user"]["avatar"], footer=f"{user_info['user']['name']} at {message.created_at.split('T')[0]}.")
							h_emb.add_field(name="Kick", value="Kick a user out of this server.", inline=True)
							h_emb.add_field(name="Ban", value="Ban a user out of this server.", inline=True)
							h_emb.add_field(name="CheckID", value="Check if the given userid is in the blacklist.", inline=True)
							h_emb.add_field(name="AddRole", value="Add a role to a user.", inline=True)
							h_emb.add_field(name="RemoveRole", value="Remove a role to a user.", inline=True)
							h_emb.add_field(name="Purge", value="Remove multiple messages.", inline=True)
							h_emb.add_field(name="NoURL", value="Forbid anyone from sending any links (including medias like images).", inline=True)
							h_emb.add_field(name="NoEntry", value="Forbid anyone from joining this server.", inline=True)
							h_emb.add_field(name="NoMessage", value="Forbid anyone from sending any kind of messages.", inline=True)
							h_emb.add_field(name="ClearInvites", value="Remove all invite links for this server.", inline=True)
							h_emb.add_field(name="GlobalAddRole", value="Add a role for every members in this server.", inline=True)
							h_emb.add_field(name="GlobalRemoveRole", value="Remove a role for every members in this server.", inline=True)
							h_emb.add_field(name="Report", value="Report a bug from the developer of this bot.", inline=True)
						else:
							h_emb = Embed(title="Help page / Error page", description=f'Unknown category type `{list_contents[1]}`.', color=colors["Dark_Red"])
					robo.send_message(message.channel_id, embed=h_emb)

				elif hint in available_commands["topic"]:
					topic_emb = Embed(title="Topic command", description=random.choice(configs["entertainments"]["topics"]), color=random_light(), footer_icon=user_info["user"]["avatar"], footer=f"{user_info['user']['name']} at {message.created_at.split('T')[0]}.")
					robo.send_message(message.channel_id, embed=topic_emb)

				elif hint in available_commands["8ball"]:
					Eightball_emb = Embed(title="8Ball command", description=random.choice(configs["entertainments"]["8ball"]), color=random_light(), footer_icon=user_info["user"]["avatar"], footer=f"{user_info['user']['name']} at {message.created_at.split('T')[0]}.")
					robo.send_message(message.channel_id, embed=Eightball_emb)

				elif hint in available_commands["joke"]:
					joke_emb = Embed(title="Joke command", description=random.choice(configs["entertainments"]["jokes"]), color=random_light(), footer_icon=user_info["user"]["avatar"], footer=f"{user_info['user']['name']} at {message.created_at.split('T')[0]}.")
					robo.send_message(message.channel_id, embed=joke_emb)

				elif hint in available_commands["say"]:
					if counted_list_contents == 1:
						say_emb = Embed(title="Say command / Error page", description=f"Messaage to be sent cannot be empty.\n\n**Example:**\n```{prefix}Say <<<YOUR-MESSAGE-HERE>>>```", color=colors["Dark_Red"], footer_icon=user_info["user"]["avatar"], footer=f"{user_info['user']['name']} at {message.created_at.split('T')[0]}.")
					else:
						say_emb = Embed(title="Say command", description=message.content[(prefix_count+len(hint)):], color=random_light(), footer_icon=user_info["user"]["avatar"], footer=f"{user_info['user']['name']} at {message.created_at.split('T')[0]}.")
					robo.send_message(message.channel_id, embed=say_emb)

				elif hint in available_commands["ssay"]:
					if counted_list_contents == 1:
						ssay_emb = Embed(title="SSay command / Error page", description=f"Messaage to be sent cannot be empty.\n\n**Example:**\n```{prefix}SSay <<<YOUR-MESSAGE-HERE>>>```", color=colors["Dark_Red"], footer_icon=user_info["user"]["avatar"], footer=f"{user_info['user']['name']} at {message.created_at.split('T')[0]}.")
						robo.send_message(message.channel_id, embed=ssay_emb)
					else:
						robo.send_message(message.channel_id, content=message.content[(prefix_count+len(hint)):])

				elif hint in available_commands["dispo"]:
					robo.delete_message(message.channel_id, message.message_id)
					dispo1_emb = Embed(title="Dispo command", description=message.content[(prefix_count+len(hint)):], footer_icon=user_info["user"]["avatar"], footer=f"Anonymous user at {message.created_at.split('T')[0]}.")
					dispo2_emb = Embed(title="Dispo command / Hint", description=f"Hey <@{message.created_by}>, you have sent a disposable message!\nThe message you have sent will be automatically removed after 1 minute.", color=random_light())
					dispo1_mes = robo.send_message(message.channel_id, embed=dispo1_emb)
					dispo2_mes = robo.send_message(message.channel_id, embed=dispo2_emb, is_private=True)
					await asyncio.sleep(15)
					robo.delete_message(message.channel_id, dispo2_mes.message_id)
					await asyncio.sleep(45)
					robo.delete_message(message.channel_id, dispo1_mes.message_id)


			else:
				return

	asyncio.run(events.run())


if __name__ == "__main__":
	# Bypass json-to-str
	guilded_api = ""
	virustotal_api = ""
	google_safe_browsing_api = ""
	prefix = ""

	available_commands = {
		"topic": ["topic", "t", "to", "top", "topi", "topics"],
		"8ball": ["8ball", "8b", "8ba", "8bal", "8ball", "8-b", "8-ba", "8-bal", "8-ball"],
		"joke": ["joke", "j", "jo", "jok", "jokes"],
		"say": ["say", "s", "sa", "sai", "said", "ssays"],
		"ssay": ["ssay", "ss", "ssa", "ssai", "ssaid", "ssays"],
		"dispo": ["dispo", "di", "dis", "disp", "dispos", "disposa", "disposab", "disposabl", "disposable", "dispose"],
		"rate": ["rate", "ra", "rat", "rati", "ratin", "rating", "ratings", "rates"],
		"dice": ["dice", "d", "di", "dic", "dices", "diced", "die"],
		"coinToss": ["cointoss", "c", "co", "coi", "coin", "coint", "cointo", "cointos", "to", "tos", "toss"],
		"gaymeter": ["gaymeter", "g", "ga", "gay", "gaym", "gayme", "gaymet", "gaymete", "gm", "gme", "gmet", "gmete", "gmeter"],
		"lovemeter": ["lovemeter", "l", "lo", "lov", "love", "lovem", "loveme", "lovemet", "lovemete", "lm", "lme", "lmet", "lmete", "lmeter"],
		"help": ["help", "h", "he", "hel"],
		"ping": ["ping", "p", "pi", "pin"],
		"qr": ["qr", "qrc", "qrco", "qrcod", "qrcode"],
		"checkid": ["checkid", "ch", "cid", "che", "chec", "check", "checki"],
		"urlscan": ["urlscan"],
		"webcode": ["webcode"],
		"compare": ["compare"],
		"version": ["version"],
		"sourcecode": ["sourcecode"],

	}
	cached_commands = []

	for item, value in available_commands.items():
		cached_commands.extend(value)

	if os.name == "posix":
		path_classifier = "/"
	else:
		path_classifier = "\\"

	if os.path.isfile('configs.json'):
		with open("configs.json", "r+") as cr:
			configs = json.load(cr)
		guilded_api += configs["apis"]["required"]["guilded_api"]
		virustotal_api += configs["apis"]["optional"]["virustotal_api"]
		google_safe_browsing_api += configs["apis"]["optional"]["google_safe_browsing_api"]
		prefix += configs["bot-config"]["prefix"]
		prefix_count = len(prefix)
		if guilded_api in ["", " "]:
			exit('"guilded_token" parameter from "configs.json" cannot be empty. Please enter you bot API/Token first!')
		main()
	else:
		with open("configs.json", "w") as cw:
			content = {
				"apis": {"required": {"guilded_api": ""}, "optional": {"virustotal_api": "", "google_safe_browsing_api": ""}},
				"bot-config": {"prefix": "/"}, "blacklist": {"id": {"method": "", "name": "", "when": "", "reason": ""}},
				"entertainments": {"8-ball": [""], "conversation_starter": [""], "jokes": [""]}, "others": {"status-code": {
					"100": "Response 100 - Continue [Information Response]\n - This interim response indicates that everything so far is OK and that the client should continue the request, or ignore the response if the request is already finished.",
					"101": "Response 101 - Switching Protocol [Information Response]\n - This code is sent in response to an Upgrade request header from the client, and indicates the protocol the server is switching to.",
					"102": "Response 102 - Processing (WebDAV) [Information Response]\n - This code indicates that the server has received and is processing the request, but no response is available yet.",
					"103": "Response 103 - Early Hints [Information Response]\n - This status code is primarily intended to be used with the Link header, letting the user agent start preloading resources while the server prepares a response.",
					"200": "Response 200 - OK [Successful Response]\n - The request has succeeded. The meaning of the success depends on the HTTP method:\n\n > GET: The resource has been fetched and is transmitted in the message body.\n > HEAD: The representation headers are included in the response without any message body.\n > PUT or POST: The resource describing the result of the action is transmitted in the message body.\n > TRACE: The message body contains the request message as received by the server.",
					"201": "Response 201 - Created [Successful Response]\n - The request has succeeded and a new resource has been created as a result. This is typically the response sent after POST requests, or some PUT requests.",
					"202": "Response 202 - Accepted [Successful Response]\n - The request has been received but not yet acted upon. It is noncommittal, since there is no way in HTTP to later send an asynchronous response indicating the outcome of the request. It is intended for cases where another process or server handles the request, or for batch processing.",
					"203": "Response 203 - Non Authoritative Information [Successful Response]\n - This response code means the returned meta information is not exactly the same as is available from the origin server, but is collected from a local or a third party copy. This is mostly used for mirrors or backups of another resource. Except for that specific case, the '200 OK' response is preferred to this status.",
					"204": "Response 204 - No Content [Successful Response]\n - There is no content to send for this request, but the headers may be useful. The useragent may update its cached headers for this resource with the new ones.",
					"205": "Response 205 - Reset Content [Successful Response]\n - Tells the useragent to reset the document which sent this request.",
					"206": "Response 206 - Partial Content [Successful Response]\n - This response code is used when the Range header is sent from the client to request only part of a resource.",
					"207": "Response 207 - Multi Status (WebDAV) [Successful Response]\n - Conveys information about multiple resources, for situations where multiple status codes might be appropriate.",
					"208": "Response 208 - Already Reported (WebDAV) [Successful Response]\n - Used inside a <dav:propstat> response element to avoid repeatedly enumerating the internal members of multiple bindings to the same collection.",
					"226": "Response 226 - IM Used (HTTP Delta encoding) [Successful Response]\n - The server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance manipulations applied to the current instance.",
					"300": "Response 300 - Multiple Choice [Redirection Message]\n - The request has more than one possible response. The useragent or user should choose one of them. (There is no standardized way of choosing one of the responses, but HTML links to the possibilities are recommended so the user can pick.)",
					"301": "Response 301 - Moved Permanently [Redirection Message]\n - The URL of the requested resource has been changed permanently. The new URL is given in the response.",
					"302": "Response 302 - Found [Redirection Message]\n - This response code means that the URI of requested resource has been changed temporarily. Further changes in the URI might be made in the future. Therefore, this same URI should be used by the client in future requests.",
					"303": "Response 303 - See Other [Redirection Message]\n - The server sent this response to direct the client to get the requested resource at another URI with a GET request.",
					"304": "Response 304 - Not Modified [Redirection Message]\n - This is used for caching purposes. It tells the client that the response has not been modified, so the client can continue to use the same cached version of the response.",
					"305": "Response 305 - Use Proxy [Redirection Message]\n - Defined in a previous version of the HTTP specification to indicate that a requested response must be accessed by a proxy. It has been deprecated due to security concerns regarding inband configuration of a proxy.",
					"306": "Response 306 - unused [Redirection Message]\n - This response code is no longer used; it is just reserved. It was used in a previous version of the HTTP/1.1 specification.",
					"307": "Response 307 - Temporary Redirect [Redirection Message]\n - The server sends this response to direct the client to get the requested resource at another URI with same method that was used in the prior request. This has the same semantics as the 302 Found HTTP response code, with the exception that the user agent must not change the HTTP method used: If a POST was used in the first request, a POST must be used in the second request.",
					"308": "Response 308 - Permanent Redirect [Redirection Message]\n - This means that the resource is now permanently located at another URI, specified by the Location: HTTP Response header. This has the same semantics as the 301 Moved Permanently HTTP response code, with the exception that the user agent must not change the HTTP method used: If a POST was used in the first request, a POST must be used in the second request.",
					"400": "Response 400 - Bad Request [Client Error Response]\n - The server could not understand the request due to invalid syntax.",
					"401": "Response 401 - Unauthorized [Client Error Response]\n - Although the HTTP standard specifies 'unauthorized', semantically this response means 'unauthenticated'. That is, the client must authenticate itself to get the requested response.",
					"402": "Response 402 - Payment Required [Client Error Response]\n - This response code is reserved for future use. The initial aim for creating this code was using it for digital payment systems, however this status code is used very rarely and no standard convention exists.",
					"403": "Response 403 - Forbidden [Client Error Response]\n - The client does not have access rights to the content; that is, it is unauthorized, so the server is refusing to give the requested resource. Unlike 401, the client's identity is known to the server.",
					"404": "Response 404 - Not Found [Client Error Response]\n - The server can not find the requested resource. In the browser, this means the URL is not recognized. In an API, this can also mean that the endpoint is valid but the resource itself does not exist. Servers may also send this response instead of 403 to hide the existence of a resource from an unauthorized client. This response code is probably the most famous one due to its frequent occurrence on the web.",
					"405": "Response 405 - Method Not Allowed [Client Error Response]\n - The request method is known by the server but is not supported by the target resource. For example, an API may forbid DELETE/ing a resource.",
					"406": "Response 406 - Not Acceptable [Client Error Response]\n - This response is sent when the web server, after performing server_driven content negotiation, doesn't find any content that conforms to the criteria given by the user agent.",
					"407": "Response 407 - Proxy Authentication Required [Client Error Response]\n - This is similar to 401 but authentication is needed to be done by a proxy.",
					"408": "Response 408 - Request Timeout [Client Error Response]\n - This response is sent on an idle connection by some servers, even without any previous request by the client. It means that the server would like to shut down this unused connection. This response is used much more since some browsers, like Chrome, Firefox 27+, or IE9, use HTTP preconnection mechanisms to speed up surfing. Also note that some servers merely shut down the connection without sending this message.",
					"409": "Response 409 - Conflict [Client Error Response]\n - This response is sent when a request conflicts with the current state of the server.",
					"410": "Response 410 - Gone [Client Error Response]\n - This response is sent when the requested content has been permanently deleted from server, with no forwarding address. Clients are expected to remove their caches and links to the resource. The HTTP specification intends this status code to be used for 'limited time, promotional services'. APIs should not feel compelled to indicate resources that have been deleted with this status code.",
					"411": "Response 411 - Length Required [Client Error Response]\n - Server rejected the request because the Content Length header field is not defined and the server requires it.",
					"412": "Response 412 - Precondition Failed [Client Error Response]\n - The client has indicated preconditions in its headers which the server does not meet.",
					"413": "Response 413 - Payload Too Large [Client Response Error]\n - Request entity is larger than limits defined by server; the server might close the connection or return an Retry After header field.",
					"414": "Response 414 - URI Too Long [Client Response Error]\n - The URI requested by the client is longer than the server is willing to interpret.",
					"415": "Response 415 - Unsupported Media Type [Client Error Response]\n - The media format of the requested data is not supported by the server, so the server is rejecting the request.",
					"416": "Response 416 - Range Not Satisfiable [Client Error Response]\n - The range specified by the Range header field in the request can't be fulfilled; it's possible that the range is outside the size of the target URI's data.",
					"417": "Response 417 - Expectation Failed [Client Response Error]\n - This response code means the expectation indicated by the Expect request header field can't be met by the server.",
					"418": "Response 418 - I'm a teapot [Client Error Response]\n - The server refuses the attempt to brew coffee with a teapot.",
					"421": "Response 421 - Misdirected Request [Client Error Response]\n - The request was directed at a server that is not able to produce a response. This can be sent by a server that is not configured to produce responses for the combination of scheme and authority that are included in the request URI.",
					"422": "Response 422 - Unprocessable Entity (WebDAV) [Client Error Response]\n - The request was well formed but was unable to be followed due to semantic errors.",
					"423": "Response 423 - Locked (WebDAV) [Client Error Response]\n - The resource that is being accessed is locked.",
					"424": "Response 424 - Failed Dependency (WebDAV) [Client Error Response]\n - The request failed due to failure of a previous request.",
					"425": "Response 425 - Too Early [Client Error Response]\n - Indicates that the server is unwilling to risk processing a request that might be replayed.",
					"426": "Response 426 - Upgrade Required [Client Error Response]\n - The server refuses to perform the request using the current protocol but might be willing to do so after the client upgrades to a different protocol. The server sends an Upgrade header in a 426 response to indicate the required protocol(s).",
					"428": "Response 428 - Precondition Required [Client Error Response]\n - The origin server requires the request to be conditional. This response is intended to prevent the 'lost update' problem, where a client GETs a resource's state, modifies it, and PUTs it back to the server, when meanwhile a third party has modified the state on the server, leading to a conflict.",
					"429": "Response 429 - Too Many Requests [Client Error Response]\\n - The user has sent too many requests in a given amount of time ('rate limiting').",
					"431": "Response 431 - Request Header Fields Too Large [Client Error Response]\n - The server is unwilling to process the request because its header fields are too large. The request may be resubmitted after reducing the size of the request header fields.",
					"451": "Response 451 - Unavailable For Legal Reasons [Client Response Error]\n - The useragent requested a resource that cannot legally be provided, such as a web page censored by a government.",
					"500": "Response 500 - Internal Server Error [Server Error Response]\n - The server has encountered a situation it doesn't know how to handle.",
					"501": "Response 501 - Not Implemented [Server Error Response]\n - The request method is not supported by the server and cannot be handled. The only methods that servers are required to support (and therefore that must not return this code) are GET and HEAD.",
					"502": "Response 502 - Bad Gateway [Server Error Response]\n - This error response means that the server, while working as a gateway to get a response needed to handle the request, got an invalid response.",
					"503": "Response 503 - Service Unavailable [Server Error Response]\n - The server is not ready to handle the request. Common causes are a server that is down for maintenance or that is overloaded. Note that together with this response, a user friendly page explaining the problem should be sent. This response should be used for temporary conditions and the Retry After: HTTP header should, if possible, contain the estimated time before the recovery of the service. The webmaster must also take care about the caching related headers that are sent along with this response, as these temporary condition responses should usually not be cached.",
					"504": "Response 504 - Gateway Timeout [Server Error Response]\n - This error response is given when the server is acting as a gateway and cannot get a response in time.",
					"505": "Response 505 - HTTP Version Not Supported [Server Error Response]\n - The HTTP version used in the request is not supported by the server.",
					"506": "Response 506 - Variant Also Negotiates [Server Error Response]\n - The server has an internal configuration error: the chosen variant resource is configured to engage in transparent content negotiation itself, and is therefore not a proper end point in the negotiation process.",
					"507": "Response 507 - Insufficient Storage (WebDAV) [Server Error Response]\n - The method could not be performed on the resource because the server is unable to store the representation needed to successfully complete the request.",
					"508": "Response 508 - Loop Detected (WebDAV) [Server Error Response]\n - The server detected an infinite loop while processing the request.",
					"510": "Response 510 - Not Extended [Server Error Response]\n - Further extensions to the request are required for the server to fulfill it.",
					"511": "Response 511 - Network Authentication Required [Server Error Response]\n - The 511 status code indicates that the client needs to authenticate to gain network access.",
					"invalid-code": "Invalid Code - The code given is invalid. - In some cases, a response code may come from a server that is not on the list of response codes. This means that the response code is possibly custom to the server's software and is not included on the list of response codes because it is a nonstandard response code.",
					"attribution": "Original Source Website Code Author: Mozilla Foundation (https://foundation.mozilla.org/en/)\nOriginal Source Website Code Link: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#information_responses\nLicense: https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt\n\nDisclaimer: This project is not in affiliation with the Mozilla Foundation."}}}
			cw.write(json.dumps(content, indent=2))
		exit(f'Please configure this bot first by opening "configs.json". Thank you {__file__.split(path_classifier)[1]}!')