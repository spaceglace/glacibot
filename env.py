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
	'connected': 0,
	'reconnects': 0
}

ping = {
	'pending': False,
	'latency': [],
}

#pings = []
#pingID = 0

shutDown = False
