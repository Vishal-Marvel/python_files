import json, base64

file = open("test", "w")
base = base64.b64encode(b"Hello")
file.write(str(base))
file.close()

	