import asyncio, json, sys, aiohttp
import slack, logic, mysql
from config import DEBUG, SQLPASS

async def bot():
	"""Create a bot that joins Slack."""

	rtm = await slack.api_call("rtm.start")
	assert rtm['ok'], "Error connecting to RTM."

	async with aiohttp.ClientSession() as session:
		async with session.ws_connect(rtm["url"]) as ws:
			async for msg in ws:
				assert msg.tp == aiohttp.WSMsgType.TEXT

				message = json.loads(msg.data)

				if message['type'] == "message" and 'subtype' in message:
					await logic.parse(message['subtype'], message)
				else:
					await logic.parse(message['type'], message)


if __name__ == "__main__":
	# connect to the database
	mysql.connect('glacibot', SQLPASS, 'glacibot')

	loop = asyncio.get_event_loop()
	loop.set_debug(DEBUG)
	loop.run_until_complete(bot())
	loop.close()

	# disconnect from the database
	mysql.disconnect()