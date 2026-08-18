from pathlib import Path

from src.config.settings import (
    HYBRID_RECOMMENDATIONS_DIR,
    HYBRID_REPORTS_DIR,
)

from src.data.loader import DataLoader

from src.hybrid.evaluator import (
    HybridEvaluator,
)


INPUT_FILE = (
    HYBRID_RECOMMENDATIONS_DIR
    / "hybrid_recommendations.csv"
)

OUTPUT_FILE = (
    HYBRID_REPORTS_DIR
    / "hybrid_evaluation_report.txt"
)


def load_hybrid_output():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            "Hybrid recommendation output was not found:\n"
            f"{INPUT_FILE}\n\n"
            "Run run_hybrid.py first."
        )

    return INPUT_FILE


def build_sections(data):
    sections = {
        "special": data[
            data["category"] == "special"
        ].copy(),

        "content_based": data[
            data["category"] == "content_based"
        ].copy(),

        "collaborative": data[
            data["category"] == "collaborative"
        ].copy(),
    }

    return sections


def build_report(results):
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


def main():

    print("=" * 70)
    print("HYBRID EVALUATION")
    print("=" * 70)

    input_file = load_hybrid_output()

    print("\nLoading Hybrid output...")

    import pandas as pd

    recommendations = pd.read_csv(
        input_file
    )

    print(
        f"Recommendations loaded: "
        f"{len(recommendations)}"
    )

    print("\nBuilding evaluation sections...")

    sections = build_sections(
        recommendations
    )

    print("\nEvaluating Hybrid output...")

    evaluator = HybridEvaluator()

    results = evaluator.evaluate(
        sections
    )

    report = build_report(
        results
    )

    HYBRID_REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(report)

    print("\n" + "=" * 70)
    print("EVALUATION COMPLETED")
    print("=" * 70)

    print(
        "\nReport saved:"
    )

    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()