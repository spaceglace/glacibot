import re, asyncio, time
import env

phrase = re.compile(r'^<@U7J9S9C5S>\s+stats', re.I)

def prettyTime(delta):
	delta = int(delta)
	minutes, seconds = divmod(delta, 60)
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

	return " ".join(timestring)

async def parse(message):
	if message['type'] != 'message' or 'subtype' in message:
		return

	match = phrase.match(message['text'])

	if match:
		current = time.time()
		output = "I've been alive for {0}".format(prettyTime(current - env.stats['born']))

		# does the birth time differ too much from the connection time?
		if abs(env.stats['born'] - env.stats['connected']) > 15:
			output += " (and connected for {0})".format(prettyTime(current - env.stats['connected']))

		output += "\n"

		# have we gotten a ping to determine latency?
		if len(env.ping['latency']) > 0:
			output += "Current latency {0}s, 2 minute average {1}s, 5 minute average {2}s".format(
				round(env.ping['latency'][-1], 3),
				round(sum(env.ping['latency'][-7:]) / min(len(env.ping['latency']), 8), 3),
				round(sum(env.ping['latency']) / min(len(env.ping['latency']), 20), 3))

		await env.slack.say(message['channel'], output)
