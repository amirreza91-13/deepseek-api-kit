 <div align="center">

# DeepSeek API Kit

### Python · FastAPI · API Integration

A Python project exploring API-compatible model access through a proxy service and a separate DeepSeek-oriented chat application.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)
![REST API](https://img.shields.io/badge/REST%20API-2563EB?style=for-the-badge)
![DeepSeek](https://img.shields.io/badge/DeepSeek-0B1220?style=for-the-badge)

[Overview](#overview) · [Architecture](#architecture) · [Setup](#getting-started) · [Security](#security)

</div>

---

## Overview

DeepSeek API Kit is a Python project containing two FastAPI applications:

* An OpenAI-style API proxy.
* A separate DeepSeek-oriented chat service with a browser-facing interface and JSON-based session persistence.

The project explores how model APIs can be integrated into Python services and how an application can organize chat interactions and session data.

## Architecture

```text
API Client
    |
    v
OpenAI-Style Proxy
    |
    v
Model API Integration


Browser Interface
    |
    v
DeepSeek Chat Service
    |
    +---- Chat Workflow
    |
    +---- JSON Session Persistence
```

The two paths describe the major components identified in the repository. They do not imply that every endpoint or integration has been tested end to end.

## Technology Stack

| Technology   | Purpose                    |
| ------------ | -------------------------- |
| Python       | Application implementation |
| FastAPI      | HTTP API framework         |
| REST APIs    | Service communication      |
| DeepSeek API | Model integration          |
| JSON         | Chat-session persistence   |

## Getting Started

### Prerequisites

* Python compatible with the project's dependencies.
* pip.
* A DeepSeek API key if required by the selected workflow.

### 1. Clone the Repository

```bash
git clone https://github.com/amirreza91-13/deepseek-api-kit.git
cd deepseek-api-kit
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Use the dependency file included in the repository, if present. For example:

```bash
pip install -r requirements.txt
```

If the repository uses another dependency-management method, follow its configuration instead.

### 4. Configure Environment Variables

Create a local `.env` file if supported by the application, based on `.env.example`.

```dotenv
DEEPSEEK_API_KEY=your_api_key_here
```

Replace the placeholder with your own key. Do not commit `.env` or publish API credentials.

### 5. Run the Applications

The repository contains these FastAPI entry points:

**OpenAI-style proxy**

```bash
uvicorn openai_proxy.main:app --host 127.0.0.1 --port 8000
```

**DeepSeek chat service**

```bash
uvicorn deepseek_chat.main:app --host 127.0.0.1 --port 8001
```

Run the service you need from the repository root. The commands assume that the project dependencies are installed and the module paths remain unchanged.

FastAPI commonly exposes interactive API documentation at `/docs` when enabled. Confirm the route in the running application.

## Configuration

Before using the services, verify:

* The expected API-key environment variable.
* The model identifier and upstream API endpoint.
* The proxy's request and response formats.
* The location and persistence behavior of chat-session files.
* The intended host and port for each service.

Do not assume every OpenAI-compatible endpoint supports every feature of every provider.

## Security

The current codebase requires a security review before network exposure.

* Keep development services bound to `127.0.0.1` unless remote access is intentionally configured.
* Do not expose an unauthenticated proxy to the public internet.
* Review CORS configuration and restrict allowed origins to trusted clients.
* Add appropriate authentication and authorization where required.
* Store API keys in environment variables or a secure secret manager.
* Avoid logging credentials, authorization headers, or sensitive conversation data.
* Protect JSON session files and validate their access permissions.
* Apply request limits and suitable error handling.

**Important:** CORS restrictions are not a replacement for server-side authentication.

## Project Scope

This repository is useful for exploring:

* Python API services.
* Model-provider integration.
* OpenAI-style request interfaces.
* Chat application structure.
* Session persistence.

Its security, reliability, and provider compatibility should be validated before use in a public or production environment.

## License

A `LICENSE` file is present and declares the MIT License. Its copyright notice names `mohammad-mousavi005`; confirm that attribution is correct and that you have the necessary rights to publish and license all included code before relying on or changing that notice.

---

<div align="center">

**Exploring API integration and practical LLM application design.**

[Repository](https://github.com/amirreza91-13/deepseek-api-kit)

</div>
