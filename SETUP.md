# KaggleNotify Setup Guide

Complete walkthrough to get Telegram notifications working on Kaggle.

---

## Step 1 — Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Choose a name (e.g. `Kaggle Notifier`)
4. Choose a username ending in `bot` (e.g. `xmgmax_kaggle_bot`)
5. BotFather will give you a **BOT_TOKEN** — looks like:
   ```
   123456789:ABCdefGhIJKlmNoPQRsTUVwXyz
   ```
6. Copy and save it

---

## Step 2 — Get Your Chat ID

1. Search for **@userinfobot** on Telegram
2. Send `/start`
3. It will reply with your numeric **Chat ID** — looks like:
   ```
   987654321
   ```
4. Copy and save it

---

## Step 3 — Add Secrets to Kaggle

1. Open any notebook on Kaggle
2. In the right sidebar, click the **key icon** (Secrets)
3. Click **"Add a new secret"**
4. Add these two secrets:

| Name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | your token from BotFather |
| `TELEGRAM_CHAT_ID` | your numeric ID from userinfobot |

5. Toggle **"Attach to notebook"** ON for both

---

## Step 4 — Use in Your Notebook

```python
# Download the script (run once)
!wget https://raw.githubusercontent.com/XMGMAX/kaggle-notify/main/kaggle_notify.py

# Import and setup
from kaggle_notify import setup, KerasNotifyCallback
notifier = setup("My Experiment")
```

You'll get an immediate test ping on Telegram confirming it works.

---

## Troubleshooting

**No message received?**
- Double-check the secret names are exactly `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
- Make sure both secrets are attached to the notebook
- Send a message to your bot first on Telegram (bots can't initiate chats)

**`UserSecretsClient` error?**
- This only works inside Kaggle notebooks, not locally

**Telegram `403 Forbidden`?**
- You haven't started a chat with your bot yet — open Telegram, find your bot, and send `/start`
