import pandas as pd
import pytest

from src.content_based.feature_engineering import FeatureEngineer
from src.data.preprocessor import DataPreprocessor


@pytest.fixture
def raw_movies() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "movieId": [1, 2, 3, 4, 5, 6, 7, 8],
            "title": [
                "Toy Story (1995)",
                "Jumanji (1995)",
                "Grumpier Old Men (1995)",
                "Waiting to Exhale (1995)",
                "Father of the Bride Part II (1995)",
                "Heat (1995)",
                "Casino (1995)",
                "Toy Story 2 (1999)",
            ],
            "genres": [
                "Adventure|Animation|Children|Comedy|Fantasy",
                "Adventure|Children|Fantasy",
                "Comedy|Romance",
                "Comedy|Drama|Romance",
                "Comedy",
                "Action|Crime|Thriller",
                "Crime|Drama",
                "Adventure|Animation|Children|Comedy|Fantasy",
            ],
        }
    )


@pytest.fixture
def raw_ratings() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "userId": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
            "movieId": [1, 2, 6, 2, 3, 7, 1, 4, 8, 3, 5, 6],
            "rating": [4.5, 3.5, 5.0, 4.0, 3.0, 4.5, 5.0, 4.0, 4.5, 3.0, 4.0, 5.0],
            "timestamp": [
                1000000000,
                1000000001,
                1000000002,
                1000000003,
                1000000004,
                1000000005,
                1000000006,
                1000000007,
                1000000008,
                1000000009,
                1000000010,
                1000000011,
            ],
        }
    )


@pytest.fixture
def processed_movies(raw_movies: pd.DataFrame) -> pd.DataFrame:
    return DataPreprocessor.preprocess_movies(raw_movies)


@pytest.fixture
def genre_matrix(processed_movies: pd.DataFrame) -> pd.DataFrame:
    return FeatureEngineer.build_genre_matrix(processed_movies)
