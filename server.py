import asyncio
import json
import websockets
from datetime import datetime
import hashlib

clients = {}
public_keys = {}

# ================= CONFIG =================
LOG_MODE = "full"   # none | basic | full | hash
LOG_TO_FILE = True
LOG_FILE = "server.log"

# ================= HELPERS =================
def now():
    return datetime.now().strftime("%H:%M:%S")

def ip(ws):
    return ws.remote_address[0] if ws.remote_address else "unknown"

def hash_ip(ip_addr):
    return hashlib.sha256(ip_addr.encode()).hexdigest()[:12]

def write_log(line):
    if LOG_TO_FILE:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")

def log(line):
    print(line)
    write_log(line)

# ================= LOG FORMAT =================
def format_connect(user, ws):
    if LOG_MODE == "none":
        return None

    ip_addr = ip(ws)

    if LOG_MODE == "basic":
        return f"[+] {user}"
    if LOG_MODE == "full":
        return f"[{now()}] [+] {user} | ip={ip_addr}"
    if LOG_MODE == "hash":
        return f"[{now()}] [+] {user} | ip_hash={hash_ip(ip_addr)}"

def format_disconnect(user, ws):
    if LOG_MODE == "none":
        return None

    ip_addr = ip(ws)

    if LOG_MODE == "basic":
        return f"[-] {user}"
    if LOG_MODE == "full":
        return f"[{now()}] [-] {user} | ip={ip_addr}"
    if LOG_MODE == "hash":
        return f"[{now()}] [-] {user} | ip_hash={hash_ip(ip_addr)}"

# ================= HANDLER =================
async def handler(ws):

    user = None

    try:
        auth_raw = await ws.recv()
        auth = json.loads(auth_raw)

        user = auth.get("user")
        pubkey = auth.get("public_key")

        if not user:
            return

        clients[user] = ws
        public_keys[user] = pubkey

        msg = format_connect(user, ws)
        if msg:
            log(msg)

        async for raw in ws:

            try:
                data = json.loads(raw)
            except:
                continue

            t = data.get("type")

            # ---------- LIST ----------
            if t == "list":
                await ws.send(json.dumps({
                    "type": "system",
                    "text": "Online: " + ", ".join(clients.keys())
                }))

            # ---------- GET KEY ----------
            elif t == "get_key":
                target = data.get("user")

                await ws.send(json.dumps({
                    "type": "key",
                    "user": target,
                    "public_key": public_keys.get(target)
                }))

            # ---------- MESSAGE ----------
            elif t == "message":
                target = data.get("to")

                if target in clients:
                    await clients[target].send(json.dumps({
                        "type": "message",
                        "from": user,
                        "public_key": public_keys.get(user),
                        "data": data.get("data")
                    }))

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        if user:
            clients.pop(user, None)
            public_keys.pop(user, None)

            msg = format_disconnect(user, ws)
            if msg:
                log(msg)

# ================= MAIN =================
async def main():
    print("E2EE Chat Server Running")
    print(f"LOG_MODE={LOG_MODE} | LOG_TO_FILE={LOG_TO_FILE}")

    async with websockets.serve(handler, "127.0.0.1", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
