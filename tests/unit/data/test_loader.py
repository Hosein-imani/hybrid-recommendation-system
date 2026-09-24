import pandas as pd
import pytest

from src.data.loader import DataLoader


pytestmark = pytest.mark.unit


def test_loader_reads_movies_and_ratings_from_configured_raw_directory(
    tmp_path,
    raw_movies,
    raw_ratings,
    monkeypatch,
):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    raw_movies.to_csv(raw_dir / "movies.csv", index=False)
    raw_ratings.to_csv(raw_dir / "ratings.csv", index=False)
    monkeypatch.setattr("src.data.loader.RAW_DATA_DIR", raw_dir)

    loader = DataLoader()

    pd.testing.assert_frame_equal(loader.load_movies(), raw_movies)
    pd.testing.assert_frame_equal(loader.load_ratings(), raw_ratings)


@pytest.mark.parametrize("method_name", ["load_movies", "load_ratings"])
def test_loader_reports_missing_input_file(tmp_path, monkeypatch, method_name):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    monkeypatch.setattr("src.data.loader.RAW_DATA_DIR", raw_dir)

    with pytest.raises(FileNotFoundError, match="File not found"):
        getattr(DataLoader(), method_name)()
