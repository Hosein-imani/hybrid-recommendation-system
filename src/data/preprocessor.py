import pandas as pd


class DataPreprocessor:
    """
    Prepare datasets for recommendation models.
    """

    @staticmethod
    def extract_year(df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract release year from movie title.
        """
        movies = df.copy()

        movies["year"] = (
            movies["title"]
            .str.extract(r"\((\d{4})\)", expand=False)
        )

        return movies

    @staticmethod
    def clean_title(df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove release year from movie title.
        """
        movies = df.copy()

        movies["title"] = (
            movies["title"]
            .str.replace(r"\(\d{4}\)", "", regex=True)
            .str.strip()
        )

        return movies

    @staticmethod
    def split_genres(df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert genres string into a list.
        """
        movies = df.copy()

        movies["genres"] = movies["genres"].str.split("|")

        return movies

    @classmethod
    def preprocess_movies(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        Complete preprocessing pipeline for movies dataset.
        """

        movies = cls.extract_year(df)
        movies = cls.clean_title(movies)
        movies = cls.split_genres(movies)

        return movies

    @staticmethod
    def preprocess_ratings(df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove unnecessary columns from ratings dataset.
        """

        ratings = df.copy()

        if "timestamp" in ratings.columns:
            ratings = ratings.drop(columns=["timestamp"])

        return ratings