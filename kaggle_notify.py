"""
KaggleNotify — Telegram notifications for Kaggle training runs.
Built by XMGMAX · github.com/XMGMAX/kaggle-notify
"""

import sys
import time
import traceback
import requests

# ── Secrets ────────────────────────────────────────────────────────────────────
def _get_secrets():
    try:
        from kaggle_secrets import UserSecretsClient
        s = UserSecretsClient()
        return s.get_secret("TELEGRAM_BOT_TOKEN"), s.get_secret("TELEGRAM_CHAT_ID")
    except Exception:
        return None, None


# ── Core Notifier ──────────────────────────────────────────────────────────────
class TelegramNotifier:
    def __init__(self, experiment_name="Kaggle Run"):
        self.name = experiment_name
        self.token, self.chat_id = _get_secrets()
        self.start_time = time.time()
        self.best_val_acc = None
        self.last_metrics = {}
        self._ok = bool(self.token and self.chat_id)

    def _elapsed(self):
        s = int(time.time() - self.start_time)
        return f"{s // 3600}h {(s % 3600) // 60}m {s % 60}s" if s >= 3600 else f"{s // 60}m {s % 60}s"

    def _post(self, text):
        if not self._ok:
            return
        try:
            requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                json={"chat_id": self.chat_id, "text": text, "parse_mode": "HTML"},
                timeout=10,
            )
        except Exception:
            pass  # fail-silent — never crash training

    def send_message(self, text):
        self._post(text)

    def send_metrics(self, epoch, logs: dict, total_epochs=None):
        def arrow(key):
            prev = self.last_metrics.get(key)
            cur = logs.get(key)
            if prev is None or cur is None:
                return ""
            if "loss" in key:
                return " ↓" if cur < prev else " ↑"
            return " ↑" if cur > prev else " ↓"

        ep_str = f"{epoch}/{total_epochs}" if total_epochs else str(epoch)
        lines = [f"📊 <b>{self.name}</b>  —  Epoch {ep_str}  ⏱ {self._elapsed()}"]
        for k, v in logs.items():
            lines.append(f"  {k}: {v:.4f}{arrow(k)}")

        val_acc = logs.get("val_accuracy") or logs.get("val_acc")
        if val_acc is not None:
            if self.best_val_acc is None or val_acc > self.best_val_acc:
                self.best_val_acc = val_acc
                lines.append(f"\n🏆 New best val_accuracy: <b>{val_acc:.4f}</b>")

        self.last_metrics = dict(logs)
        self._post("\n".join(lines))

    def send_completion(self, summary: dict = None):
        best = f"{self.best_val_acc:.4f}" if self.best_val_acc else "N/A"
        msg = (
            f"🎉 <b>Training Complete!</b>\n"
            f"📌 {self.name}\n"
            f"⏱ Time: {self._elapsed()}\n"
            f"📈 Best Val Accuracy: {best}"
        )
        if summary:
            for k, v in summary.items():
                msg += f"\n  {k}: {v}"
        self._post(msg)

    def send_error(self, exc: BaseException):
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        if len(tb) > 1500:
            tb = tb[-1500:]
        oom = "CUDA out of memory" in str(exc)
        tip = "\n💡 Tip: Reduce batch size or use gradient checkpointing." if oom else ""
        msg = (
            f"❌ <b>Training Crashed!</b>\n"
            f"⏱ Failed at: {self._elapsed()}\n"
            f"💥 {type(exc).__name__}: {exc}{tip}\n\n"
            f"📋 <pre>{tb}</pre>"
        )
        self._post(msg)


# ── Keras Callback ─────────────────────────────────────────────────────────────
try:
    import tensorflow as tf

    class KerasNotifyCallback(tf.keras.callbacks.Callback):
        def __init__(self, notifier: TelegramNotifier):
            super().__init__()
            self.n = notifier
            self._total = None

        def on_train_begin(self, logs=None):
            self._total = self.params.get("epochs")

        def on_epoch_end(self, epoch, logs=None):
            self.n.send_metrics(epoch + 1, logs or {}, self._total)

        def on_train_end(self, logs=None):
            self.n.send_completion()

except ImportError:
    class KerasNotifyCallback:
        def __init__(self, *a, **kw): pass


# ── PyTorch Hook ───────────────────────────────────────────────────────────────
class PyTorchNotifyCallback:
    """
    Manual hook for custom PyTorch training loops.
    Call .on_epoch_end(epoch, metrics_dict) from your loop.
    """
    def __init__(self, notifier: TelegramNotifier, total_epochs=None):
        self.n = notifier
        self.total = total_epochs

    def on_epoch_end(self, epoch, metrics: dict):
        self.n.send_metrics(epoch, metrics, self.total)

    def on_train_end(self):
        self.n.send_completion()


# ── HuggingFace Callback ───────────────────────────────────────────────────────
try:
    from transformers import TrainerCallback

    class HFNotifyCallback(TrainerCallback):
        def __init__(self, notifier: TelegramNotifier):
            self.n = notifier

        def on_log(self, args, state, control, logs=None, **kwargs):
            if logs and state.epoch:
                self.n.send_metrics(int(state.epoch), logs, state.num_train_epochs)

        def on_train_end(self, args, state, control, **kwargs):
            self.n.send_completion()

except ImportError:
    class HFNotifyCallback:
        def __init__(self, *a, **kw): pass


# ── Sklearn Wrapper ────────────────────────────────────────────────────────────
class SKLearnNotifyWrapper:
    """
    Wraps any sklearn estimator so .fit() triggers Telegram notifications.
    Usage: wrapper = SKLearnNotifyWrapper(model, notifier); wrapper.fit(X, y)
    """
    def __init__(self, model, notifier: TelegramNotifier):
        self.model = model
        self.n = notifier

    def fit(self, X, y, **kwargs):
        self.n.send_message(f"🚀 <b>{self.n.name}</b> — sklearn fit() started")
        try:
            self.model.fit(X, y, **kwargs)
            self.n.send_completion()
        except Exception as e:
            self.n.send_error(e)
            raise
        return self

    def __getattr__(self, name):
        return getattr(self.model, name)


# ── Global Exception Hook ──────────────────────────────────────────────────────
_notifier_ref = None

def _global_hook(exc_type, exc_value, exc_tb):
    if _notifier_ref is not None:
        try:
            _notifier_ref.send_error(exc_value)
        except Exception:
            pass
    sys.__excepthook__(exc_type, exc_value, exc_tb)


# ── setup() — the one-liner entry point ───────────────────────────────────────
def setup(experiment_name="Kaggle Run") -> TelegramNotifier:
    global _notifier_ref
    n = TelegramNotifier(experiment_name)
    _notifier_ref = n
    sys.excepthook = _global_hook
    n.send_message(
        f"✅ <b>KaggleNotify ready!</b>\n"
        f"📌 Experiment: {experiment_name}\n"
        f"🔔 You'll get epoch updates + crash alerts here."
    )
    return n
