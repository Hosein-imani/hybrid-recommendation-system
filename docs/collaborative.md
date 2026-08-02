# Collaborative Filtering (Matrix Factorization using Surprise SVD)

## Overview

This module implements a **Collaborative Filtering Recommendation System** using the **Surprise** library and the **SVD (Singular Value Decomposition)** algorithm.

Unlike Content-Based Filtering, this approach learns user preferences directly from historical rating behavior rather than movie metadata.

---

# Workflow

```text
Ratings Dataset
        │
        ▼
Prepare Surprise Dataset
        │
        ▼
Train SVD Model
        │
        ▼
Evaluate Model
        │
        ▼
Generate Recommendations
        │
        ▼
Save Reports & Artifacts
```

---

# Project Structure

```text
src/
└── collaborative/
    ├── model.py
    ├── evaluator.py
    ├── recommender.py
    └── __init__.py

scripts/
└── collaborative/
    ├── run_svd.py
    └── test_collaborative.py
```

---

# Components

## model.py

Responsible for:

* Preparing the Surprise dataset
* Training the SVD model
* Predicting ratings
* Saving the trained model
* Loading a trained model
* Exporting metadata

---

## evaluator.py

Evaluates the trained model using:

* RMSE
* MAE

---

## recommender.py

Generates Top-N movie recommendations for a given user based on estimated ratings produced by the trained SVD model.

---

## run_svd.py

Complete training pipeline:

1. Load datasets
2. Prepare data
3. Train SVD
4. Evaluate
5. Generate recommendations
6. Save reports
7. Save trained model

---

## test_collaborative.py

Loads an already-trained model and generates recommendations without retraining.

---

# Model

Algorithm:

* Surprise SVD

Training:

* Stochastic Gradient Descent (SGD)

Optimization Objective:

* Matrix Factorization

---

# Outputs

Training generates the following artifacts:

```text
outputs/
└── collaborative/
    ├── reports/
    │   └── svd_evaluation_report.txt
    │
    ├── recommendations/
    │   └── user_1_recommendations.csv
    │
    └── models/
        ├── svd_model.pkl
        ├── trainset.pkl
        └── metadata.json
```

Only lightweight showcase files are tracked in GitHub.

Large generated model artifacts are intentionally excluded from version control.

---

# Evaluation Metrics

The model is evaluated using:

* RMSE (Root Mean Squared Error)
* MAE (Mean Absolute Error)

These metrics measure how accurately the model predicts unseen user ratings.

---

# Technologies

* Python
* Pandas
* NumPy
* Surprise
* Joblib

---

# Future Improvements

* SVD++
* NMF
* Implicit Feedback
* Hybrid Recommendation System
* Hyperparameter Optimization
* Precision@K
* Recall@K
* NDCG
* FastAPI Deployment
