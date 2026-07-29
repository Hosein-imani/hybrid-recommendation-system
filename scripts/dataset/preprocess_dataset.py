from src.config.settings import DATASET_REPORTS_DIR

from src.data.loader import DataLoader
from src.data.preprocessor import DataPreprocessor


OUTPUT_FILE = DATASET_REPORTS_DIR / "preprocessing_report.txt"


def main():

    loader = DataLoader()

    movies = loader.load_movies()

    preprocessor = DataPreprocessor()

    # قبل از پردازش
    original_title = movies.loc[0, "title"]
    original_genres = movies.loc[0, "genres"]

    # پردازش
    movies = preprocessor.extract_year(movies)
    movies = preprocessor.clean_title(movies)
    movies = preprocessor.split_genres(movies)

    # بعد از پردازش
    processed_title = movies.loc[0, "title"]
    processed_year = movies.loc[0, "year"]
    processed_genres = movies.loc[0, "genres"]

    DATASET_REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    report = f"""
==================================================
PREPROCESSING REPORT
==================================================

Extract Year
----------------------------------------

Before:
{original_title}

After:
Title : {processed_title}
Year  : {processed_year}

==================================================

Split Genres
----------------------------------------

Before:
{original_genres}

After:
{processed_genres}

==================================================

Dataset Shape

Rows    : {movies.shape[0]}
Columns : {movies.shape[1]}

Columns

{movies.columns.tolist()}
"""

    print(report)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"\nPreprocessing report saved to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()