# client/client.py
import requests
import json

MODEL = "llama3:8b-instruct-q8_0" # replace with your desired model
URL = "http://localhost:11434/api/chat"
MAX_CHARS = 8000 # history limitations

history = [
    {"role": "system", "content": "You will not respond in markdown. Your responses will be brief and accurate."}
]

def trim_memory(conversation):
    if not conversation:
        return conversation

    system_msg = conversation[0]  # preserve this
    other_msgs = conversation[1:]

    total = 0
    kept = []

    # walk backwards through non-system messages
    for msg in reversed(other_msgs):
        total += len(msg["content"])
        if total > MAX_CHARS:
            break
        kept.append(msg)

    # reverse back to correct chronological order
    kept.reverse()

    # final conversation: system + trimmed history
    return [system_msg] + kept

def stream_chat(prompt: str):
    history.append({"role": "user", "content": prompt})
    history[:] = trim_memory(history)

    with requests.post(
        URL,
        json={
            "model": MODEL,
            "messages": history,
            "stream": True,
        },
        stream=True,
    ) as r:

        reply_text = ""

        for line in r.iter_lines():
            if not line:
                continue
            data = line.decode("utf-8")
            try:
                msg = json.loads(data)
                if "message" in msg and "content" in msg["message"]:
                    chunk = msg["message"]["content"]
                    reply_text += chunk
                    print(chunk, end="", flush=True)
            except:
                pass

    print()

    history.append({"role": "assistant", "content": reply_text})


def main():
    print("Chat local model.")
    while True:
        prompt = input("> ")
        if prompt.strip().lower() == "exit":
            break
        stream_chat(prompt)


if __name__ == "__main__":
    main()
