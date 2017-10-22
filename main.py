import os, asyncio
import env

# Bootstrap the module loader into the environment
import utils.module
env.module = utils.module.load('utils.module')
del utils.module

# Load the rest of the custom utilities
env.slack = env.module.load('utils.slack')
env.admin = env.module.load('utils.admin')
env.mysql = env.module.load('utils.mysql')
env.mysql.create()

# Load all of the custom commands
for name in os.listdir('./commands/'):
	if os.path.isdir('./commands/{0}'.format(name)):
		try:
			env.commands[name] = env.module.load('commands.{0}.main'.format(name))
			print("Loaded {0} command set".format(name))
		except:
			error, tb = sys.exc_info()[1:]
			filename = tb.tb_frame_f_code.co_filename

			print("Error in {0}.{1}: {2}".format(item, filename, error))

loop = asyncio.get_event_loop()
loop.run_until_complete(env.slack.listen())
loop.close()