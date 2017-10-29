import asyncio, aiohttp, websockets, json, time
import env

async def ping(destination, interval):
	print("ping: Ping slave is born.")

	while True:
		#print("ping: sleeping for {0} to ping".format(interval))
		await asyncio.sleep(interval)

		# Assume the connection broke if there's still a ping waiting
		if env.ping['pending']:
			break

		env.ping['pending'] = True

		#print("ping: woke up to send ping... ({0}s)".format(interval))
		await destination(json.dumps({"type": "ping", "sent": time.time()}))

	print("ping: Ping slave dies.")

async def parse(receive):
	print("parse: Parse slave is born.")

	while True:
		# wait for a message to come in
		message = await receive()

		if message is None:
			break

		message = json.loads(message)
		#print("parse: {0}".format(message))

		# did we get a ping reply?
		if message['type'] == 'pong':
			env.ping['pending'] = False
			env.ping['latency'].append(time.time() - float(message['sent']))

			if len(env.ping['latency']) > 20:
				env.ping['latency'].pop(0)

		else:
			for command in env.commands:
				await env.commands[command].parse(message)

	print("parse: Parse slave dies.")

async def listen():
	reconnections = 0
	max_delay = 30

	while env.shutDown == False:
		try:
			# ask slack for a connection link
			rtm = await api_call("rtm.start")
			assert rtm['ok'], "Error connecting to RTM."

			# if we get here, assume a good connection
			print("listen: Listener is alive.")
			env.stats['connected'] = time.time()
			env.stats['pingHang'] = 0
			reconnections = 0

			async with websockets.connect(rtm["url"]) as ws:
				# spin up the ping and websocket tasks
				pingTask = asyncio.ensure_future(ping(ws.send, 15))
				parseTask = asyncio.ensure_future(parse(ws.recv))

				print("listen: Red October, standing by...")

				# wait until either of them finish/error out
				done, pending = await asyncio.wait([pingTask, parseTask], return_when=asyncio.FIRST_COMPLETED)

				print("listen: Something broke")
				print("listen: piT: {0}".format(pingTask))
				print("listen: paT: {0}".format(parseTask))

				# set both of them to cancel
				pingTask.cancel()
				parseTask.cancel()

				# wait for them to have cycles to process the cancel
				print("listen: Letting things settle...")
				await asyncio.sleep(0.5)
				ws.close()

		except Exception as e:
			print("listen: Fell from heaven: {0}".format(e))

		# did we mean to fall down here?
		if env.shutDown == False:
			# record the lost connection, and delay trying to reconnect
			reconnections += 1
			temp = min(reconnections * 5, max_delay)
			print("listen: disconnected from server (try {0}). Retry in {1} seconds".format(reconnections, temp))
			await asyncio.sleep(temp)

	print("listen: All is finished.")

# MAIN ENTRY POINT
def connect():
	print("connect: Entered connect.")

	loop = asyncio.get_event_loop()
	loop.set_debug(True)
	loop.run_until_complete(listen())
	loop.close()

	print("connect: Loop is closed, all is quiet.")

async def api_call(method, data=None, token=env.TOKEN):
	#print("api: Starting api call...")

	with aiohttp.ClientSession() as session:
		# add our authentication token to the request
		form = aiohttp.FormData(data or {})
		form.add_field('token', token)

		while True:
			# send slack the request
			async with session.post('https://slack.com/api/{0}'.format(method), data=form) as response:
				# did it succeed?
				if response.status == 200:
					#print("api: Got good api response.")
					return await response.json()

				# are we getting rate limited?
				elif response.status == 429:
					print("api: Received 'Too Many Requests' warning from Slack, sleeping for a bit...")
					await asyncio.sleep(5)

				# did something weird happen?
				else:
					print("api: Unknown api response: {0}".format(response.status))
					raise

async def say(channel, message):
	await api_call("chat.postMessage", {'channel': channel, 'text': message, 'as_user': True})
