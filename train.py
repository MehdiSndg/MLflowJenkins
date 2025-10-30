"""
Simple training script to demonstrate Jenkins-triggered MLflow runs.
Uses scikit-learn to train a logistic regression model on the Iris dataset.
"""

from pathlib import Path

import mlflow
import mlflow.sklearn
import numpy as np
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def prepare_data(test_size: float = 0.2, random_state: int = 42):
    """Load the Iris dataset and split it into train/test subsets."""
    iris = datasets.load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data,
        iris.target,
        test_size=test_size,
        random_state=random_state,
        stratify=iris.target,
    )
    return X_train, X_test, y_train, y_test


def build_model():
    """Create a simple pipeline with scaling and logistic regression."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "logreg",
                LogisticRegression(
                    C=1.0, solver="lbfgs", max_iter=200, multi_class="auto"
                ),
            ),
        ]
    )


def log_artifacts(run_dir: Path, y_true: np.ndarray, y_pred: np.ndarray):
    """Persist evaluation artifacts and log them with MLflow."""
    run_dir.mkdir(parents=True, exist_ok=True)

    cm = confusion_matrix(y_true, y_pred)
    cm_path = run_dir / "confusion_matrix.csv"
    np.savetxt(cm_path, cm, delimiter=",", fmt="%d")

    metrics_path = run_dir / "metrics.txt"
    accuracy = accuracy_score(y_true, y_pred)
    metrics_path.write_text(f"accuracy: {accuracy:.4f}\n", encoding="utf-8")

    mlflow.log_artifact(cm_path)
    mlflow.log_artifact(metrics_path)


def main():
    mlflow.set_tracking_uri("file:./mlruns")
    mlflow.set_experiment("jenkins-mlflow-demo")

    test_size = 0.2
    random_state = 42

    X_train, X_test, y_train, y_test = prepare_data(test_size, random_state)
    model = build_model()

    with mlflow.start_run():
        # Log input parameters so we can reproduce this run later.
        mlflow.log_params(
            {
                "test_size": test_size,
                "random_state": random_state,
                "model_C": model.named_steps["logreg"].C,
                "model_solver": model.named_steps["logreg"].solver,
                "model_max_iter": model.named_steps["logreg"].max_iter,
            }
        )

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        mlflow.log_metric("accuracy", accuracy)

        # Persist trained model and evaluation artifacts for inspection.
        mlflow.sklearn.log_model(model, artifact_path="model")
        log_artifacts(Path("artifacts"), y_test, y_pred)

        print(f"Model accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    main()
