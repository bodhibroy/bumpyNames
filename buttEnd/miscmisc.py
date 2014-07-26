import hashlib
import os

def file_sha1hash(path):
	try:
		filesize = os.path.getsize(path)
		data = open(path).read()
		return hashlib.sha1("icon " + str(filesize) + "\0" + data).hexdigest()
	except Exception as e:
		return None