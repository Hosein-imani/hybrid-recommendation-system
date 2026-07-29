import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity


class SimilarityCalculator:
    """
    Compute movie similarities for Content-Based Recommendation.
    """

    @staticmethod
    def find_similar_movies(
        movie_id: int,
        genre_matrix: pd.DataFrame,
        top_n: int = 10,
    ) -> pd.DataFrame:

        # پیدا کردن اندیس فیلم
        movie_index = genre_matrix.index[
            genre_matrix["movieId"] == movie_id
        ]

        if len(movie_index) == 0:
            raise ValueError(f"Movie ID {movie_id} not found.")

        movie_index = movie_index[0]

        # فقط ستون‌های ویژگی
        features = genre_matrix.drop(
            columns=[
                "movieId",
                "title",
                "genres",
                "year",
            ]
        )

        # بردار فیلم انتخاب‌شده
        movie_vector = features.iloc[[movie_index]]

        # شباهت با تمام فیلم‌ها
        scores = cosine_similarity(
            movie_vector,
            features,
        ).flatten()

        similarity_df = genre_matrix[
            [
                "movieId",
                "title",
                "genres",
                "year",
            ]
        ].copy()

        similarity_df["similarity"] = scores

        similarity_df = similarity_df.sort_values(
            by="similarity",
            ascending=False,
        )

        # حذف خود فیلم
        similarity_df = similarity_df[
            similarity_df["movieId"] != movie_id
        ]

        return similarity_df.head(top_n)