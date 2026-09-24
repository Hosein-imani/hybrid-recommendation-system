import pytest

from scripts.hybrid import run_hybrid


pytestmark = pytest.mark.integration


def test_seed_title_helper_resolves_configured_titles_case_insensitively(
    raw_movies,
):
    assert run_hybrid.get_seed_movie_ids(raw_movies) == [2, 1]


def test_seed_title_helper_reports_unknown_title(raw_movies, monkeypatch):
    monkeypatch.setattr(run_hybrid, "SEED_MOVIE_TITLES", ["Unknown Movie"])

    with pytest.raises(ValueError, match="Movie not found: Unknown Movie"):
        run_hybrid.get_seed_movie_ids(raw_movies)


def test_clear_previous_outputs_removes_only_configured_artifact_patterns(
    tmp_path,
    monkeypatch,
):
    recommendations = tmp_path / "recommendations"
    reports = tmp_path / "reports"
    recommendations.mkdir()
    reports.mkdir()
    removable = [
        recommendations / "special_recommendations.csv",
        recommendations / "hybrid_recommendations.csv",
        reports / "hybrid_report.txt",
    ]
    retained = recommendations / "keep.csv"
    for path in removable + [retained]:
        path.write_text("artifact", encoding="utf-8")
    monkeypatch.setattr(run_hybrid, "HYBRID_RECOMMENDATIONS_DIR", recommendations)
    monkeypatch.setattr(run_hybrid, "HYBRID_REPORTS_DIR", reports)

    removed = run_hybrid.clear_previous_outputs()

    assert set(removed) == set(removable)
    assert all(not path.exists() for path in removable)
    assert retained.exists()
