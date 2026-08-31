# IPICO Telegram Auto-Post Agent

Drafts posts in Russian about obesity prevention/control, fact-checked via
live web search against WHO/ВОЗ, Минздрав РФ, and peer-reviewed sources,
then posts to the @ipico_news Telegram channel on a daily schedule.
Ships in **dry-run mode** — logs what it would post without publishing,
until you turn that off.

## Setup

### 1. Create a Telegram bot
- Open Telegram, message **@BotFather**, send `/newbot`, follow the prompts.
- Save the token it gives you (looks like `123456789:AAH...`).

### 2. Add the bot to your channel
- Go to @ipico_news → Administrators → Add Admin → add your new bot →
  make sure "Post Messages" permission is on.

### 3. Get an Anthropic API key
- [console.anthropic.com](https://console.anthropic.com) → API Keys → Create Key.
- Make sure the account has credits (Plans & Billing).

### 4. Push this folder to a GitHub repo
Same process as before: create a repo, upload these files (including the
hidden `.github/workflows/post.yml` — use "creating a new file" and type
the full path with slashes if drag-and-drop flattens it).

### 5. Add repository secrets
Repo → Settings → Secrets and variables → Actions → New repository secret.
Add: `ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (value:
`@ipico_news`).

### 6. Test it manually
Actions tab → "Auto-post to Telegram" → Run workflow. Check the log —
with `dry_run: true` you'll see the drafted Russian-language post but
nothing goes live.

### 7. Go live
Once you like the drafts, set `dry_run: false` in `config.yaml`, commit,
and push. It now posts once daily (11:00 Moscow time — no DST changes to
worry about, unlike the GALA Health/CEST schedule).

## Notes
- Topics cycle in order (no repeats until the full list is used) — edit
  `config.yaml` anytime to add, remove, or reorder topics.
- Stats are only included when the model finds and verifies them via
  search this run — otherwise it writes qualitatively instead of guessing.
- Uses the same Anthropic API key/account as any other agent you're
  running — keep an eye on shared credit balance.
