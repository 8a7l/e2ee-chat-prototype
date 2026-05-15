import asyncio
import json
import threading
import websockets

from nacl.public import PublicKey
from crypto import generate_keys, encrypt, decrypt, fingerprint

USERNAME = input("Your ID: ")

private_key, public_key = generate_keys()
public_key_hex = public_key.encode().hex()

known_keys = {}
known_fingerprints = {}
key_events = {}

ws_global = None
loop = None
running = True

# ================= FINGERPRINT =================
def check_fingerprint(user, pubkey_hex):

    fp = fingerprint(pubkey_hex)

    if user not in known_fingerprints:
        known_fingerprints[user] = fp
        print(f"\n🔐 Fingerprint saved for {user}: {fp}")
        return

    if known_fingerprints[user] != fp:
        print(f"\n⚠️ Fingerprint changed for {user}")
        print(f"OLD: {known_fingerprints[user]}")
        print(f"NEW: {fp}")
        known_fingerprints[user] = fp

# ================= SEND WRAPPER =================
async def send(msg):
    if ws_global:
        await ws_global.send(json.dumps(msg))

# ================= REQUEST KEY =================
async def request_key(user):

    key_events[user] = asyncio.Event()

    await send({
        "type": "get_key",
        "user": user
    })

    try:
        await asyncio.wait_for(key_events[user].wait(), timeout=2)
    except:
        pass

# ================= MESSAGE SEND =================
async def send_message(cmd):

    try:
        _, target, text = cmd.split(" ", 2)
    except:
        print("Usage: /msg user text")
        return

    if target not in known_keys:
        await request_key(target)

    if target not in known_keys:
        print("No key for user")
        return

    check_fingerprint(target, known_keys[target])

    receiver_pub = PublicKey(bytes.fromhex(known_keys[target]))
    enc = encrypt(text, private_key, receiver_pub)

    await send({
        "type": "message",
        "to": target,
        "data": enc
    })

# ================= INPUT LOOP =================
def input_loop():
    global running

    while running:
        cmd = input("> ").strip()

        if not cmd:
            continue

        # ---------- HELP ----------
        if cmd == "/help":
            print("""
====================================
        E2EE CHAT COMMANDS
====================================

/list              show online users
/msg user text     send encrypted message
/finger user       show fingerprint
/help              show help
/quit              exit client

====================================
Notes:
- E2EE using NaCl Box
- Server cannot read messages
- Fingerprints detect key changes
====================================
""")
            continue

        # ---------- QUIT ----------
        if cmd == "/quit":
            running = False
            asyncio.run_coroutine_threadsafe(ws_global.close(), loop)
            break

        # ---------- LIST ----------
        if cmd == "/list":
            asyncio.run_coroutine_threadsafe(
                send({"type": "list"}),
                loop
            )

        # ---------- MSG ----------
        if cmd.startswith("/msg "):
            asyncio.run_coroutine_threadsafe(send_message(cmd), loop)

        # ---------- FINGERPRINT ----------
        if cmd.startswith("/finger "):
            user = cmd.split(" ", 1)[1]

            if user not in known_keys:
                print("Unknown user")
                continue

            print(fingerprint(known_keys[user]))

# ================= RECEIVER =================
async def receiver(ws):

    async for raw in ws:

        try:
            data = json.loads(raw)
        except:
            continue

        t = data.get("type")

        # ---------- SYSTEM ----------
        if t == "system":
            print(f"\n[SYSTEM] {data['text']}")

        # ---------- KEY ----------
        elif t == "key":
            user = data.get("user")
            key = data.get("public_key")

            if user and key:
                known_keys[user] = key
                check_fingerprint(user, key)

                if user in key_events:
                    key_events[user].set()

        # ---------- MESSAGE ----------
        elif t == "message":
            sender = data.get("from")
            enc = data.get("data")
            sender_key = data.get("public_key")

            if sender_key:
                known_keys[sender] = sender_key
                check_fingerprint(sender, sender_key)

            if sender not in known_keys:
                print("\n[ERROR] missing key")
                continue

            try:
                sender_pub = PublicKey(bytes.fromhex(known_keys[sender]))
                text = decrypt(enc, private_key, sender_pub)

                print(f"\n{sender}: {text}")

            except:
                print("\n[decrypt error]")

# ================= MAIN =================
async def main():

    global ws_global, loop

    loop = asyncio.get_running_loop()

    threading.Thread(target=input_loop, daemon=True).start()

    async with websockets.connect("ws://127.0.0.1:8765") as ws:

        ws_global = ws

        await ws.send(json.dumps({
            "user": USERNAME,
            "public_key": public_key_hex
        }))

        print("E2EE Chat Running")
        print("Type /help")

        await receiver(ws)

if __name__ == "__main__":
    asyncio.run(main())
