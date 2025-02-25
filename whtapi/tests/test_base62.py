import pytest
from bson import ObjectId
from app.utils.base62 import (
    encode_base62, 
    decode_base62, 
    objectid_to_base62, 
    base62_to_objectid,
    is_valid_base62
)

def test_base62_encoding_decoding():
    # Test basic encoding/decoding
    number = 12345
    encoded = encode_base62(number)
    decoded = decode_base62(encoded)
    assert decoded == number

def test_objectid_conversion():
    # Test ObjectId conversion
    original_id = ObjectId()
    base62_str = objectid_to_base62(original_id)
    recovered_id = base62_to_objectid(base62_str)
    assert original_id == recovered_id

def test_valid_base62():
    # Test valid Base62 strings
    assert is_valid_base62("ABC123xyz")
    assert is_valid_base62("0123456789")
    assert not is_valid_base62("ABC_123")  # underscore is not valid
    assert not is_valid_base62("ABC 123")  # space is not valid

def test_invalid_base62_conversion():
    # Test invalid Base62 string
    with pytest.raises(ValueError):
        base62_to_objectid("invalid_base62") 

# Converting ObjectId to Base62
object_id = ObjectId()
base62_str = objectid_to_base62(object_id)
print(f"Base62: {base62_str}")

# Converting Base62 back to ObjectId
try:
    recovered_id = base62_to_objectid(base62_str)
    print(f"Recovered ObjectId: {recovered_id}")
except ValueError as e:
    print(f"Error: {e}")
