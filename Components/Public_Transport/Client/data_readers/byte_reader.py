import struct

def read_bytes(file, offset, length):
    file.seek(offset)
    return file.read(length)

def move_cursor(file, offset):
    file.seek(offset)

def read_next_bytes(file, length):
    return file.read(length)

def read_int(file, offset, length):
    raw_bytes = read_bytes(file, offset, length)
    if length == 1:
        return struct.unpack('<b', raw_bytes)[0]
    elif length == 2:
        return struct.unpack('<h', raw_bytes)[0]
    elif length == 4:
        return struct.unpack('<i', raw_bytes)[0]
    else:
        raise ValueError("Unsupported integer byte length")
    
def read_next_int(file, length):
    raw_bytes = read_next_bytes(file, length)
    if length == 1:
        return struct.unpack('<b', raw_bytes)[0]
    elif length == 2:
        return struct.unpack('<h', raw_bytes)[0]
    elif length == 4:
        return struct.unpack('<i', raw_bytes)[0]
    else:
        raise ValueError("Unsupported integer byte length")
    
def read_string(file, offset, length):
    raw_bytes = read_bytes(file, offset, length)
    return raw_bytes.decode('utf-8').rstrip('\x00')

def read_next_string(file, length):
    raw_bytes = read_next_bytes(file, length)
    return raw_bytes.decode('utf-8').rstrip('\x00')