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
	'born': 0,
	'connected': 0
}

connection = {
	'max delay': 30,
	'delay step': 5,
	'reconnects': 0
}

ping = {
	'pending': False,
	'latency': [],
}

#pings = []
#pingID = 0

shutDown = False
