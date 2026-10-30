# 🤖 Kepin — Local AI Agent for DevOps & Research

> A self-hosted, tool-augmented AI agent that runs entirely on your machine.
> Built on Ollama and a custom fine-tuned Qwen2.5-Coder model (`kepinV1`), with
> bare-metal tool calling for server checks, web research, GitHub inspection,
> and persistent memory. No cloud APIs.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?logo=ollama)](https://ollama.com/)
[![Model](https://img.shields.io/badge/%F0%9F%A4%97%20Model-bygrafy%2FkepinV1-yellow)](https://huggingface.co/bygrafy/kepinV1)
[![License](https://img.shields.io/badge/License-MIT-green)](#-license)

---

## 📖 Overview

**Kepin** is a personal AI assistant experiment — a *fully local, tool-augmented
agent* that runs entirely on your machine. No cloud LLM providers, no data leaving
your PC. It acts as a DevOps helper and autonomous researcher, with a focus on
transparency and self-hosted operation.

Tool calling is handled by a **custom JSON parser** instead of provider-native
function calling, so the agent stays portable across any OpenAI-compatible LLM
backend:

```json
{"tool": "check_server_status", "args": {"url": "http://localhost:11434"}}
```

The system prompt is specifically tuned to **prevent tool hallucination** — the
model is explicitly forbidden from inventing tools that do not exist.

---

## ✨ Features

| Capability | Tool | Description |
| :--- | :--- | :--- |
| 🩺 Server Health | `check_server_status` | HTTP GET to allowlisted domains only |
| 🐚 Shell Simulator | `execute_safe_bash` | Command *simulation* with blocklist guardrails |
| 🔎 Web Search | `search_web` | DuckDuckGo search — top 3 snippets, no API key |
| 📦 GitHub Reader | `read_github_repo` | Public repo metadata via the GitHub API |
| 🧠 Long-Term Memory | `save_to_brain` | Persist facts to `kepin_brain.json`, auto-injected per session |

### Design Principles

- **Local-first** — everything runs against `http://localhost:11434` (Ollama)
- **Portable tool calling** — regex-based JSON extraction; no native function calling required
- **Anti-hallucination** — the system prompt forbids inventing tools such as `ask_ai` or `chatgpt`
- **Transparent** — every tool call and guardrail decision is logged to the console
- **Simulation-safe** — shell execution is *simulated*; no real commands are run

---

## 🗂️ Project Structure

```text
Kepin/
├── main_agent.py       # Agent loop, tool dispatcher, guardrails, system prompt
├── ModelFile           # Ollama Modelfile (chat template, num_ctx 2048)
├── README.md
├── rules.json          # Auto-generated on first run — guardrail config
└── kepin_brain.json    # Auto-generated on first run — long-term memory
```

---

## 🚀 Quick Start

### Prerequisites

- Python ≥ 3.10
- [Ollama](https://ollama.com/) installed and running
- Git

### Step 1 — Install the model

Kepin uses a custom fine-tuned model hosted on Hugging Face. Ollama can pull it
directly:

```bash
ollama pull hf.co/bygrafy/kepinV1:Q4_K_M

echo 'FROM hf.co/bygrafy/kepinV1:Q4_K_M' > Modelfile
ollama create kepinV1 -f Modelfile
rm Modelfile

ollama list
```

The output of `ollama list` should include `kepinV1:latest`.

<details>
<summary>Alternative: build from a local GGUF file</summary>

```bash
# Put KepinV1.gguf in the project folder, then:
ollama create kepinV1 -f ModelFile
```

The included `ModelFile` expects `FROM ./KepinV1.gguf`.

</details>

### Step 2 — Install & run the agent

```bash
git clone https://github.com/ProTourRial/kepinV1.git
cd kepinV1

python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

pip install openai requests ddgs

python main_agent.py
```

---

## ▶️ Usage

### Mode 1 — Direct chat via terminal (no tools)

For quick Q&A without running the Python agent:

```bash
ollama run kepinV1 "Jelaskan konsep reverse proxy dalam Bahasa Indonesia"
```

### Mode 2 — Full agent with tools (recommended)

Enables every Kepin capability: server checks, web search, GitHub reader, and
long-term memory.

```bash
python main_agent.py
```

Expected startup output:

```text
=== Memulai KepinV1 (The Researcher & Memory) ===
Ketik 'exit' untuk keluar.

👤 Anda: _
```

### Example Prompts

| Prompt | Tool invoked | Purpose |
| :--- | :--- | :--- |
| `cek apakah server Ollama aktif di http://localhost:11434` | `check_server_status` | Check local HTTP server status |
| `cari di internet siapa penemu bahasa Python` | `search_web` | Browse via DuckDuckGo |
| `telaah repositori github Vigil-SOC/vigil` | `read_github_repo` | Read GitHub repo metadata |
| `simpan kesimpulan tentang Vigil SOC ke ingatanmu` | `save_to_brain` | Persist to `kepin_brain.json` |
| `ingat-ingat, apa yang kamu tahu tentang Vigil SOC?` | *(reads brain)* | Retrieve from long-term memory |
| `halo, apa kabar?` | *(plain text)* | Normal conversation, no tool |

### Stopping the Agent

Type `exit`, `keluar`, or `quit`, then press <kbd>Enter</kbd>.

---

## ⚙️ Configuration

Two files are auto-generated on first run.

### `rules.json` — Guardrails

```json
{
  "allowed_domains": ["localhost", "127.0.0.1"],
  "blocked_commands": ["sudo", "mkfs", "dd", "shutdown", "reboot", ">"]
}
```

Edit this file anytime to expand or restrict agent capabilities. Changes apply
in real time — no restart needed.

### `kepin_brain.json` — Persistent Memory

```json
{
  "production_server": "Port 9000",
  "db_host": "10.0.0.5"
}
```

The entire file is injected into the system prompt on every session. Delete it
to reset memory.

---

## 🔐 Security & Guardrails

Kepin ships with basic safety mechanisms, but **they are not production-grade**:

| Mechanism | Limitation |
| :--- | :--- |
| Domain allowlist | Substring matching → `http://evil.com?x=localhost` can bypass it |
| Command blocklist | Case-sensitive → `SuDo` or `s udo` can bypass it |
| Shell execution | Simulation only — no real commands are run |

> ⛔ Do not expose this agent to untrusted input. See [Known Limitations](#--known-limitations).

---

## 🧪 Known Limitations

| Area | Issue |
| :--- | :--- |
| Guardrail (URL) | Substring domain matching — bypassable |
| Guardrail (command) | Case-sensitive, no normalization |
| Parser | Greedy regex `\{.*\}` — fails on multiple JSON blocks |
| Memory | Entire brain injected per prompt — token cost grows unbounded |
| GitHub API | 60 requests/hour unauthenticated limit |
| Shell exec | Simulation only (intentional safety measure) |

---

## 📦 Model

| Property | Value |
| :--- | :--- |
| HF repository | `bygrafy/kepinV1` |
| Base model | Qwen2.5-Coder-3B-Instruct |
| Format | GGUF (`Q4_K_M` recommended) |
| Size | ~1.8 GB |
| Context window | 2048 tokens |
| Fine-tuning | QLoRA via Unsloth — 60 steps on a custom tool-calling dataset |

💡 The GGUF file is not stored in this GitHub repository due to size limits. The
model is hosted on Hugging Face for better bandwidth, CDN, and versioning.

---

## ⚠️ Disclaimer

This project is provided for educational and personal use only.

- The author is not responsible for any misuse, damage, or data loss.
- Guardrails are best-effort, **not** security boundaries. Do not run against untrusted input.
- Local LLMs can hallucinate. Always verify outputs before acting on them.
- The "agent" is a prompt-engineering experiment — behaviour depends heavily on the
  underlying model and system prompt.
- Free to use, free to modify — at your own risk.

---

## 📜 License

Released under the **MIT License**.

---

## 👤 Author

**Abia Nugrahanto**

- GitHub: [@ProTourRial](https://github.com/ProTourRial)
- Hugging Face: [@bygrafy](https://huggingface.co/bygrafy)

Personal project — built to understand how local LLM agents work under the hood.
Forks, issues, and discussions are welcome.

---

## 🙏 Acknowledgements

- [Ollama](https://ollama.com/) — painless local LLM runtime
- [Qwen Team](https://github.com/QwenLM) — Qwen2.5-Coder base model
- [Unsloth](https://github.com/unslothai/unsloth) — fast QLoRA fine-tuning
- [ddgs](https://pypi.org/project/ddgs/) — free DuckDuckGo search library
- [Hugging Face](https://huggingface.co/) — model hosting & distribution
- The open-source community — for the tools that make projects like this possible

---

<div align="center">

Built with curiosity, caffeine, and a healthy distrust of cloud APIs. ☕🔒

</div>
