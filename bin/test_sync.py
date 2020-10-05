"""Test sync file
"""
from sync import *

__author__ = "help@castellanidavide.it"
__version__ = "1.0 2020-10-5"

def test():
	"""Tests the sync function in the sync class
	Write here all test you want to do.
	REMEMBER to test your programm you can't use __init__ function
	"""
	assert sync.sync() == "sync", "test failed"
	#assert sync.<function>(<values>) == <the result(s) you would like to have>, "<the fail message>"
	
if __name__ == "__main__":
	test()
