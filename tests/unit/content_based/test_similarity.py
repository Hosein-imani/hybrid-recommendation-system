import pandas as pd
import pytest

from src.content_based.similarity import SimilarityCalculator


pytestmark = pytest.mark.unit


def test_similarity_excludes_seed_movies_and_returns_descending_top_n(
    genre_matrix,
):
    result = SimilarityCalculator.find_similar_movies(
        movie_id=1,
        genre_matrix=genre_matrix,
        top_n=3,
    )

    assert len(result) == 3
    assert 1 not in set(result["movieId"])
    assert result["similarity"].is_monotonic_decreasing
    assert result.iloc[0]["movieId"] == 8


def test_similarity_averages_multiple_seed_profiles_and_deduplicates_inputs(
    genre_matrix,
):
    single = SimilarityCalculator.find_similar_movies(
        movie_id=1,
        genre_matrix=genre_matrix,
        top_n=5,
    )
    duplicate_seed = SimilarityCalculator.find_similar_movies(
        movie_id=[1, 1],
        genre_matrix=genre_matrix,
        top_n=5,
    )
    multiple = SimilarityCalculator.find_similar_movies(
        movie_id=[1, 3],
        genre_matrix=genre_matrix,
        top_n=5,
    )

    pd.testing.assert_frame_equal(single.reset_index(drop=True), duplicate_seed.reset_index(drop=True))
    assert not {1, 3}.intersection(multiple["movieId"])
    assert multiple.iloc[0]["movieId"] == 8


@pytest.mark.parametrize(
    ("movie_id", "expected_error"),
    [
        ((1,), TypeError),
        ([], ValueError),
        ([999], ValueError),
        ([1, 999], ValueError),
    ],
)
def test_similarity_rejects_invalid_seed_requests(
    genre_matrix,
    movie_id,
    expected_error,
):
    with pytest.raises(expected_error):
        SimilarityCalculator.find_similar_movies(
            movie_id=movie_id,
            genre_matrix=genre_matrix,
        )
