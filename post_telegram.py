"""
Posts a piece of text to the IPICO Telegram channel via the Bot API.
Respects `dry_run` in config.yaml: if true, logs the would-be post
and exits without calling the API.

Required env vars:
  TELEGRAM_BOT_TOKEN
  TELEGRAM_CHAT_ID   (e.g. "@ipico_news")
"""
import os
import sys
import requests
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def post(text: str, dry_run: bool):
    if dry_run:
        print(f"[DRY RUN] Would post to Telegram:\n{text}")
        return

    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    resp = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "disable_web_page_preview": False},
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")

    msg_id = data["result"]["message_id"]
    print(f"Posted to Telegram (message_id: {msg_id})")


if __name__ == "__main__":
    cfg = load_config()
    text = sys.stdin.read().strip() if not sys.stdin.isatty() else sys.argv[1]
    post(text, dry_run=cfg.get("dry_run", True))
