import re, asyncio
import env

phrase = re.compile(r'^<@U7J9S9C5S>\s+mod\s+(?P<payload>.+)$', re.I)

async def error(channel, error):
	await env.slack.say(channel, error)

async def parse(message):
	if message['type'] != 'message' or 'subtype' in message:
		return

	match = phrase.match(message['text'])
	
	if match:
		payload = match.group('payload').split()
		action = payload[0]
		caller = "<@{0}>".format(message['user'])
		channel = message['channel']

		if not env.mysql.isAlive():
			await error(channel, "I can't connect to my database right now, no mod commands will work until I can, sorry!")
			return

		elif action in ("new", "add"):
			await addMod(caller, channel, payload)
			return

		elif action in ("delete", "del", "remove"):
			await removeMod(caller, channel, payload)
			return

		elif action in ("update", "change"):
			await updateMod(caller, channel, payload)
			return

		elif action in ("list", "show"):
			await listMod(caller, channel)
			return

		elif action in ("help", "info", "man"):
			await helpMod(caller, channel)
			return

		else:
			await error(channel, "Unrecognized mod action. Try `mod help` for a list!")
			return

async def addMod(caller, channel, payload):
	# Make sure all variables are there
	if len(payload) != 3:
		await error(channel, "Expected format is `mod add <user> <power>`.")
		return

	targetName, targetPriv = payload[1:3]

	# Make sure the desired privilege is numeric
	if not targetPriv.isdigit():
		await error(channel, "You need to assign a positive whole number as a power level.")
		return

	targetPriv = int(targetPriv)

	# Make sure it isn't 0
	if targetPriv < 1:
		await error(channel, "You cannot assign a power level of 0. You might be looking for `mod remove <user>`.")
		return

	if caller not in env.admins:
		# Check the database for the caller's mod power
		resultUser = env.mysql.execute("SELECT `power` FROM `moderators` WHERE `name` = {0} LIMIT 1;".format(env.mysql.escape(caller)))

		# Make sure we found them in the mod database
		if len(resultUser) == 0:
			await error(channel, "You need to be a moderator in order to add moderators.")
			return

		userPriv = resultUser[0]['power']

		if userPriv < targetPriv:
			await error(channel, "You can't assign a higher power level than you currently have.")
			return

	# Is the target already an admin?
	if targetName in env.admins:
		await error(channel, "You don't need to assign moderators to an admin.")
		return

	# Is the target already a mod?
	resultTarget = env.mysql.execute("SELECT `power` FROM `moderators` WHERE `name` = {0} LIMIT 1;".format(env.mysql.escape(targetName)))

	if len(resultTarget) > 0:
		await error(channel, "{0} is already in the mod database. You might be looking for `mod update <user> <power>`.".format(targetName))
		return

	env.mysql.execute("INSERT INTO `moderators` (`name`, `power`) VALUES ({0}, {1});".format(env.mysql.escape(targetName), targetPriv))
	env.mysql.commit()

	await env.slack.say(channel, "{0} has been added to the moderator list with a power of {1}!".format(targetName, targetPriv))
	return

async def removeMod(caller, channel, payload):
	# Make sure all variables are there
	if len(payload) != 2:
		await error(channel, "Expected format is `mod remove <user>`.")
		return

	targetName = payload[1]

	if caller not in env.admins:
		# Check the database for the caller's mod power
		resultUser = env.mysql.execute("SELECT `power` FROM `moderators` WHERE `name` = {0} LIMIT 1;".format(env.mysql.escape(caller)))

		# Make sure we found them in the mod database
		if len(resultUser) == 0:
			await error(channel, "You need to be a moderator in order to remove moderators.")
			return

		userPriv = resultUser[0]['power']

	# Is the target already an admin?
	if targetName in env.admins:
		await error(channel, "You can't remove admins.")
		return

	# Make sure the target is currently a mod
	resultTarget = env.mysql.execute("SELECT `power` FROM `moderators` WHERE `name` = {0} LIMIT 1;".format(env.mysql.escape(targetName)))

	if len(resultTarget) == 0:
		await error(channel, "I couldn't find {0} in the mod database.".format(targetName))
		return

	targetPriv = resultTarget[0]['power']

	# Make sure the caller has sufficient privilege
	if caller not in env.admins and userPriv <= targetPriv:
		await error(channel, "You can't remove moderators of a higher or equal power level.")
		return

	env.mysql.execute("DELETE FROM `moderators` WHERE `name` = {0};".format(env.mysql.escape(targetName)))
	env.mysql.commit()

	await env.slack.say(channel, "I've removed {0} from the mod database.".format(targetName))
	return

async def updateMod(caller, channel, payload):
	await env.slack.say(channel, "Coming Soon (tm)")
	return

async def listMod(caller, channel):
	await env.slack.say(channel, "Coming Soon (tm)")
	return

async def helpMod(caller, channel):
	await env.slack.say(channel, "Coming Soon (tm)")
	return
