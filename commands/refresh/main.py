import re
import env

phrase = re.compile(r'^<@U7J9S9C5S>\s+(?:reload|refresh)\s+(?P<module>[^ ]+)', re.I)
requiredPower = 50

async def error(message, error):
	await env.slack.say(message['channel'], error)

async def parse(message):
	if message['type'] != 'message' or 'subtype' in message:
		return

	match = phrase.match(message['text'])

	if match:
		caller = "<@{0}>".format(message['user'])
		priv = 0

		if caller not in env.admins:
			if env.mysql.isAlive():
				# Check the database for the user if they're not an admin
				result = env.mysql.execute("SELECT `power` FROM `moderators` WHERE `name` = {0} LIMIT 1;".format(caller))

				if len(result) > 0:
					priv = resultUser[0]['power']

					if priv < requiredPower:
						await error(message, "You need a power level of at least {0} to run this.".format(requiredPower))
						return

				else:
					await error(message, "You have to be a moderator to run this.")
					return

		# asert
		if caller not in env.admins and priv < requiredPower:
			await error(message, "Something doesn't add up here, sorry! [a={0}, p={1}, r={2}]".format(caller in env.admins, priv, requiredPower))
			return

		if match.group('module') == "mysql":
			env.mysql.destroy()
			env.module.refresh(env.mysql)
			env.mysql.create()
			await env.slack.say(message['channel'], "Refreshed mysql utility.")

		elif match.group('module') == "admin":
			env.module.refresh(env.admin)
			await env.slack.say(message['channel'], "Refreshed admin utility.")

		elif match.group('module') in env.commands:
			env.module.refresh(env.commands[match.group('module')])
			await env.slack.say(message['channel'], "Refreshed {0} command.".format(match.group('module')))