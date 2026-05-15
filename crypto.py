import base64
import hashlib
from nacl.public import PrivateKey, PublicKey, Box

# ================= KEYS =================
def generate_keys():
    priv = PrivateKey.generate()
    return priv, priv.public_key

# ================= ENCRYPT =================
def encrypt(message, sender_private, receiver_public):
    box = Box(sender_private, receiver_public)
    encrypted = box.encrypt(message.encode())
    return base64.b64encode(encrypted).decode()

# ================= DECRYPT =================
def decrypt(message, receiver_private, sender_public):
    box = Box(receiver_private, sender_public)
    decrypted = box.decrypt(base64.b64decode(message))
    return decrypted.decode()

# ================= FINGERPRINT =================
def fingerprint(public_key_hex):
    h = hashlib.sha256(public_key_hex.encode()).hexdigest()

    # більш стандартний формат (повніший fingerprint)
    return ":".join(h[i:i+2] for i in range(0, 32, 2))
