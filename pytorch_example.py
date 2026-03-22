# examples/pytorch_example.py
# KaggleNotify — PyTorch usage example
# Copy this into your Kaggle notebook cell

from kaggle_notify import setup, PyTorchNotifyCallback
import torch
import torch.nn as nn

notifier = setup("My PyTorch Experiment")
hook = PyTorchNotifyCallback(notifier, total_epochs=10)

model = nn.Sequential(nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10))
optimizer = torch.optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()

for epoch in range(1, 11):
    model.train()
    running_loss = 0.0
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(X_batch), y_batch)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    avg_loss = running_loss / len(train_loader)

    # Validate
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for X_batch, y_batch in val_loader:
            preds = model(X_batch).argmax(dim=1)
            correct += (preds == y_batch).sum().item()
            total += len(y_batch)
    val_acc = correct / total

    # Notify
    hook.on_epoch_end(epoch, {"loss": avg_loss, "val_accuracy": val_acc})

hook.on_train_end()
