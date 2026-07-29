import pandas as pd


class FeatureEngineer:
    """
    Create features for recommendation models.
    """

    @staticmethod
    def build_genre_matrix(movies: pd.DataFrame) -> pd.DataFrame:
        movies_with_genres = movies.copy()

        for _, row in movies.iterrows():
            for genre in row["genres"]:
                movies_with_genres.at[row.name, genre] = 1

        movies_with_genres = movies_with_genres.fillna(0)

        return movies_with_genres