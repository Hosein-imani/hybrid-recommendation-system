import json

from src.data.loader import DataLoader

from src.collaborative.model import CollaborativeModel
from src.collaborative.evaluator import CollaborativeEvaluator
from src.collaborative.recommender import CollaborativeRecommender

from src.config.settings import (
    COLLABORATIVE_REPORTS_DIR,
    COLLABORATIVE_RECOMMENDATIONS_DIR,
    COLLABORATIVE_MODELS_DIR,
)


def main():

    # ======================================
    # Load Dataset
    # ======================================

    print("Loading datasets...")

    loader = DataLoader()

    ratings = loader.load_ratings()
    movies = loader.load_movies()

    print(f"Ratings: {len(ratings)}")
    print(f"Movies: {len(movies)}")

    # ======================================
    # Create Model
    # ======================================

    print("\nPreparing SVD model...")

    collaborative_model = CollaborativeModel(
        n_factors=50,
        learning_rate=0.005,
        regularization=0.02,
        epochs=20,
    )

    # ======================================
    # Prepare Data
    # ======================================

    print("\nPreparing dataset...")

    trainset, testset = collaborative_model.prepare_data(
        ratings
    )

    # ======================================
    # Train
    # ======================================

    print("\nTraining model...")

    collaborative_model.train()

    # ======================================
    # Evaluate
    # ======================================

    print("\nEvaluating model...")

    evaluator = CollaborativeEvaluator(
        collaborative_model.model
    )

    results = evaluator.evaluate(
        testset
    )

    print("\nEvaluation Results:")

    print(results)

    # ======================================
    # Save Evaluation Report
    # ======================================

    report_path = (
        COLLABORATIVE_REPORTS_DIR /
        "svd_evaluation_report.txt"
    )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "Collaborative Filtering - SVD\n"
        )

        file.write(
            "=============================\n\n"
        )

        for key, value in results.items():

            file.write(
                f"{key}: {value}\n"
            )

    print("\nReport saved:")

    print(report_path)

    # ======================================
    # Recommendation
    # ======================================

    print("\nGenerating recommendations...")

    recommender = CollaborativeRecommender(
        model=collaborative_model.model,
        trainset=trainset,
        movies=movies,
    )

    recommendations = recommender.recommend(
        user_id=1,
        n_recommendations=10,
    )

    print(recommendations)

    recommendation_path = (
        COLLABORATIVE_RECOMMENDATIONS_DIR /
        "user_1_recommendations.csv"
    )

    recommendation_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    recommendations.to_csv(
        recommendation_path,
        index=False,
    )

    print("\nRecommendations saved:")

    print(recommendation_path)

    # ======================================
    # Save Model
    # ======================================

    saved_files = collaborative_model.save()

    metadata = collaborative_model.get_metadata(
        ratings,
        movies,
    )

    metadata_path = (
        COLLABORATIVE_MODELS_DIR /
        "metadata.json"
    )

    with open(
        metadata_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
        )

    print("\nModel artifacts saved:")

    print(saved_files["model_path"])
    print(saved_files["trainset_path"])
    print(metadata_path)


if __name__ == "__main__":
    main()