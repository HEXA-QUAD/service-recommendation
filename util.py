import uuid

def generate_id(prefix):
    r = str(uuid.uuid4())
    r = prefix + "_" + r
    return r
