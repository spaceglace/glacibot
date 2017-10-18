import importlib

def load(mod):
	return importlib.import_module(mod)

def refresh(mod):
	importlib.reload(mod)