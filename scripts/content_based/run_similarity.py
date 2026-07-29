from src.config.settings import (
    CONTENT_SIMILARITY_REPORTS_DIR,
    CONTENT_SIMILARITY_ARTIFACTS_DIR,
)

from src.data.loader import DataLoader
from src.data.preprocessor import DataPreprocessor

from src.content_based.feature_engineering import FeatureEngineer
from src.content_based.similarity import SimilarityCalculator


REPORT_FILE = (
    CONTENT_SIMILARITY_REPORTS_DIR /
    "similarity_report.txt"
)

OUTPUT_FILE = (
    CONTENT_SIMILARITY_ARTIFACTS_DIR /
    "top_similar_movies.csv"
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

    similarity = SimilarityCalculator()

    recommendations = similarity.find_similar_movies(
        movie_id=MOVIE_ID,
        genre_matrix=genre_matrix,
        top_n=TOP_N,
    )

    CONTENT_SIMILARITY_REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    CONTENT_SIMILARITY_ARTIFACTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    recommendations.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    movie_title = genre_matrix.loc[
        genre_matrix["movieId"] == MOVIE_ID,
        "title"
    ].iloc[0]

    report = f"""
==================================================
CONTENT-BASED SIMILARITY REPORT
==================================================

Query Movie
-----------
Movie ID : {MOVIE_ID}
Title    : {movie_title}

Similarity Metric
-----------------
Cosine Similarity

Top Recommendations
-------------------
{TOP_N}

Output File
-----------
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
        f"\nSimilarity report saved to:\n{REPORT_FILE}"
    )


if __name__ == "__main__":
    main()