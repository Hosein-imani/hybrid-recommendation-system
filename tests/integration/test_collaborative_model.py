import numpy as np
import pytest

from src.collaborative.model import CollaborativeModel


pytestmark = pytest.mark.integration


def test_small_ratings_dataset_can_be_prepared_trained_and_persisted(
    raw_movies,
    raw_ratings,
    tmp_path,
    monkeypatch,
):
    import src.collaborative.model as model_module

    model_directory = tmp_path / "models"
    monkeypatch.setattr(model_module, "COLLABORATIVE_MODELS_DIR", model_directory)

    model = CollaborativeModel(n_factors=2, epochs=5)
    trainset, testset = model.prepare_data(raw_ratings)

    assert len(list(trainset.all_ratings())) + len(testset) == len(raw_ratings)

    model.train()
    prediction = model.predict(user_id=1, movie_id=3)
    assert np.isfinite(prediction)

    metadata = model.get_metadata(raw_ratings, raw_movies)
    assert metadata == {
        "algorithm": "Surprise SVD",
        "n_factors": 2,
        "learning_rate": 0.005,
        "regularization": 0.02,
        "epochs": 5,
        "ratings": len(raw_ratings),
        "movies": len(raw_movies),
        "users": raw_ratings["userId"].nunique(),
    }

    saved = model.save()
    assert saved["model_path"].exists()
    assert saved["trainset_path"].exists()

    loaded = CollaborativeModel(n_factors=2, epochs=5)
    loaded.load()
    assert loaded.trainset is not None
    assert loaded.predict(user_id=1, movie_id=3) == pytest.approx(prediction)


def test_training_requires_prepared_data():
    with pytest.raises(ValueError, match="Dataset is not prepared"):
        CollaborativeModel(n_factors=2, epochs=1).train()
