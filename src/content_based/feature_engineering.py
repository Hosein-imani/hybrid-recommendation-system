import pandas as pd


class FeatureEngineer:
    """
    Create features for recommendation models.
    """

    @staticmethod
    def _is_missing_genres(genres: object) -> bool:
        if genres is None or isinstance(genres, (float, int, bool)):
            return True
        if isinstance(genres, str):
            return not genres.strip()
        if isinstance(genres, (list, tuple, set)):
            if len(genres) == 0:
                return True
            return any(
                g is None or pd.isna(g) or (isinstance(g, str) and not g.strip())
                for g in genres
            )
        try:
            if pd.isna(genres):
                return True
        except (TypeError, ValueError):
            pass
        return not hasattr(genres, "__iter__")

    @classmethod
    def _validate_genres(cls, movies: pd.DataFrame) -> None:
        if "genres" not in movies.columns:
            raise ValueError("Movies dataset must contain a 'genres' column.")

        for idx, row in movies.iterrows():
            if cls._is_missing_genres(row["genres"]):
                identifiers = [f"row={idx}"]
                if "movieId" in movies.columns and pd.notna(row["movieId"]):
                    identifiers.append(f"movieId={row['movieId']}")
                if "title" in movies.columns and pd.notna(row["title"]):
                    identifiers.append(f"title={row['title']!r}")
                raise ValueError(
                    f"Missing genre value for movie ({', '.join(identifiers)})."
                )

    @classmethod
    def build_genre_matrix(cls, movies: pd.DataFrame) -> pd.DataFrame:
        cls._validate_genres(movies)

        movies_with_genres = movies.copy()

        for _, row in movies.iterrows():
            genres = (
                row["genres"].split("|")
                if isinstance(row["genres"], str)
                else row["genres"]
            )
            for genre in genres:
                movies_with_genres.at[row.name, genre] = 1

        movies_with_genres = movies_with_genres.fillna(0)

        return movies_with_genres