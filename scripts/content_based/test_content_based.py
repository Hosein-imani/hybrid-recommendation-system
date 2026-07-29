from src.config.settings import (
    CONTENT_RECOMMENDER_RECOMMENDATIONS_DIR,
)

from src.data.loader import DataLoader
from src.data.preprocessor import DataPreprocessor

from src.content_based.feature_engineering import FeatureEngineer
from src.content_based.recommender import ContentBasedRecommender


# ================================
# Test Configuration
# ================================


# ================================
# chose movie name from the dataset 
# and drop in the MOVIE_TITLE variable below
# ================================
MOVIE_TITLE = "Jumanji"
TOP_N = 10
# ================================




OUTPUT_FILE = (
    CONTENT_RECOMMENDER_RECOMMENDATIONS_DIR
    / "test_recommendations.csv"
)


def main():

    print("=" * 50)
    print("CONTENT BASED RECOMMENDATION TEST")
    print("=" * 50)


    # -------------------------------
    # Load Dataset
    # -------------------------------

    loader = DataLoader()

    movies = loader.load_movies()


    # -------------------------------
    # Preprocessing
    # -------------------------------

    preprocessor = DataPreprocessor()

    movies = preprocessor.preprocess_movies(
        movies
    )


    # -------------------------------
    # Feature Engineering
    # -------------------------------

    feature_engineer = FeatureEngineer()

    genre_matrix = (
        feature_engineer.build_genre_matrix(
            movies
        )
    )


    # -------------------------------
    # Find Movie
    # -------------------------------

    selected_movie = genre_matrix[
        genre_matrix["title"] == MOVIE_TITLE
    ]


    if selected_movie.empty:

        raise ValueError(
            f"Movie not found: {MOVIE_TITLE}"
        )


    movie_id = (
        selected_movie["movieId"]
        .iloc[0]
    )


    print(
        f"\nSelected Movie: {MOVIE_TITLE}"
    )


    # -------------------------------
    # Recommendation
    # -------------------------------

    recommender = ContentBasedRecommender()


    recommendations = recommender.recommend(
        movie_id=movie_id,
        genre_matrix=genre_matrix,
        top_n=TOP_N,
    )


    # -------------------------------
    # Save Output
    # -------------------------------

    CONTENT_RECOMMENDER_RECOMMENDATIONS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    recommendations.to_csv(
        OUTPUT_FILE,
        index=False,
    )


    print("\nTop Recommendations:")
    print("-" * 50)

    print(recommendations)


    print("\nOutput saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()