from datetime import datetime

def get_tz_delta():
    return datetime.now() - datetime.utcnow()
