import re, asyncio
import env

phrase = re.compile(r'^<@U7J9S9C5S>\s+(?P<greeting>hello|hihi|heyo|hiya|hi)', re.I)

async def parse(message):
	if message['type'] != 'message' or 'subtype' in message:
		return

	match = phrase.match(message['text'])

	if match:
		output = "{0}, <@{1}> !!!".format(match.group('greeting'), message['user'])
		await env.slack.say(message['channel'], output)