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
