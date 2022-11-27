import base64


def base64_decode(val, field):
    data = val[field]
    return base64.b64decode(data).decode('utf')
