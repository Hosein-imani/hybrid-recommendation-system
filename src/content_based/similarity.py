import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity


class SimilarityCalculator:
    """
    Compute movie similarities for Content-Based Recommendation.
    """

    @staticmethod
    def find_similar_movies(
        movie_id: int | list[int],
        genre_matrix: pd.DataFrame,
        top_n: int = 10,
    ) -> pd.DataFrame:

        # -----------------------------------------
        # Normalize input
        # -----------------------------------------

        if isinstance(movie_id, int):
            movie_ids = [movie_id]

        elif isinstance(movie_id, list):
            movie_ids = movie_id

        else:
            raise TypeError(
                "movie_id must be an int "
                "or list[int]."
            )

        if not movie_ids:
            raise ValueError(
                "At least one movie ID is required."
            )

        # Remove duplicate IDs while
        # preserving input order.
        movie_ids = list(
            dict.fromkeys(movie_ids)
        )

        # -----------------------------------------
        # Find input movies
        # -----------------------------------------

        movie_indexes = genre_matrix.index[
            genre_matrix["movieId"].isin(
                movie_ids
            )
        ]

        if len(movie_indexes) == 0:
            raise ValueError(
                "None of the provided Movie IDs "
                "were found."
            )

        found_movie_ids = set(
            genre_matrix.loc[
                movie_indexes,
                "movieId",
            ]
        )

        missing_movie_ids = (
            set(movie_ids)
            - found_movie_ids
        )

        if missing_movie_ids:
            raise ValueError(
                "Movie IDs not found: "
                f"{sorted(missing_movie_ids)}"
            )

        # -----------------------------------------
        # Feature matrix
        # -----------------------------------------

        features = genre_matrix.drop(
            columns=[
                "movieId",
                "title",
                "genres",
                "year",
            ]
        )

        # -----------------------------------------
        # Build preference profile
        # -----------------------------------------

        movie_vectors = features.loc[
            movie_indexes
        ]

        profile_vector = (
            movie_vectors
            .mean(axis=0)
            .to_frame()
            .T
        )

        # -----------------------------------------
        # Calculate similarity
        # -----------------------------------------

        scores = cosine_similarity(
            profile_vector,
            features,
        ).flatten()

        # -----------------------------------------
        # Build result
        # -----------------------------------------

        similarity_df = genre_matrix[
            [
                "movieId",
                "title",
                "genres",
                "year",
            ]
        ].copy()

        similarity_df[
            "similarity"
        ] = scores

        # -----------------------------------------
        # Remove input movies
        # -----------------------------------------

        similarity_df = similarity_df[
            ~similarity_df["movieId"].isin(
                movie_ids
            )
        ]

        # -----------------------------------------
        # Sort by similarity
        # -----------------------------------------

        similarity_df = (
            similarity_df
            .sort_values(
                by="similarity",
                ascending=False,
            )
        )

        return similarity_df.head(top_n)