import re
import env

phrase = re.compile(r'^<@U7J9S9C5S>\s+quote\s+(?P<type>[^ ]+)\s+(?P<target>[^ ]+)\s+(?P<quote>.+)*$', re.I)

async def parse(message):
	if message['type'] != 'message' or 'subtype' in message:
		return

	match = phrase.match(message['text'])

	if match:
		if match.group('type') in ("add", "new"):
			# Add a new quote to the database
			await env.slack.say(message['channel'], "no")

		elif match.group('type') in ("show", "say", "give", "random"):
			# Pick a random quote and say it to the channel
			output = "＃5273 (30077) by Bash\n><erno> hm. I've lost a machine.. literally _lost_. it responds to ping, it works completely, I just can't figure out where in my apartment it is."
			await env.slack.say(message['channel'], output)

		#elif match.group('type') in ("del", "delete", "remove"):
			# Remove a quote?