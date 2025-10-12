import base64



def _encrypt_string(string: str):
    s = bytes(string, 'utf-8')
    s = base64.b64encode(s)
    return s

def _decrypt_string(string):
    try:
        s = base64.b64decode(string)
        s = s.decode()
        return s
    except:
        return string