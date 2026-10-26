# 🤖 Kepin — Local AI Agent for DevOps & Research

> A self-hosted, uncensored AI agent that runs entirely on your machine. Built on Ollama + Qwen2.5-Coder, with custom tool-calling for server testing, web research, GitHub inspection, and persistent memory.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](#-license)

---

## 📖 Overview

**Kepin** is a personal experiment in building a *fully local, tool-augmented AI agent* — no cloud APIs, no external LLM providers, no data leaving your machine. It acts as a DevOps assistant and autonomous researcher with a focus on transparency and self-hosted operation.

The agent uses a **custom JSON-based tool-calling parser** instead of relying on native function-calling APIs, making it portable across any chat-completion-compatible LLM backend.

---

## ✨ Features

| Capability | Tool | Description |
|------------|------|-------------|
| 🩺 Server Health | `check_server_status` | HTTP GET to allowlisted domains |
| 🐚 Shell Simulator | `execute_safe_bash` | Command *simulation* with blocklist guardrails |
| 🔎 Web Search | `search_web` | DuckDuckGo search — top 3 snippets, no API key required |
| 📦 GitHub Reader | `read_github_repo` | Fetch public repo metadata via GitHub API |
| 🧠 Long-Term Memory | `save_to_brain` | Persist facts to `kepin_brain.json`, auto-injected per session |

### Design Principles

- **Local-first** — Everything runs against `localhost:11434` (Ollama)
- **Portable tool-calling** — Regex-based JSON extraction; no native function-calling required
- **Transparent** — Every tool invocation and guardrail decision is logged to console
- **Simulation-safe** — Shell execution is *simulated*; no real command runs

---

## 🚀 Quick Start

### Prerequisites

- Python ≥ 3.10
- [Ollama](https://ollama.com/) installed and running
- Qwen2.5-Coder model pulled:

```bash
ollama pull qwen2.5-coder:3b
```

### Install & Run

```bash
git clone https://github.com/<your-username>/kepin.git
cd kepin

python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

pip install openai requests duckduckgo-search
python kepin.py
```

---

## ⚙️ Configuration

Two files are auto-generated on first run:

### `rules.json` — Guardrails

```json
{
  "allowed_domains": ["localhost", "127.0.0.1"],
  "blocked_commands": ["sudo", "mkfs", "dd", "shutdown", "reboot", ">"]
}
```

Edit this file to expand or restrict what the agent can do.

### `kepin_brain.json` — Persistent Memory

```json
{
  "production_server": "Port 9000",
  "db_host": "10.0.0.5"
}
```

The entire file is injected into the system prompt on every session. Delete it to reset memory.

---

## ⚠️ Security & Guardrails

Kepin includes **basic** safety mechanisms, but they are **not production-grade**:

- Domain allowlist uses **substring matching** → `http://evil.com?x=localhost` can bypass
- Command blocklist is **case-sensitive** → `SuDo`, `s udo` can bypass
- Shell execution is **simulated only** — no real commands are run

**Do not expose this agent to untrusted input.** See [Known Limitations](#-known-limitations).

---

## 🧪 Known Limitations

Current technical debts (contributions welcome):

| Area | Issue |
|------|-------|
| Guardrail (URL) | Substring domain matching — bypassable |
| Guardrail (command) | Case-sensitive, no normalization |
| Parser | Greedy regex `\{.*\}` — fails on multiple JSON blocks |
| Memory | Entire brain injected per prompt — token cost grows unbounded |
| GitHub API | 60 req/hour unauthenticated limit |
| Shell exec | Simulation only (intentional) |

---

## ⚠️ Disclaimer

**This project is provided for educational and personal use only.**

- The author **is not responsible** for any misuse, damage, or data loss.
- The "uncensored" persona in the system prompt is a **prompt-engineering experiment** and does not represent endorsement of unsafe AI behavior.
- Guardrails are **best-effort**, not security boundaries. Do not run against untrusted input.
- Local LLMs can hallucinate. **Always verify outputs** before acting on them.

**Free to use, free to modify — at your own risk.**

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for the full text.

---

## 👤 Author

**Abia Nugrahanto**

Personal project — built to understand how local LLM agents work under the hood. Forks, issues, and discussions are welcome.

---

## 🙏 Acknowledgements

- [Ollama](https://ollama.com/) — painless local LLM runtime
- [Qwen Team](https://github.com/QwenLM) — Qwen2.5-Coder model
- [DuckDuckGo Search](https://github.com/deedy5/duckduckgo_search) — free web search
- Open-source community — for the tools that make projects like this possible

---

<div align="center">

*Built with curiosity, caffeine, and a healthy distrust of cloud APIs.*

</div>
```

---