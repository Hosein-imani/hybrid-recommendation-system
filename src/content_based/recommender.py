import pandas as pd

from src.content_based.similarity import SimilarityCalculator


class ContentBasedRecommender:
    """
    Content-Based Recommendation System.
    """

    def __init__(self):

        self.similarity_calculator = (
            SimilarityCalculator()
        )

    def recommend(
        self,
        movie_id: int | list[int],
        genre_matrix: pd.DataFrame,
        top_n: int = 10,
    ) -> pd.DataFrame:

        recommendations = (
            self.similarity_calculator.find_similar_movies(
                movie_id=movie_id,
                genre_matrix=genre_matrix,
                top_n=top_n,
            )
        )

        return recommendations