from base64 import b64decode

data_uri = "data:image/png;base64,iVBORw0KGg..."

# Python 2 and <Python 3.4
header, encoded = data_uri.split("base64,", 1)
data = b64decode(encoded)
