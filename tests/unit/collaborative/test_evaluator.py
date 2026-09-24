from types import SimpleNamespace

import pytest

from src.collaborative.evaluator import CollaborativeEvaluator


pytestmark = pytest.mark.unit


class StubEvaluationModel:
    def test(self, testset):
        assert testset == [(1, 2, 4.0)]
        return [
            (1, 2, 4.0, 3.0, {}),
            (2, 3, 2.0, 3.0, {}),
        ]


def test_evaluator_returns_rmse_mae_and_sample_count():
    results = CollaborativeEvaluator(StubEvaluationModel()).evaluate(
        [(1, 2, 4.0)]
    )

    assert results["RMSE"] == pytest.approx(1.0)
    assert results["MAE"] == pytest.approx(1.0)
    assert results["samples"] == 2
