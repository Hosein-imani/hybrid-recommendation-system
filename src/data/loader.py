import pandas as pd

from src.config.settings import RAW_DATA_DIR


class DataLoader:
    """
    Responsible for loading datasets into pandas DataFrames.
    """

    def __init__(self):
        self.raw_data_path = RAW_DATA_DIR

    def load_movies(self) -> pd.DataFrame:
        movies_path = self.raw_data_path / "movies.csv"

        if not movies_path.exists():
            raise FileNotFoundError(f"File not found: {movies_path}")

        return pd.read_csv(movies_path)

    def load_ratings(self) -> pd.DataFrame:
        ratings_path = self.raw_data_path / "ratings.csv"

        if not ratings_path.exists():
            raise FileNotFoundError(f"File not found: {ratings_path}")

        return pd.read_csv(ratings_path)