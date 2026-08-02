import json
import joblib

from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise.model_selection import train_test_split

from src.config.settings import (
    COLLABORATIVE_MODELS_DIR,
)

class CollaborativeModel:
    """
    Collaborative Filtering model
    using Surprise SVD algorithm.
    """


    def __init__(
        self,
        n_factors=50,
        learning_rate=0.005,
        regularization=0.02,
        epochs=20
    ):
        """
        Initialize SVD model.

        Parameters
        ----------
        n_factors:
            Number of latent factors

        learning_rate:
            Learning rate for SGD

        regularization:
            Regularization strength

        epochs:
            Training iterations
        """
        self.n_factors = n_factors
        self.learning_rate = learning_rate
        self.regularization = regularization
        self.epochs = epochs

        self.model = SVD(
            n_factors=n_factors,
            lr_all=learning_rate,
            reg_all=regularization,
            n_epochs=epochs
        )


        self.trainset = None
        self.testset = None



    def prepare_data(
        self,
        ratings
    ):
        """
        Convert pandas dataframe
        into Surprise dataset.
        """


        reader = Reader(
            rating_scale=(
                ratings["rating"].min(),
                ratings["rating"].max()
            )
        )


        dataset = Dataset.load_from_df(
            ratings[
                [
                    "userId",
                    "movieId",
                    "rating"
                ]
            ],
            reader
        )


        self.trainset, self.testset = (
            train_test_split(
                dataset,
                test_size=0.2,
                random_state=42
            )
        )


        return self.trainset, self.testset



    def train(self):
        """
        Train SVD model.
        """

        if self.trainset is None:
            raise ValueError(
                "Dataset is not prepared. "
                "Run prepare_data() first."
            )


        self.model.fit(
            self.trainset
        )



    def predict(
        self,
        user_id,
        movie_id
    ):
        """
        Predict rating for user/movie 
        """


        prediction = self.model.predict(
            uid=user_id,
            iid=movie_id
        )


        return prediction.est




    def save(self):
        """
        Save trained model artifacts.
        """

        COLLABORATIVE_MODELS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        model_path = (
            COLLABORATIVE_MODELS_DIR /
            "svd_model.pkl"
        )

        trainset_path = (
            COLLABORATIVE_MODELS_DIR /
            "trainset.pkl"
        )

        joblib.dump(
            self.model,
            model_path
        )

        joblib.dump(
            self.trainset,
            trainset_path
        )

        return {

            "model_path": model_path,

            "trainset_path": trainset_path

        }



    def load(self):
        """
        Load trained model artifacts.
        """

        model_path = (
            COLLABORATIVE_MODELS_DIR /
            "svd_model.pkl"
        )

        trainset_path = (
            COLLABORATIVE_MODELS_DIR /
            "trainset.pkl"
        )

        self.model = joblib.load(
            model_path
        )

        self.trainset = joblib.load(
            trainset_path
        )



    def get_metadata(
        self,
        ratings,
        movies
    ):
        """
        Return model metadata.
        """

        return {

            "algorithm": "Surprise SVD",

            "n_factors":
                self.n_factors,

            "learning_rate":
                self.learning_rate,

            "regularization":
                self.regularization,

            "epochs":
                self.epochs,

            "ratings":
                len(ratings),

            "movies":
                len(movies),

            "users":
                ratings["userId"].nunique()

        }