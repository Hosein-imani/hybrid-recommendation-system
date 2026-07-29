from pathlib import Path

# ==================================================
# Project
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ==================================================
# Data
# ==================================================

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# ==================================================
# Outputs
# ==================================================

OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Dataset Analysis
DATASET_OUTPUT_DIR = OUTPUT_DIR / "dataset_analysis"
DATASET_REPORTS_DIR = DATASET_OUTPUT_DIR / "reports"
DATASET_STATISTICS_DIR = DATASET_OUTPUT_DIR / "statistics"
DATASET_VISUALIZATIONS_DIR = DATASET_OUTPUT_DIR / "visualizations"

# Content-Based
CONTENT_OUTPUT_DIR = OUTPUT_DIR / "content_based"
CONTENT_RECOMMENDATIONS_DIR = CONTENT_OUTPUT_DIR / "recommendations"
CONTENT_MATRICES_DIR = CONTENT_OUTPUT_DIR / "matrices"
CONTENT_REPORTS_DIR = CONTENT_OUTPUT_DIR / "reports"
CONTENT_VISUALIZATIONS_DIR = CONTENT_OUTPUT_DIR / "visualizations"

# Collaborative Filtering
COLLABORATIVE_OUTPUT_DIR = OUTPUT_DIR / "collaborative"
COLLABORATIVE_RECOMMENDATIONS_DIR = COLLABORATIVE_OUTPUT_DIR / "recommendations"
COLLABORATIVE_MODELS_DIR = COLLABORATIVE_OUTPUT_DIR / "models"
COLLABORATIVE_REPORTS_DIR = COLLABORATIVE_OUTPUT_DIR / "reports"
COLLABORATIVE_VISUALIZATIONS_DIR = COLLABORATIVE_OUTPUT_DIR / "visualizations"

# Hybrid
HYBRID_OUTPUT_DIR = OUTPUT_DIR / "hybrid"
HYBRID_RECOMMENDATIONS_DIR = HYBRID_OUTPUT_DIR / "recommendations"
HYBRID_MODELS_DIR = HYBRID_OUTPUT_DIR / "models"
HYBRID_REPORTS_DIR = HYBRID_OUTPUT_DIR / "reports"
HYBRID_VISUALIZATIONS_DIR = HYBRID_OUTPUT_DIR / "visualizations"

##########################




# ==========================================
# Feature Engineering
# ==========================================

CONTENT_FEATURE_ENGINEERING_DIR = CONTENT_OUTPUT_DIR / "feature_engineering"

CONTENT_FEATURE_ENGINEERING_REPORTS_DIR = (
    CONTENT_FEATURE_ENGINEERING_DIR / "reports"
)

CONTENT_FEATURE_ENGINEERING_ARTIFACTS_DIR = (
    CONTENT_FEATURE_ENGINEERING_DIR / "artifacts"
)

CONTENT_FEATURE_ENGINEERING_VISUALIZATIONS_DIR = (
    CONTENT_FEATURE_ENGINEERING_DIR / "visualizations"
)

# ==========================================
# Similarity
# ==========================================

CONTENT_SIMILARITY_DIR = CONTENT_OUTPUT_DIR / "similarity"

CONTENT_SIMILARITY_REPORTS_DIR = (
    CONTENT_SIMILARITY_DIR / "reports"
)

CONTENT_SIMILARITY_ARTIFACTS_DIR = (
    CONTENT_SIMILARITY_DIR / "artifacts"
)

CONTENT_SIMILARITY_VISUALIZATIONS_DIR = (
    CONTENT_SIMILARITY_DIR / "visualizations"
)

# ==========================================
# Recommender
# ==========================================

CONTENT_RECOMMENDER_DIR = CONTENT_OUTPUT_DIR / "recommender"

CONTENT_RECOMMENDER_REPORTS_DIR = (
    CONTENT_RECOMMENDER_DIR / "reports"
)

CONTENT_RECOMMENDER_RECOMMENDATIONS_DIR = (
    CONTENT_RECOMMENDER_DIR / "recommendations"
)

CONTENT_RECOMMENDER_VISUALIZATIONS_DIR = (
    CONTENT_RECOMMENDER_DIR / "visualizations"
)