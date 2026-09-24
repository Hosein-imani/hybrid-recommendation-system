import pandas as pd
import pytest

from scripts.hybrid import run_hybrid
from src.collaborative.model import CollaborativeModel
from src.collaborative.recommender import CollaborativeRecommender
from src.content_based.feature_engineering import FeatureEngineer
from src.content_based.recommender import ContentBasedRecommender
from src.data.preprocessor import DataPreprocessor
from src.hybrid.evaluator import HybridEvaluator
from src.hybrid.recommender import HybridRecommender


pytestmark = pytest.mark.e2e


def test_small_real_workflow_writes_evaluable_hybrid_artifact(
    raw_movies,
    raw_ratings,
    tmp_path,
):
    seed_movie_ids = run_hybrid.get_seed_movie_ids(raw_movies)
    processed_movies = DataPreprocessor.preprocess_movies(raw_movies)
    genre_matrix = FeatureEngineer.build_genre_matrix(processed_movies)

    collaborative_model = CollaborativeModel(n_factors=2, epochs=5)
    collaborative_model.prepare_data(raw_ratings)
    collaborative_model.train()

    hybrid = HybridRecommender(
        content_recommender=ContentBasedRecommender(),
        collaborative_recommender=CollaborativeRecommender(
            model=collaborative_model.model,
            trainset=collaborative_model.trainset,
            movies=raw_movies,
        ),
        movies=raw_movies,
        ratings=raw_ratings,
    )

    sections = hybrid.recommend(
        user_id=1,
        seed_movie_id=seed_movie_ids,
        genre_matrix=genre_matrix,
        top_n_per_model=3,
        special_candidate_pool_size=5,
        special_top_n=2,
    )
    combined = pd.concat(sections.values(), ignore_index=True)

    output_file = tmp_path / "hybrid_recommendations.csv"
    combined.to_csv(output_file, index=False)
    loaded = pd.read_csv(output_file)
    loaded_sections = {
        category: loaded[loaded["category"] == category].copy()
        for category in ("special", "content_based", "collaborative")
    }
    results = HybridEvaluator().evaluate(loaded_sections)

    assert output_file.exists()
    assert set(loaded.columns) == set(HybridRecommender.OUTPUT_COLUMNS)
    assert loaded["movieId"].is_unique
    assert not {1, 2, 6}.intersection(loaded["movieId"])
    assert results["integrity"]["passed"] is True
    assert results["counts"]["total_unique"] == len(loaded)
