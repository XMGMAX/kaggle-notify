# KaggleNotify 🔔

> Get **Telegram notifications** for your Kaggle training runs — epoch updates, crash alerts, and completion messages. Zero config. One line of code.

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Kaggle-20BEFF)](https://kaggle.com)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 Epoch updates | Loss, accuracy + trend arrows ↑↓ after every epoch |
| 🏆 Best model alert | Fires whenever val_accuracy hits a new high |
| ⏱ ETA | Time elapsed shown in every message |
| ❌ Crash alerts | Full traceback + CUDA OOM detection sent to Telegram |
| 🔇 Fail-silent | Telegram errors never crash your training |
| 🧩 4 frameworks | Keras, PyTorch, HuggingFace, Sklearn |

---

## 🚀 Quick Start

```python
from kaggle_notify import setup, KerasNotifyCallback

notifier = setup("My Experiment")  # sends a test ping immediately

model.fit(X_train, y_train,
          callbacks=[KerasNotifyCallback(notifier)])
```

---

## 📦 Installation on Kaggle

```python
# In a Kaggle notebook cell:
!pip install requests  # already installed, but just in case
!wget https://raw.githubusercontent.com/XMGMAX/kaggle-notify/main/kaggle_notify.py
```

---

## 🔑 Setup (one-time)

See [SETUP.md](SETUP.md) for the full BotFather + Kaggle Secrets walkthrough.

**TL;DR:**
1. Create a bot via [@BotFather](https://t.me/BotFather) → get `BOT_TOKEN`
2. Get your Chat ID from [@userinfobot](https://t.me/userinfobot)
3. Add both as Kaggle Secrets: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

---

## 📬 Example Telegram Messages

**Epoch update:**
```
📊 My Experiment — Epoch 5/10  ⏱ 12m 34s
  loss: 0.3421 ↓
  accuracy: 0.8812 ↑
  val_loss: 0.4102 ↓
  val_accuracy: 0.8654 ↑
```

**Completion:**
```
🎉 Training Complete!
📌 My Experiment
⏱ Time: 47m 32s
📈 Best Val Accuracy: 0.8921
```

**Crash alert:**
```
❌ Training Crashed!
⏱ Failed at: 23m 11s
💥 RuntimeError: CUDA out of memory
💡 Tip: Reduce batch size or use gradient checkpointing.
📋 Traceback...
```

---

## 🧩 Framework Examples

| Framework | File |
|---|---|
| Keras / TensorFlow | [examples/keras_example.py](examples/keras_example.py) |
| PyTorch | [examples/pytorch_example.py](examples/pytorch_example.py) |
| HuggingFace | [examples/huggingface_example.py](examples/huggingface_example.py) |
| Scikit-learn | [examples/sklearn_example.py](examples/sklearn_example.py) |

---

## 📄 License

MIT — Built by [XMGMAX](https://github.com/XMGMAX)
