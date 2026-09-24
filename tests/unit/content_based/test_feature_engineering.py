import pytest

from src.content_based.feature_engineering import FeatureEngineer


pytestmark = pytest.mark.unit


def test_build_genre_matrix_creates_binary_columns_and_preserves_metadata(
    processed_movies,
):
    matrix = FeatureEngineer.build_genre_matrix(processed_movies)

    assert list(matrix.columns[:4]) == ["movieId", "title", "genres", "year"]
    assert matrix.loc[matrix["movieId"] == 1, "Adventure"].item() == 1
    assert matrix.loc[matrix["movieId"] == 1, "Romance"].item() == 0
    assert matrix.loc[matrix["movieId"] == 3, "Romance"].item() == 1
    assert set(matrix["movieId"]) == set(processed_movies["movieId"])
