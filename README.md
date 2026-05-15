# 🔐 E2EE Chat Prototype

Lightweight end-to-end encrypted CLI chat using WebSockets and NaCl (PyNaCl).

> ⚠️ Educational project — not production-ready.

---

## 📌 Overview

This project is a minimal experimental chat system that demonstrates:
- End-to-End Encryption (E2EE)
- Client-to-client encrypted messaging
- A server acting only as a message relay (no message access)

The server never sees plaintext messages.

---

## ⚙️ Features

- 🔐 End-to-End Encryption using NaCl Box (PyNaCl)
- 🌐 WebSocket communication
- 💻 CLI-based chat interface
- 👤 Direct user-to-user messaging (`/msg`)
- 📡 Online users list (`/list`)
- 🧾 Public key exchange via server
- 👁 Basic fingerprint verification (key change detection)
- 🖥 Lightweight relay server

---

## 🧠 Security Model

- Messages are encrypted on the client side
- Only the recipient can decrypt messages
- Server only forwards encrypted data
- Public keys are distributed via server
- Fingerprints help detect key changes (basic trust check)

> ⚠️ This is NOT a production secure system.

---

## 📁 Project Structure

```

e2ee-chat-prototype/
│
├── server.py      # WebSocket relay server
├── client.py      # CLI chat client
├── crypto.py      # Encryption logic (NaCl)
└── README.md

````

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install websockets pynacl
````

---

### 2. Run server

```bash
python server.py
```

Server runs on:

```text
ws://127.0.0.1:8765
```

---

### 3. Run client

Run multiple instances for different users:

```bash
python client.py
```

---

## 💬 Commands

```text
/help              Show help
/list              Show online users
/msg user text     Send encrypted message
/finger user       Show fingerprint
/quit              Exit
```

---

## 👁 Fingerprints

* Used to detect possible key changes
* Helps identify unexpected identity changes

---

## ⚠️ Limitations

* No message persistence
* No offline message delivery
* No identity recovery
* No advanced forward secrecy system
* Fingerprints are basic and manually verified
* Keys are not stored between sessions

---

## 🎯 Purpose

This project is for learning and experimentation:

* Understanding encrypted communication
* Learning how messaging systems work internally
* Experimenting with WebSockets and cryptography

---

## 📜 License

GPLv3 

---
