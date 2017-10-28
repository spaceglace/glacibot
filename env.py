from config import *

# Utility modules
module = None
slack = None
admin = None
mysql = None
logger = None

commands = {}
admins = []

# Life statistics
stats = {
	'pingSent': 0,
	'pingRecv': 0,
	'pingHang': 0,
	'latency': 0,
	'birth' : 0,
	'connected': 0,
	'reconnects': 0
}
shutDown = False