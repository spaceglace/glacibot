import asyncio, json, sys, aiohttp
from config import DEBUG, TOKEN

async def api_call(method, data=None, token=TOKEN):
	"""Slack API call."""
	with aiohttp.ClientSession() as session:
		form = aiohttp.FormData(data or {})
		form.add_field('token', token)

		async with session.post('https://slack.com/api/{0}'.format(method), data=form) as response:
			assert 200 == response.status, ('{0} with {1} failed.'.format(method, data))
			return await response.json()

async def postMessage(channel, message):
	return await api_call("chat.postMessage", {'channel' : channel, 'text' : message, 'as_user': True})

async def bot(token=TOKEN):
	"""Create a bot that joins Slack."""
	rtm = await api_call("rtm.start")
	assert rtm['ok'], "Error connecting to RTM."

	async with aiohttp.ClientSession() as session:
		async with session.ws_connect(rtm["url"]) as ws:
			async for msg in ws:
				assert msg.tp == aiohttp.MsgType.text

				x = json.loads(msg.data)
				print(x)

				if x['type'] == "message":
					if x['text'] == "hello":
						print("!!! SENDING MESSAGE !!!")
						result = await postMessage(x['channel'], "hihi")
						print(result)
						print("!!! DONE SENDING MESSAGE !!!")
					elif x['text'] == "quit":
						return 0

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.set_debug(DEBUG)
	loop.run_until_complete(bot())
	loop.close()