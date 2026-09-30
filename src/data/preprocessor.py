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
        if "genres" not in df.columns:
            raise ValueError("Movies dataset must contain a 'genres' column.")

        missing_mask = df["genres"].isna()
        if missing_mask.any():
            idx = missing_mask[missing_mask].index[0]
            row = df.loc[idx]
            identifiers = [f"row={idx}"]
            if "movieId" in df.columns and pd.notna(row["movieId"]):
                identifiers.append(f"movieId={row['movieId']}")
            if "title" in df.columns and pd.notna(row["title"]):
                identifiers.append(f"title={row['title']!r}")
            raise ValueError(
                f"Missing genre value for movie ({', '.join(identifiers)})."
            )

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