import pandas as pd
import pytest

from src.data.preprocessor import DataPreprocessor


pytestmark = pytest.mark.unit


def test_preprocess_movies_extracts_year_cleans_title_and_splits_genres(
    raw_movies,
):
    original = raw_movies.copy(deep=True)

    processed = DataPreprocessor.preprocess_movies(raw_movies)

    assert processed.loc[0, "title"] == "Toy Story"
    assert processed.loc[0, "year"] == "1995"
    assert processed.loc[0, "genres"] == [
        "Adventure",
        "Animation",
        "Children",
        "Comedy",
        "Fantasy",
    ]
    pd.testing.assert_frame_equal(raw_movies, original)


def test_extract_year_preserves_missing_year_as_missing_value():
    movies = pd.DataFrame(
        {
            "movieId": [1, 2],
            "title": ["Known Title (2001)", "Untitled"],
            "genres": ["Drama", "Comedy"],
        }
    )

    processed = DataPreprocessor.extract_year(movies)

    assert processed.loc[0, "year"] == "2001"
    assert pd.isna(processed.loc[1, "year"])


def test_preprocess_ratings_removes_timestamp_without_mutating_input(raw_ratings):
    original = raw_ratings.copy(deep=True)

    processed = DataPreprocessor.preprocess_ratings(raw_ratings)

    assert list(processed.columns) == ["userId", "movieId", "rating"]
    pd.testing.assert_frame_equal(raw_ratings, original)


def test_preprocess_ratings_accepts_already_prepared_frame(raw_ratings):
    prepared = raw_ratings.drop(columns="timestamp")

    result = DataPreprocessor.preprocess_ratings(prepared)

    pd.testing.assert_frame_equal(result, prepared)
