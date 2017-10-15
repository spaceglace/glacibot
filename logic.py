import asyncio
import mysql, slack
from config import DEBUG

async def parse(branch, message):
	if branch in behavior:
		await behavior[branch](message)
	else:
		print("*** Unrecognized type: {0} ***".format(branch))


async def hello(message):
	print("~ received hello")

async def reconnect(message):
	"""	From the Slack API: 'The reconnect_url event is currently unsupported and experimental.' """
	return

async def message(message):
	isThread = 'thread_ts' in message

	if isThread:
		print("(thread) {0}".format(message['text']))
	else:
		print(message['text'])

	pieces = message['text'].split()

	if pieces[0] == "find":
		result = mysql.execute("SELECT `name`, `value` FROM `test` WHERE `name` = \"{0}\" LIMIT 1;".format(pieces[1]))

		if len(result) > 0:
			row = result[0]
			output = "{0} has a value of {1}".format(row[0], row[1])
		else:
			output = "Couldn't find {0} in the database.".format(pieces[1])

		await slack.api_call("chat.postMessage", {'channel': message['channel'], 'text': output, 'as_user': True})

async def replied(message):
	print("~ received message replied message.")

async def changed(message):
	print("~ received message_changed message.")

async def deleted(message):
	print("~ received message_deleted message.")


# map message types to behaviors
behavior = {
	'hello': hello,
	'reconnect_url': reconnect,
	'message': message,
	'message_replied': replied,
	'message_changed': changed,
	'message_deleted': deleted
}