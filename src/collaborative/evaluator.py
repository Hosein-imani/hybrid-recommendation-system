from surprise import accuracy
from surprise import Trainset


class CollaborativeEvaluator:
    """
    Evaluate collaborative filtering models
    """

    def __init__(self, model):
        """
        Parameters:
        -----------
        model:
            Trained Surprise model
        """

        self.model = model


    def evaluate(
        self,
        testset
    ):
        """
        Evaluate model performance.

        Parameters:
        -----------
        testset:
            Surprise test dataset
        """

        predictions = self.model.test(
            testset
        )


        rmse = accuracy.rmse(
            predictions,
            verbose=False
        )


        mae = accuracy.mae(
            predictions,
            verbose=False
        )


        results = {
            "RMSE": rmse,
            "MAE": mae,
            "samples": len(predictions)
        }


        return results