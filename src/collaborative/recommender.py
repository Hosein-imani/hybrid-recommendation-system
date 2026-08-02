import pandas as pd


class CollaborativeRecommender:
    """
    Generate recommendations using
    trained Surprise model
    """

    def __init__(
        self,
        model,
        trainset,
        movies: pd.DataFrame
    ):
        """
        Parameters:
        -----------
        model:
            Trained Surprise model

        trainset:
            Surprise trainset

        movies:
            Movies dataframe
        """

        self.model = model
        self.trainset = trainset
        self.movies = movies



    def recommend(
        self,
        user_id: int,
        n_recommendations: int = 10
    ):
        """
        Generate top-N recommendations
        for a user.
        """


        recommendations = []


        # All movies
        movie_ids = (
            self.movies["movieId"]
            .unique()
        )


        # Movies user already rated

        try:

            inner_user_id = (
                self.trainset
                .to_inner_uid(user_id)
            )


            rated_movies = {
                self.trainset
                .to_raw_iid(movie_inner_id)

                for (
                    movie_inner_id,
                    _
                )
                in self.trainset
                .ur[inner_user_id]
            }


        except ValueError:

            rated_movies = set()



        for movie_id in movie_ids:


            if movie_id in rated_movies:
                continue



            prediction = self.model.predict(
                uid=user_id,
                iid=movie_id
            )


            recommendations.append(
                {
                    "movieId": movie_id,
                    "estimated_rating":
                    prediction.est
                }
            )



        recommendations = (
            pd.DataFrame(
                recommendations
            )
            .sort_values(
                by="estimated_rating",
                ascending=False
            )
            .head(
                n_recommendations
            )
        )



        recommendations = recommendations.merge(
            self.movies,
            on="movieId",
            how="left"
        )


        return recommendations[
            [
                "movieId",
                "title",
                "genres",
                "estimated_rating"
            ]
        ]