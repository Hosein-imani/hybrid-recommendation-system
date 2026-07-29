from src.config.settings import DATASET_REPORTS_DIR

from src.data.loader import DataLoader
from src.data.validator import DataValidator


OUTPUT_FILE = DATASET_REPORTS_DIR / "validation_report.txt"


def main():

    loader = DataLoader()

    movies = loader.load_movies()
    ratings = loader.load_ratings()

    validator = DataValidator()

    movies_report = validator.dataset_info(
        movies,
        "Movies"
    )

    ratings_report = validator.dataset_info(
        ratings,
        "Ratings"
    )

    DATASET_REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    report = (
        "DATA VALIDATION REPORT\n"
        + "=" * 60
        + "\n\n"
        + movies_report
        + "\n\n"
        + ratings_report
    )

    print(report)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"\nValidation report saved to:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()