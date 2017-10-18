import asyncio, aiohttp, json
import env

async def listen():
	rtm = await api_call("rtm.start")
	assert rtm['ok'], "Error connecting to RTM."

	async with aiohttp.ClientSession() as session:
		async with session.ws_connect(rtm["url"]) as ws:
			async for msg in ws:
				assert msg.tp == aiohttp.WSMsgType.TEXT

				current = json.loads(msg.data)

				for command in env.commands:
					await env.commands[command].parse(current)

async def api_call(method, data=None, token=env.TOKEN):
	with aiohttp.ClientSession() as session:
		form = aiohttp.FormData(data or {})
		form.add_field('token', token)

		async with session.post('https://slack.com/api/{0}'.format(method), data=form) as response:
			assert 200 == response.status, ('{0} with {1} failed.'.format(method, data))
			return await response.json()

async def say(channel, message):
	await api_call("chat.postMessage", {'channel': channel, 'text': message, 'as_user': True})