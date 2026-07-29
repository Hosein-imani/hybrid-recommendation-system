from src.config.settings import (
    CONTENT_RECOMMENDER_REPORTS_DIR,
    CONTENT_RECOMMENDER_RECOMMENDATIONS_DIR,
)

from src.data.loader import DataLoader
from src.data.preprocessor import DataPreprocessor

from src.content_based.feature_engineering import FeatureEngineer
from src.content_based.recommender import (
    ContentBasedRecommender,
)


REPORT_FILE = (
    CONTENT_RECOMMENDER_REPORTS_DIR /
    "recommendation_report.txt"
)

OUTPUT_FILE = (
    CONTENT_RECOMMENDER_RECOMMENDATIONS_DIR /
    "recommendations.csv"
)


MOVIE_ID = 1
TOP_N = 10


def main():

    loader = DataLoader()

    movies = loader.load_movies()

    preprocessor = DataPreprocessor()

    movies = preprocessor.preprocess_movies(movies)

    feature_engineer = FeatureEngineer()

    genre_matrix = feature_engineer.build_genre_matrix(
        movies
    )

    recommender = ContentBasedRecommender()

    recommendations = recommender.recommend(
        movie_id=MOVIE_ID,
        genre_matrix=genre_matrix,
        top_n=TOP_N,
    )

    CONTENT_RECOMMENDER_REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    CONTENT_RECOMMENDER_RECOMMENDATIONS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    recommendations.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    movie_title = genre_matrix.loc[
        genre_matrix["movieId"] == MOVIE_ID,
        "title",
    ].iloc[0]

    report = f"""
==================================================
CONTENT-BASED RECOMMENDATION REPORT
==================================================

Movie ID
--------
{MOVIE_ID}

Movie Title
-----------
{movie_title}

Number of Recommendations
-------------------------
{TOP_N}

Recommendation File
-------------------
{OUTPUT_FILE}
"""

    print(report)

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(report)

    print(recommendations)

    print(
        f"\nRecommendation report saved to:\n{REPORT_FILE}"
    )


if __name__ == "__main__":
    main()