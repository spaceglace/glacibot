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

		# I've been alive for 2d 0h 9m 14s
		# Current Latency: 0.229s, Average Latency: 1.000s
		# Latency: 0.011s min, 1.010s max, 0.229s avg
		# Average latency of 0.038s, connection score of 377
		# onnection score: 377
		# Current Latency: 0.229s, 2 minute average 0.339s, 5 minute average 1.330s

		#status = 0
		#latencies = []

		#for entry in env.pings:
		#	status <<= 1

		#	if entry['reply']:
		#		status += 1
		#		latencies.append(entry['received'] - entry['sent'])



		output = "I've been alive for {0}\n".format(" ".join(timestring))

		if len(env.ping['latency']) > 0:
			output += "Current latency {0}s, 2 minute average {1}s, 5 minute average {2}s".format(
				round(env.ping['latency'][-1], 3),
				round(sum(env.ping['latency'][-7:]) / min(len(env.ping['latency']), 8), 3),
				round(sum(env.ping['latency']) / min(len(env.ping['latency']), 20), 3))
#			output += "Latency: {0}s min, {1}s max, {2}s avg\n".format(
#				round(min(latencies), 3), 
#				round(max(latencies), 3),
#				round(sum(latencies) / len(latencies), 3))
#			output += "Connection stability score is currently {0}".format(
#				oct(status)[2:])
#			output += "verage latency of {0}, connection score of {1}".format(
#				round(sum(latencies) / len(latencies), 3),
#				oct(status)[2:])

		await env.slack.say(message['channel'], output)
		