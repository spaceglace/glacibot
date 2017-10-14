import asyncio, json, sys, aiohttp
import logic
from config import DEBUG, TOKEN

async def api_call(method, data=None, token=TOKEN):
	"""Slack API call."""
	with aiohttp.ClientSession() as session:
		form = aiohttp.FormData(data or {})
		form.add_field('token', token)

		async with session.post('https://slack.com/api/{0}'.format(method), data=form) as response:
			assert 200 == response.status, ('{0} with {1} failed.'.format(method, data))
			return await response.json()

async def bot(token=TOKEN):
	"""Create a bot that joins Slack."""
	rtm = await api_call("rtm.start")
	assert rtm['ok'], "Error connecting to RTM."

	async with aiohttp.ClientSession() as session:
		async with session.ws_connect(rtm["url"]) as ws:
			async for msg in ws:
				assert msg.tp == aiohttp.WSMsgType.TEXT

				message = json.loads(msg.data)
				print(message)

				if message['type'] == "hello":
					logic.handleHello(message)

				elif message['type'] == "reconnect_url":
					logic.handleReconnectURL(message)

				# Ignore any non-messages for now
				if 'type' not in message or message['type'] != "message":
					continue

				# Ignore any 'replied to a thread' announcements
				if 'subtype' in message and message['subtype'] == "message_replied":
					continue

				isThread = 'thread_ts' in message

				if message['type'] == "message":
					if message['text'].startswith("<@U7J9S9C5S>"):
						payload = {
							'text' : ":glaceon-thinking:",
							'channel' : message["channel"],
							'as_user' : True
						}

						if isThread:
							payload['thread_ts'] = message['thread_ts']

						result = await api_call("chat.postMessage", payload)
						print("SENDING MESSAGE: {}".format(result))

					elif message['text'] == "hello":
						payload = {}
						payload['text'] = "hihi"
						payload['channel'] = message['channel']
						payload['as_user'] = True

						if isThread:
							payload['thread_ts'] = message['thread_ts']

						result = await api_call("chat.postMessage", payload)
						print("SENDING MESSAGE: {}".format(result))

					elif message['text'] == "quit":
						return 0

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.set_debug(DEBUG)
	loop.run_until_complete(bot())
	loop.close()