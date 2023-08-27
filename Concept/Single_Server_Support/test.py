"""available_commands = {
	"help": ["h", "he", "hel"],
	"ping": ["p", "pi", "pin"],
	"a": "bcdefg"
	}

result = []

for key, value in available_commands.items():
	result.append(key)
	result.extend(value)

print(result)

lists = ["qwe", "rTy", "uio"]
print(str(lists[1:]).lower())
c = 2
print(lists[0][c:])

print(f"\n\n\n{len('qwe')}")"""

"""message_content = "/help this is a message content."
list_content = message_content.lower().split(" ")
hint = list_content[4][:-1]

print(message_content)
print(list_content)
print(hint)"""
"""
import random

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


print(random_all())
print(random_light())
print(random_dark())
"""

t = {
	"sample": [1,2,3,4]
}

if 1 in t["sample"]:
	print("Ok")