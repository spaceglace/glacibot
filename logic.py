logic = {}
handle = lambda f: logic.setdefault(f.__name__, f)

def parse(branch, message):
	if branch in logic:
		logic[branch](message)
	else:
		print("*** Unrecognized type: {0} ***".format(branch))


@handle
def hello(message):
	print("~ received hello")

@handle
def reconnect_url(message):
	"""	From the Slack API: 'The reconnect_url event is currently unsupported and experimental.' """
	return

@handle
def message(message):
	isThread = 'thread_ts' in message

	if isThread:
		print("(thread) {0}".format(message['text']))
	else:
		print(message['text'])

@handle
def message_replied(message):
	print("~ received message replied message.")

@handle
def message_changed(message):
	print("~ received message_changed message.")

@handle
def message_deleted(message):
	print("~ received message_deleted message.")