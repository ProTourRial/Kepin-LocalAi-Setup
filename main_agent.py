import json
import os
import requests
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODEL_NAME = "qwen2.5-coder:3b"

tools = [
    {
        "type": "function",
        "function": {
            "name": "check_server_status",
            "description": "Cek apakah sebuah URL server lokal berjalan atau tidak.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL lengkap server, contoh: http://localhost:8080"
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_safe_bash",
            "description": "Menjalankan perintah CLI sederhana untuk mengecek sistem (HANYA perintah aman).",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Perintah bash, contoh: 'df -h' atau 'free -m'"
                    }
                },
                "required": ["command"]
            }
        }
    }
]

def load_guardrail_rules():
    rules_file = "rules.json"
    default_rules = {
        "allowed_domains": ["localhost", "127.0.0.1"],
        "blocked_commands": ["rm", "sudo", "mkfs", "dd", "shutdown", "reboot", ">"]
    }
    if not os.path.exists(rules_file):
        with open(rules_file, "w") as f:
            json.dump(default_rules, f, indent=4)
        return default_rules

    with open(rules_file, "r") as f:
        return json.load(f)

def execute_tool(tool_name: str, tool_args: dict) -> str:
    rules = load_guardrail_rules()

    if tool_name == "check_server_status":
        url = tool_args.get("url", "")
        if not any(domain in url for domain in rules["allowed_domains"]):
            return f"⛔ GUARDRAIL BLOCKED: Akses ke {url} ditolak. Hanya domain lokal yang diizinkan."

        try:
            res = requests.get(url, timeout=3)
            return f"✅ Server merespons dengan Status Code: {res.status_code}"
        except Exception as e:
            return f"❌ Server tidak merespons: {str(e)}"

    elif tool_name == "execute_safe_bash":
        cmd = tool_args.get("command", "")
        for blocked in rules["blocked_commands"]:
            if blocked in cmd:
                return f"⛔ GUARDRAIL BLOCKED: Perintah '{cmd}' mengandung kata terlarang '{blocked}'."

        return f"✅ [SIMULASI] Perintah '{cmd}' aman dan akan dieksekusi di terminal."

    return "⛔ ERROR: Tool tidak dikenal."

def run_agent(user_prompt: str):
    print(f"\n👤 Anda: {user_prompt}")

    messages = [
        {"role": "system", "content": "Anda adalah asisten DevOps dan Server Tester lokal. Gunakan tools yang tersedia jika Anda butuh data real-time dari sistem. Jawab dalam Bahasa Indonesia."},
        {"role": "user", "content": user_prompt}
    ]

    while True:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)

                print(f"🔧 AI memanggil tool: {func_name}({func_args})")

                tool_result = execute_tool(func_name, func_args)
                print(f"🛡️ Hasil Guardrail: {tool_result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })

        else:
            print(f"🤖 AI: {message.content}")
            break

if __name__ == "__main__":
    print("=== Memulai Core Agent Lokal ===")
    print("Ketik 'exit' untuk keluar.\n")

    while True:
        user_input = input("👤 Anda: ")
        if user_input.lower() in ['exit', 'keluar', 'quit']:
            break
        run_agent(user_input)