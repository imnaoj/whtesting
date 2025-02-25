from bson import ObjectId

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
ALPHABET_DICT = {char: index for index, char in enumerate(ALPHABET)}

def encode_base62(num):
    """Encode a number in Base62"""
    if num == 0:
        return ALPHABET[0]
    
    arr = []
    base = len(ALPHABET)
    while num:
        num, rem = divmod(num, base)
        arr.append(ALPHABET[rem])
    arr.reverse()
    return ''.join(arr)

def decode_base62(string):
    """Decode a Base62 string to number"""
    num = 0
    base = len(ALPHABET)
    for char in string:
        num = num * base + ALPHABET_DICT[char]
    return num

def objectid_to_base62(object_id):
    """Convert MongoDB ObjectId to Base62 string"""
    # Convert ObjectId to integer using its timestamp + machine + pid + counter
    num = int(str(object_id), 16)
    return encode_base62(num)

def base62_to_objectid(base62_str):
    """Convert Base62 string back to MongoDB ObjectId
    
    Args:
        base62_str (str): The Base62 encoded string
        
    Returns:
        ObjectId: MongoDB ObjectId
        
    Raises:
        ValueError: If the input string is invalid Base62 or can't be converted to ObjectId
    """
    try:
        # Decode base62 string to number
        num = decode_base62(base62_str)
        # Convert number to hexadecimal string
        hex_str = hex(num)[2:].rjust(24, '0')
        # Create ObjectId from hex string
        return ObjectId(hex_str)
    except (ValueError, KeyError) as e:
        raise ValueError(f"Invalid Base62 string or cannot convert to ObjectId: {e}")

def is_valid_base62(string):
    """Check if a string is valid Base62
    
    Args:
        string (str): String to validate
        
    Returns:
        bool: True if string is valid Base62, False otherwise
    """
    return all(char in ALPHABET_DICT for char in string) 