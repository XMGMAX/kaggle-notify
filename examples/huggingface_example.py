# examples/huggingface_example.py
# KaggleNotify — HuggingFace Transformers usage example

from kaggle_notify import setup, HFNotifyCallback
from transformers import Trainer, TrainingArguments, AutoModelForSequenceClassification

notifier = setup("My HuggingFace Experiment")

model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    evaluation_strategy="epoch",
    logging_steps=50,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    callbacks=[HFNotifyCallback(notifier)],  # ← add this line
)

trainer.train()
