from src.data.loader import DataLoader

from src.collaborative.model import CollaborativeModel
from src.collaborative.recommender import CollaborativeRecommender

from src.config.settings import (
    COLLABORATIVE_RECOMMENDATIONS_DIR,
)


def main():

    print("Loading datasets...")

    loader = DataLoader()

    movies = loader.load_movies()

    print(
        f"Movies: {len(movies)}"
    )

    # ======================================
    # Load Model
    # ======================================

    print("\nLoading trained model...")

    collaborative_model = CollaborativeModel()

    collaborative_model.load()

    # ======================================
    # Create Recommender
    # ======================================

    recommender = CollaborativeRecommender(
        model=collaborative_model.model,
        trainset=collaborative_model.trainset,
        movies=movies,
    )

    # ======================================
    # User Input
    # ======================================

    user_id = int(
        input(
            "\nEnter User ID: "
        )
    )

    recommendations = recommender.recommend(
        user_id=user_id,
        n_recommendations=10,
    )

    print("\nRecommendations")

    print(recommendations)

    # ======================================
    # Save
    # ======================================

    output_path = (
        COLLABORATIVE_RECOMMENDATIONS_DIR /
        f"user_{user_id}_recommendations.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    recommendations.to_csv(
        output_path,
        index=False,
    )

    print("\nSaved:")

    print(output_path)


if __name__ == "__main__":
    main()