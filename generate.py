Drafts a Telegram post in Russian based on config.yaml topics/tone.
If the topic calls for a statistic or factual claim, the model uses live
web search to verify it against a credible source (WHO/ВОЗ, Минздрав РФ,
peer-reviewed journals, official statistics) before writing — and is
instructed to skip specific numbers rather than guess if it can't verify one.
"""
import os
import random
import sys
import yaml
import anthropic

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
STATE_PATH = os.path.join(os.path.dirname(__file__), ".topic_cursor")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def pick_topic(cfg):
    topics = cfg["topics"]
    if not cfg.get("cycle", False):
        return random.choice(topics)

    idx = 0
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH) as f:
            idx = int(f.read().strip() or 0)
    topic = topics[idx % len(topics)]
    with open(STATE_PATH, "w") as f:
        f.write(str((idx + 1) % len(topics)))
    return topic


def generate_post(cfg) -> str:
    topic = pick_topic(cfg)
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    system = (
        "You write a single Telegram post in RUSSIAN for IPICO "
        "(Институт профилактики и контроля ожирения), a Russian nonprofit "
        "working on evidence-based obesity prevention and control. "
        "Output ONLY the final post text in Russian, nothing else — no "
        "quotes, no preamble, no explanation. "
        f"Tone: {cfg['tone']} "
        f"Hard limit: {cfg['max_length']} characters. "
        "\n\n"
        "FACTUAL ACCURACY RULE: if the topic involves a specific statistic "
        "or factual claim, you MUST use web search first to verify it "
        "against a credible source — WHO/ВОЗ, Минздрав РФ, a peer-reviewed "
        "journal, or an official statistics report. Only state a number if "
        "you found it from one of those source types in your search results "
        "this turn. If you cannot verify a specific number, do NOT invent "
        "one — write the post qualitatively instead. Never state a "
        "statistic from memory alone without searching."
    )

    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=system,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": f"Напиши пост. Тема: {topic}"}],
    )

    text = "".join(block.text for block in resp.content if block.type == "text").strip()
    text = text.strip('"')

    if len(text) > cfg["max_length"]:
        truncated = text[: cfg["max_length"]]
        # Prefer cutting at the last complete sentence, not mid-word
        last_period = max(truncated.rfind(". "), truncated.rfind(".\n"), truncated.rfind("!"), truncated.rfind("?"))
        if last_period > cfg["max_length"] * 0.5:  # only use it if it's not too far back
            text = truncated[: last_period + 1]
        else:
            text = truncated.rsplit(" ", 1)[0] + "…"

    return text


if __name__ == "__main__":
    cfg = load_config()
    post = generate_post(cfg)
    print(post, file=sys.stderr)
    print(post)
