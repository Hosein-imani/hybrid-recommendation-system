from types import SimpleNamespace

import pandas as pd
import pytest

from src.collaborative.recommender import CollaborativeRecommender


pytestmark = pytest.mark.unit


class StubTrainset:
    def __init__(self, rated_by_user):
        self.rated_by_user = rated_by_user
        self.ur = {7: [(101, 4.0), (102, 3.0)]}

    def to_inner_uid(self, user_id):
        if user_id not in self.rated_by_user:
            raise ValueError("unknown user")
        return 7

    def to_raw_iid(self, inner_movie_id):
        return {101: 1, 102: 2}[inner_movie_id]


class StubModel:
    estimates = {1: 4.2, 2: 4.1, 3: 2.5, 4: 4.8, 5: 3.7}

    def __init__(self):
        self.calls = []

    def predict(self, uid, iid):
        self.calls.append((uid, iid))
        return SimpleNamespace(est=self.estimates[iid])


@pytest.fixture
def collaborative_movies():
    return pd.DataFrame(
        {
            "movieId": [1, 2, 3, 4, 5],
            "title": ["A", "B", "C", "D", "E"],
            "genres": ["Drama", "Comedy", "Action", "Drama", "Crime"],
        }
    )


def test_recommender_excludes_rated_movies_sorts_predictions_and_attaches_metadata(
    collaborative_movies,
):
    model = StubModel()
    recommender = CollaborativeRecommender(
        model=model,
        trainset=StubTrainset({7}),
        movies=collaborative_movies,
    )

    result = recommender.recommend(user_id=7, n_recommendations=2)

    assert result["movieId"].tolist() == [4, 5]
    assert result["title"].tolist() == ["D", "E"]
    assert result["estimated_rating"].tolist() == [4.8, 3.7]
    assert {movie_id for _, movie_id in model.calls} == {3, 4, 5}


def test_recommender_treats_unknown_user_as_having_no_rated_movies(
    collaborative_movies,
):
    model = StubModel()
    recommender = CollaborativeRecommender(
        model=model,
        trainset=StubTrainset(set()),
        movies=collaborative_movies,
    )

    result = recommender.recommend(user_id=99, n_recommendations=10)

    assert result["movieId"].tolist() == [4, 1, 2, 5, 3]


@pytest.mark.parametrize(
    "n_recommendations",
    [0, -1, True, False, 1.5, "3"],
)
def test_recommender_rejects_invalid_n_recommendations(
    collaborative_movies,
    n_recommendations,
):
    recommender = CollaborativeRecommender(
        model=StubModel(),
        trainset=StubTrainset({7}),
        movies=collaborative_movies,
    )

    with pytest.raises(ValueError, match="n_recommendations"):
        recommender.recommend(
            user_id=7,
            n_recommendations=n_recommendations,
        )


def test_recommender_accepts_valid_positive_n_recommendations(
    collaborative_movies,
):
    recommender = CollaborativeRecommender(
        model=StubModel(),
        trainset=StubTrainset({7}),
        movies=collaborative_movies,
    )

    result = recommender.recommend(user_id=7, n_recommendations=1)

    assert result["movieId"].tolist() == [4]
