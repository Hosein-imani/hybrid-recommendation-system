import pandas as pd
import pytest

from src.hybrid import evaluate_hybrid


pytestmark = pytest.mark.integration


def test_hybrid_evaluation_loads_csv_builds_sections_and_writes_report(
    tmp_path,
    monkeypatch,
):
    input_file = tmp_path / "hybrid_recommendations.csv"
    output_file = tmp_path / "reports" / "hybrid_evaluation_report.txt"
    pd.DataFrame(
        {
            "movieId": [1, 2, 3],
            "title": ["A", "B", "C"],
            "genres": ["Comedy|Drama", "Comedy", "Drama"],
            "category": ["special", "content_based", "collaborative"],
            "similarity": [0.9, 0.7, None],
            "estimated_rating": [4.5, None, 4.0],
        }
    ).to_csv(input_file, index=False)
    monkeypatch.setattr(evaluate_hybrid, "INPUT_FILE", input_file)
    monkeypatch.setattr(evaluate_hybrid, "OUTPUT_FILE", output_file)
    monkeypatch.setattr(evaluate_hybrid, "HYBRID_REPORTS_DIR", output_file.parent)

    evaluate_hybrid.main()

    assert output_file.exists()
    report = output_file.read_text(encoding="utf-8")
    assert "HYBRID EVALUATION REPORT" in report
    assert "Evaluation Status:        PASSED" in report
    assert "Total Unique Movies:      3" in report


def test_hybrid_evaluation_reports_missing_input_artifact(
    tmp_path,
    monkeypatch,
):
    missing_file = tmp_path / "missing.csv"
    monkeypatch.setattr(evaluate_hybrid, "INPUT_FILE", missing_file)

    with pytest.raises(FileNotFoundError, match="Run scripts/hybrid/run_hybrid.py first"):
        evaluate_hybrid._load_hybrid_output()
