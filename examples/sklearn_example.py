# examples/sklearn_example.py
# KaggleNotify — Scikit-learn usage example

from kaggle_notify import setup, SKLearnNotifyWrapper
from sklearn.ensemble import RandomForestClassifier

notifier = setup("My Sklearn Experiment")

model = RandomForestClassifier(n_estimators=100, random_state=42)

# Wrap the model — use wrapper.fit() instead of model.fit()
wrapper = SKLearnNotifyWrapper(model, notifier)
wrapper.fit(X_train, y_train)

# wrapper passes through all other methods unchanged
preds = wrapper.predict(X_test)
score = wrapper.score(X_test, y_test)
print(f"Test accuracy: {score:.4f}")
