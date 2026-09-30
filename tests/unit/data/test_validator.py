import numpy as np
import pandas as pd
import pytest

from src.data.validator import DataValidator


pytestmark = pytest.mark.unit


def test_dataset_info_reports_shape_types_missing_values_and_duplicates():
    data = pd.DataFrame(
        {
            "movieId": [1, 1, 2],
            "title": ["A", "A", np.nan],
        }
    )

    report = DataValidator.dataset_info(data, "Movies")

    assert "missing-marker" in report
    assert "Rows: 3" in report
    assert "Columns: 2" in report
    assert "Missing Values:" in report
    assert "title" in report
    assert "1" in report.split("Missing Values:", 1)[1]
    assert "Duplicate Rows: 1" in report
