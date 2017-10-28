import re, asyncio, time
import env

phrase = re.compile(r'^<@U7J9S9C5S>\s+stats', re.I)

async def parse(message):
	if message['type'] != 'message' or 'subtype' in message:
		return

	match = phrase.match(message['text'])

	if match:
		seconds = int(time.time() - env.stats['connected'])
		minutes, seconds = divmod(seconds, 60)
		hours, minutes = divmod(minutes, 60)
		days, hours = divmod(hours, 24)

		timestring = []
		drop = False
		if days > 0:
			timestring.append("{0}d".format(days))
			drop = True
		if hours > 0 or drop:
			timestring.append("{0}h".format(hours))
			drop = True
		if minutes > 0 or drop:
			timestring.append("{0}m".format(minutes))
		timestring.append("{0}s".format(seconds))

		# 2d 0h 9m 14s

		output = "I've been alive for {0}\n".format(" ".join(timestring))
		output += "{1} out of {0} heartbeat pings received.".format(env.stats['pingSent'], env.stats['pingRecv'])

		await env.slack.say(message['channel'], output)