from src.config.settings import (
    CONTENT_FEATURE_ENGINEERING_REPORTS_DIR,
    CONTENT_FEATURE_ENGINEERING_ARTIFACTS_DIR,
)

from src.data.loader import DataLoader
from src.data.preprocessor import DataPreprocessor
from src.content_based.feature_engineering import FeatureEngineer


REPORT_FILE = CONTENT_FEATURE_ENGINEERING_REPORTS_DIR / "feature_engineering_report.txt"
GENRE_MATRIX_FILE = CONTENT_FEATURE_ENGINEERING_ARTIFACTS_DIR / "genre_matrix.csv"


def main():

    loader = DataLoader()

    movies = loader.load_movies()

    preprocessor = DataPreprocessor()

    movies = preprocessor.preprocess_movies(movies)

    feature_engineer = FeatureEngineer()

    genre_matrix = feature_engineer.build_genre_matrix(movies)

    CONTENT_FEATURE_ENGINEERING_REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    CONTENT_FEATURE_ENGINEERING_ARTIFACTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    genre_matrix.to_csv(
        GENRE_MATRIX_FILE,
        index=False,
    )

    report = f"""
==================================================
CONTENT-BASED FEATURE ENGINEERING REPORT
==================================================

Input Dataset
-------------
Rows    : {movies.shape[0]}
Columns : {movies.shape[1]}

Output Dataset
--------------
Rows    : {genre_matrix.shape[0]}
Columns : {genre_matrix.shape[1]}

Generated Genre Columns
-----------------------
{genre_matrix.columns[4:].tolist()}

Genre Matrix File
-----------------
{GENRE_MATRIX_FILE}
"""

    print(report)

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"\nReport saved to:\n{REPORT_FILE}")


if __name__ == "__main__":
    main()