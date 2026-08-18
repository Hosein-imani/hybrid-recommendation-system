import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

import pandas as pd

from src.config.settings import (
    HYBRID_RECOMMENDATIONS_DIR,
    HYBRID_REPORTS_DIR,
)
from src.hybrid.evaluator import HybridEvaluator


USER_ID = 5


def _load_recommendations(
    filename: str,
) -> pd.DataFrame:
    path = HYBRID_RECOMMENDATIONS_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Recommendation file was not found:\n{path}\n\n"
            "Run scripts/hybrid/run_hybrid.py first."
        )

    return pd.read_csv(path)


def _format_value(value):
    if value is None:
        return "N/A"

    if isinstance(value, float):
        return f"{value:.4f}"

    return str(value)


def _build_report(
    results: dict,
) -> str:
    counts = results["counts"]
    overlap = results["overlap"]
    scores = results["scores"]
    diversity = results["diversity"]
    integrity = results["integrity"]

    lines = [
        "=" * 60,
        "HYBRID EVALUATION REPORT",
        "=" * 60,
        "",
        "Recommendation Counts",
        "-" * 60,
        f"Special Recommendations: {counts['special']}",
        f"Content-Based Only:       {counts['content_based']}",
        f"Collaborative Only:       {counts['collaborative']}",
        f"Total Unique Movies:      {counts['total_unique']}",
        f"Total Recommendation Rows:{counts['total_rows']}",
        "",
        "Overlap Analysis",
        "-" * 60,
        f"Shared Movies:             {overlap['shared_movies']}",
        f"Content Candidates:        {overlap['content_candidates']}",
        f"Collaborative Candidates:  {overlap['collaborative_candidates']}",
        (
            "Content Overlap Rate:      "
            f"{_format_value(overlap['content_overlap_rate'])}"
        ),
        (
            "Collaborative Overlap Rate:"
            f" {_format_value(overlap['collaborative_overlap_rate'])}"
        ),
        "",
        "Recommendation Scores",
        "-" * 60,
        (
            "Average Content Similarity: "
            f"{_format_value(scores['average_similarity'])}"
        ),
        (
            "Average Estimated Rating:   "
            f"{_format_value(scores['average_estimated_rating'])}"
        ),
        "",
        "Diversity",
        "-" * 60,
        f"Unique Movies:             {diversity['unique_movies']}",
        f"Unique Genres:             {diversity['unique_genres']}",
        "",
        "Genre Distribution",
        "-" * 60,
    ]

    if diversity["genre_distribution"]:
        for genre, count in diversity["genre_distribution"].items():
            lines.append(f"{genre}: {count}")
    else:
        lines.append("No genres found.")

    lines.extend(
        [
            "",
            "Integrity Checks",
            "-" * 60,
            (
                "Duplicate Movie IDs:      "
                f"{integrity['duplicate_movie_ids']}"
            ),
            (
                "Missing Titles:           "
                f"{integrity['missing_titles']}"
            ),
            (
                "Missing Genres:           "
                f"{integrity['missing_genres']}"
            ),
            (
                "Invalid Categories:       "
                f"{integrity['invalid_categories'] or 'None'}"
            ),
            (
                "Special Overlap Violation:"
                f" {integrity['special_overlap_violation']}"
            ),
            "",
            (
                "Evaluation Status:        "
                f"{'PASSED' if integrity['passed'] else 'FAILED'}"
            ),
            "",
            "=" * 60,
        ]
    )

    return "\n".join(lines)


def main():
    print("=" * 60)
    print("HYBRID EVALUATION")
    print("=" * 60)

    print("\nLoading Hybrid recommendation output...")

    special = _load_recommendations(
        f"user_{USER_ID}_special_recommendations.csv"
    )

    content_based = _load_recommendations(
        f"user_{USER_ID}_content_recommendations.csv"
    )

    collaborative = _load_recommendations(
        f"user_{USER_ID}_collaborative_recommendations.csv"
    )

    sections = {
        "special": special,
        "content_based": content_based,
        "collaborative": collaborative,
    }

    print("Running HybridEvaluator...")

    evaluator = HybridEvaluator()

    results = evaluator.evaluate(
        sections
    )

    report = _build_report(
        results
    )

    HYBRID_REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path = (
        HYBRID_REPORTS_DIR
        / f"user_{USER_ID}_hybrid_evaluation_report.txt"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(report)

    print("\n" + report)

    print("\nEvaluation report saved:")
    print(report_path)


if __name__ == "__main__":
    main()
