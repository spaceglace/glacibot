import os, asyncio
import env

# Bootstrap the module loader into the environment
import utils.module
env.module = utils.module.load('utils.module')
del utils.module

# Load the rest of the custom utilities
env.slack = env.module.load('utils.slack')
env.mysql = env.module.load('utils.mysql')

# Load all of the custom commands
commands = os.listdir('./commands/')
for file in commands:
	if file.endswith('.py'):
		name = file.split('.')[0]
		env.commands[name] = env.module.load('commands.{0}'.format(name))
		print("Loaded {0} command set".format(name))

loop = asyncio.get_event_loop()
loop.run_until_complete(env.slack.listen())
loop.close()