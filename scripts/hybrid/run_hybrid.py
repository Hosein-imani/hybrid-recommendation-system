import pandas as pd

from src.collaborative.model import (
    CollaborativeModel,
)

from src.collaborative.recommender import (
    CollaborativeRecommender,
)

from src.config.settings import (
    HYBRID_RECOMMENDATIONS_DIR,
    HYBRID_REPORTS_DIR,
)

from src.content_based.feature_engineering import (
    FeatureEngineer,
)

from src.content_based.recommender import (
    ContentBasedRecommender,
)

from src.data.loader import (
    DataLoader,
)

from src.data.preprocessor import (
    DataPreprocessor,
)

from src.hybrid.recommender import (
    HybridRecommender,
)

from src.hybrid.evaluator import (
    HybridEvaluator,
)


USER_ID = 5
SEED_MOVIE_ID = 5
TOP_N_PER_MODEL = 10

OUTPUT_FILE = (
    HYBRID_RECOMMENDATIONS_DIR
    / "hybrid_recommendations.csv"
)

EVALUATION_FILE = (
    HYBRID_REPORTS_DIR
    / "hybrid_evaluation_report.txt"
)


def build_content_features(
    movies: pd.DataFrame,
) -> pd.DataFrame:

    print("\nPreparing Content-Based features...")

    preprocessor = DataPreprocessor()

    processed_movies = (
        preprocessor.preprocess_movies(
            movies
        )
    )

    feature_engineer = FeatureEngineer()

    genre_matrix = (
        feature_engineer.build_genre_matrix(
            processed_movies
        )
    )

    return genre_matrix


def train_collaborative_model(
    ratings: pd.DataFrame,
) -> tuple:

    print("\nPreparing Collaborative model...")

    collaborative_model = CollaborativeModel(
        n_factors=50,
        learning_rate=0.005,
        regularization=0.02,
        epochs=20,
    )

    print(
        "\nPreparing collaborative dataset..."
    )

    trainset, testset = (
        collaborative_model.prepare_data(
            ratings
        )
    )

    print(
        "\nTraining collaborative model..."
    )

    collaborative_model.train()

    return (
        collaborative_model,
        trainset,
    )


def build_recommenders(
    movies: pd.DataFrame,
    ratings: pd.DataFrame,
    collaborative_model,
    trainset,
):

    print(
        "\nInitializing recommenders..."
    )

    content_recommender = (
        ContentBasedRecommender()
    )

    collaborative_recommender = (
        CollaborativeRecommender(
            model=collaborative_model.model,
            trainset=trainset,
            movies=movies,
        )
    )

    hybrid_recommender = (
        HybridRecommender(
            content_recommender=content_recommender,
            collaborative_recommender=collaborative_recommender,
            movies=movies,
            ratings=ratings,
        )
    )

    return hybrid_recommender


def generate_hybrid_recommendations(
    hybrid_recommender,
    genre_matrix: pd.DataFrame,
):

    print(
        "\nGenerating Hybrid recommendations..."
    )

    sections = (
        hybrid_recommender.recommend(
            user_id=USER_ID,
            seed_movie_id=SEED_MOVIE_ID,
            genre_matrix=genre_matrix,
            top_n_per_model=TOP_N_PER_MODEL,
        )
    )

    return sections


def combine_recommendations(
    sections,
) -> pd.DataFrame:

    return pd.concat(
        [
            sections["special"],
            sections["content_based"],
            sections["collaborative"],
        ],
        ignore_index=True,
    )


def save_recommendations(
    recommendations: pd.DataFrame,
) -> None:

    HYBRID_RECOMMENDATIONS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    recommendations.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print(
        "\nHybrid recommendations saved:"
    )

    print(OUTPUT_FILE)


def evaluate_hybrid(
    sections,
) -> dict:

    print(
        "\nEvaluating Hybrid output..."
    )

    evaluator = HybridEvaluator()

    results = evaluator.evaluate(
        sections
    )

    return results


def build_evaluation_report(
    results: dict,
) -> str:

    counts = results["counts"]
    integrity = results["integrity"]
    diversity = results["diversity"]
    scores = results["scores"]
    overlap = results["overlap"]

    report = f"""
HYBRID RECOMMENDATION EVALUATION
================================

COUNTS
------
Special Recommendations:
{counts["special"]}

Content-Based Recommendations:
{counts["content_based"]}

Collaborative Recommendations:
{counts["collaborative"]}

Total Rows:
{counts["total_rows"]}

Total Unique Movies:
{counts["total_unique"]}


INTEGRITY
---------
Duplicate Movie IDs:
{integrity["duplicate_movie_ids"]}

Missing Titles:
{integrity["missing_titles"]}

Missing Genres:
{integrity["missing_genres"]}

Invalid Categories:
{integrity["invalid_categories"]}

Special Overlap Violation:
{integrity["special_overlap_violation"]}

Integrity Passed:
{integrity["passed"]}


DIVERSITY
---------
Unique Movies:
{diversity["unique_movies"]}

Unique Genres:
{diversity["unique_genres"]}

Genre Distribution:
"""

    for genre, count in (
        diversity["genre_distribution"].items()
    ):
        report += (
            f"{genre}: {count}\n"
        )

    report += f"""

SCORES
------
Average Similarity:
{scores["average_similarity"]}

Average Estimated Rating:
{scores["average_estimated_rating"]}


CONTENT / COLLABORATIVE OVERLAP
--------------------------------
Shared Movies:
{overlap["shared_movies"]}

Content-Based Candidates:
{overlap["content_candidates"]}

Collaborative Candidates:
{overlap["collaborative_candidates"]}

Content-Based Overlap Rate:
{overlap["content_overlap_rate"]:.4f}

Collaborative Overlap Rate:
{overlap["collaborative_overlap_rate"]:.4f}
"""

    return report


def save_evaluation_report(
    report: str,
) -> None:

    HYBRID_REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        EVALUATION_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(report)

    print(
        "\nEvaluation report saved:"
    )

    print(EVALUATION_FILE)


def main():

    print("=" * 70)
    print("HYBRID RECOMMENDATION PIPELINE")
    print("=" * 70)

    # ------------------------------
    # 1. Load data
    # ------------------------------

    print("\nLoading datasets...")

    loader = DataLoader()

    movies = loader.load_movies()
    ratings = loader.load_ratings()

    print(
        f"Movies: {len(movies)}"
    )

    print(
        f"Ratings: {len(ratings)}"
    )

    # ------------------------------
    # 2. Content features
    # ------------------------------

    genre_matrix = (
        build_content_features(
            movies
        )
    )

    # ------------------------------
    # 3. Collaborative training
    # ------------------------------

    (
        collaborative_model,
        trainset,
    ) = train_collaborative_model(
        ratings
    )

    # ------------------------------
    # 4. Build recommenders
    # ------------------------------

    hybrid_recommender = (
        build_recommenders(
            movies=movies,
            ratings=ratings,
            collaborative_model=collaborative_model,
            trainset=trainset,
        )
    )

    # ------------------------------
    # 5. Hybrid recommendation
    # ------------------------------

    sections = (
        generate_hybrid_recommendations(
            hybrid_recommender,
            genre_matrix,
        )
    )

    # ------------------------------
    # 6. Combine output
    # ------------------------------

    recommendations = (
        combine_recommendations(
            sections
        )
    )

    # ------------------------------
    # 7. Save one CSV
    # ------------------------------

    save_recommendations(
        recommendations
    )

    # ------------------------------
    # 8. Evaluate
    # ------------------------------

    results = evaluate_hybrid(
        sections
    )

    # ------------------------------
    # 9. Build report
    # ------------------------------

    report = (
        build_evaluation_report(
            results
        )
    )

    # ------------------------------
    # 10. Save report
    # ------------------------------

    save_evaluation_report(
        report
    )

    # ------------------------------
    # Final summary
    # ------------------------------

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED")
    print("=" * 70)

    print(
        f"\nTotal recommendations: "
        f"{len(recommendations)}"
    )

    print(
        "\nRecommendation output:"
    )

    print(OUTPUT_FILE)

    print(
        "\nEvaluation report:"
    )

    print(EVALUATION_FILE)


if __name__ == "__main__":
    main()