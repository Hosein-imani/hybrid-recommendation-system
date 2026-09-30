import pandas as pd
import pytest

from src.content_based.feature_engineering import FeatureEngineer


pytestmark = pytest.mark.unit


def test_build_genre_matrix_creates_binary_columns_and_preserves_metadata(
    processed_movies,
):
    original = processed_movies.copy(deep=True)

    matrix = FeatureEngineer.build_genre_matrix(processed_movies)

    assert list(matrix.columns[:4]) == ["movieId", "title", "genres", "year"]
    assert matrix.loc[matrix["movieId"] == 1, "Adventure"].item() == 1
    assert matrix.loc[matrix["movieId"] == 1, "Romance"].item() == 0
    assert matrix.loc[matrix["movieId"] == 3, "Romance"].item() == 1
    assert set(matrix["movieId"]) == set(processed_movies["movieId"])
    pd.testing.assert_frame_equal(processed_movies, original)


@pytest.mark.parametrize("missing_value", [None, float("nan"), pd.NA, [], [None]])
def test_build_genre_matrix_raises_clear_error_for_missing_genre_and_preserves_input(
    processed_movies,
    missing_value,
):
    movies = processed_movies.copy(deep=True)
    movies.at[1, "genres"] = missing_value
    original = movies.copy(deep=True)

    with pytest.raises(
        ValueError,
        match=r"Missing genre value for movie .*row=1.*movieId=2.*title='Jumanji'",
    ):
        FeatureEngineer.build_genre_matrix(movies)

    pd.testing.assert_frame_equal(movies, original)


def test_build_genre_matrix_identifies_row_when_movie_metadata_columns_unavailable():
    movies = pd.DataFrame(
        {
            "genres": [["Drama"], None],
        },
        index=[10, 20],
    )
    original = movies.copy(deep=True)

    with pytest.raises(
        ValueError,
        match=r"Missing genre value for movie \(row=20\)\.",
    ):
        FeatureEngineer.build_genre_matrix(movies)

    pd.testing.assert_frame_equal(movies, original)

