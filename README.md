@'
<div align="center">

# 🚀 DeepSeek API Kit

**A lightweight toolkit for integrating DeepSeek into local applications and OpenAI-compatible clients.**

<br>

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-AI-4D6BFE)](https://www.deepseek.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<br>

🧠 **Thinking** &nbsp; • &nbsp; 🔍 **Web Search** &nbsp; • &nbsp; 📡 **Streaming**  
💾 **Persistent Sessions** &nbsp; • &nbsp; 🖥️ **Management Panel** &nbsp; • &nbsp; 🔌 **OpenAI Compatibility**

</div>

---

## ✨ Overview

**DeepSeek API Kit** provides two lightweight local services for working with DeepSeek:

- 🔌 **OpenAI Proxy** — an OpenAI-compatible API layer for applications and clients.
- 💬 **DeepSeek Chat Server** — a chat service with persistent sessions and a browser-based management panel.

The project is designed to keep the integration simple while providing useful controls such as **Thinking**, **Web Search**, **Streaming**, session management, and CORS support.

---

## ⚡ Features

| Feature | OpenAI Proxy | DeepSeek Chat |
|---|:---:|:---:|
| 🔌 OpenAI-compatible API | ✅ | ❌ |
| 🧠 Thinking control | ✅ | ✅ |
| 🔍 Web Search control | ✅ | ✅ |
| 📡 Streaming | ✅ | ✅ |
| 💾 Persistent sessions | ❌ | ✅ |
| 🖥️ Web management panel | ❌ | ✅ |
| 🌐 CORS | ❌ | ✅ |
| 🛡️ API / challenge error handling | ✅ | ✅ |

---

## 🏗️ Architecture

```mermaid
flowchart TD
    A[Client / Application] --> B[DeepSeek API Kit]

    B --> C[OpenAI-Compatible Proxy]
    B --> D[DeepSeek Chat Server]

    C --> E[DeepSeek]
    D --> E

    D --> F[(Persistent Sessions)]
    D --> G[Web Management Panel]
