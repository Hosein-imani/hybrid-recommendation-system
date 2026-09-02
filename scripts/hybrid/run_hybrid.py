import pandas as pd

from src.collaborative.model import CollaborativeModel
from src.collaborative.recommender import CollaborativeRecommender

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

from src.data.loader import DataLoader
from src.data.preprocessor import DataPreprocessor

from src.hybrid.recommender import (
    HybridRecommender,
)


# ============================================================
# Configuration
# ============================================================

USER_ID = 5

SEED_MOVIE_TITLES = [
    "Jumanji",
    "Toy Story",
]

TOP_N_PER_MODEL = 10


# ============================================================
# Find Seed Movie IDs
# ============================================================

def get_seed_movie_ids(
    movies: pd.DataFrame,
) -> list[int]:

    movie_ids = []

    for movie_title in SEED_MOVIE_TITLES:

        search_title = movie_title.strip().lower()

        selected_movie = movies[
            movies["title"]
            .str.lower()
            .str.startswith(search_title)
        ]

        if selected_movie.empty:
            raise ValueError(
                f"Movie not found: {movie_title}"
            )

        movie_id = int(
            selected_movie["movieId"].iloc[0]
        )

        movie_ids.append(movie_id)

    return movie_ids


# ============================================================
# Generate Hybrid Recommendations
# ============================================================

def generate_hybrid_recommendations(
    hybrid_recommender,
    genre_matrix: pd.DataFrame,
    seed_movie_ids: list[int],
):

    print(
        "\nGenerating Hybrid recommendations..."
    )

    sections = hybrid_recommender.recommend(
        user_id=USER_ID,
        seed_movie_id=seed_movie_ids,
        genre_matrix=genre_matrix,
        top_n_per_model=TOP_N_PER_MODEL,
    )

    return sections


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 70)
    print("HYBRID RECOMMENDATION PIPELINE")
    print("=" * 70)

    # ========================================================
    # Load datasets
    # ========================================================

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

    # ========================================================
    # Find Seed Movies
    # ========================================================

    seed_movie_ids = get_seed_movie_ids(
        movies
    )

    print("\nSelected Seed Movies:")

    for movie_title, movie_id in zip(
        SEED_MOVIE_TITLES,
        seed_movie_ids,
    ):
        print(
            f"- {movie_title} "
            f"(ID: {movie_id})"
        )

    # ========================================================
    # Prepare Content-Based Features
    # ========================================================

    print(
        "\nPreparing Content-Based features..."
    )

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

    # ========================================================
    # Prepare Collaborative Model
    # ========================================================

    print(
        "\nPreparing Collaborative model..."
    )

    collaborative_model = CollaborativeModel()

    print(
        "\nPreparing collaborative dataset..."
    )

    collaborative_model.prepare_data(
        ratings
    )

    print(
        "\nTraining collaborative model..."
    )

    collaborative_model.train()

    # ========================================================
    # Initialize Recommenders
    # ========================================================

    print(
        "\nInitializing recommenders..."
    )

    content_recommender = (
        ContentBasedRecommender()
    )

    collaborative_recommender = (
        CollaborativeRecommender(
            model=collaborative_model.model,
            trainset=collaborative_model.trainset,
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

    # ========================================================
    # Generate Hybrid Recommendations
    # ========================================================

    sections = (
        generate_hybrid_recommendations(
            hybrid_recommender,
            genre_matrix,
            seed_movie_ids,
        )
    )

    special = sections["special"]

    content_based = sections[
        "content_based"
    ]

    collaborative = sections[
        "collaborative"
    ]

    # ========================================================
    # Combine Results
    # ========================================================

    combined = pd.concat(
        [
            special,
            content_based,
            collaborative,
        ],
        ignore_index=True,
    )

    # ========================================================
    # Create Output Directories
    # ========================================================

    HYBRID_RECOMMENDATIONS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    HYBRID_REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ========================================================
    # Output Paths
    # ========================================================

    special_path = (
        HYBRID_RECOMMENDATIONS_DIR
        / f"user_{USER_ID}_special_recommendations.csv"
    )

    content_path = (
        HYBRID_RECOMMENDATIONS_DIR
        / f"user_{USER_ID}_content_recommendations.csv"
    )

    collaborative_path = (
        HYBRID_RECOMMENDATIONS_DIR
        / f"user_{USER_ID}_collaborative_recommendations.csv"
    )

    combined_path = (
        HYBRID_RECOMMENDATIONS_DIR
        / f"user_{USER_ID}_all_recommendations.csv"
    )

    report_path = (
        HYBRID_REPORTS_DIR
        / f"user_{USER_ID}_hybrid_report.txt"
    )

    # ========================================================
    # Save Recommendations
    # ========================================================

    special.to_csv(
        special_path,
        index=False,
    )

    content_based.to_csv(
        content_path,
        index=False,
    )

    collaborative.to_csv(
        collaborative_path,
        index=False,
    )

    combined.to_csv(
        combined_path,
        index=False,
    )

    # ========================================================
    # Create Report
    # ========================================================

    report = f"""
HYBRID RECOMMENDATION REPORT
============================

User ID
-------
{USER_ID}

Seed Movies
-----------
{", ".join(SEED_MOVIE_TITLES)}

Seed Movie IDs
--------------
{", ".join(map(str, seed_movie_ids))}

Requested Per Model
-------------------
{TOP_N_PER_MODEL}

Special Recommendations
-----------------------
{len(special)}

Content-Based Only
------------------
{len(content_based)}

Collaborative Only
------------------
{len(collaborative)}

Total Recommendations
---------------------
{len(combined)}

Special Recommendation File
---------------------------
{special_path}

Content-Based Recommendation File
---------------------------------
{content_path}

Collaborative Recommendation File
---------------------------------
{collaborative_path}

Combined Recommendation File
----------------------------
{combined_path}
"""

    with open(
        report_path,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(report)

    # ========================================================
    # Print Results
    # ========================================================

    print("\n" + "=" * 70)
    print("SPECIAL RECOMMENDATIONS")
    print("Recommended by both models")
    print("=" * 70)

    if special.empty:

        print(
            "No shared recommendations were found."
        )

    else:

        print(special)

    print("\n" + "=" * 70)
    print("CONTENT-BASED RECOMMENDATIONS")
    print("=" * 70)

    if content_based.empty:

        print(
            "No Content-Based-only recommendations "
            "were found."
        )

    else:

        print(content_based)

    print("\n" + "=" * 70)
    print("COLLABORATIVE RECOMMENDATIONS")
    print("=" * 70)

    if collaborative.empty:

        print(
            "No Collaborative-only recommendations "
            "were found."
        )

    else:

        print(collaborative)

    # ========================================================
    # Summary
    # ========================================================

    print("\nSummary")
    print("-------")

    print(
        f"Special: {len(special)}"
    )

    print(
        f"Content-Based only: "
        f"{len(content_based)}"
    )

    print(
        f"Collaborative only: "
        f"{len(collaborative)}"
    )

    print(
        f"Total: {len(combined)}"
    )

    print(
        "\nCombined recommendation file saved:"
    )

    print(combined_path)

    print(
        "\nReport saved:"
    )

    print(report_path)


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()