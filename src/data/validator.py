import pandas as pd


class DataValidator:
    """
    Validate and analyze datasets.
    """

    @staticmethod
    def dataset_info(df: pd.DataFrame, name: str) -> str:

        report = []

        report.append("=" * 50)
        report.append(f"{name} Dataset")
        report.append("=" * 50)

        report.append(f"Rows: {df.shape[0]}")
        report.append(f"Columns: {df.shape[1]}")

        report.append("\nData Types:")
        report.append(df.dtypes.to_string())

        report.append("\nMissing Values:")
        report.append(df.isnull().sum().to_string())

        report.append(f"\nDuplicate Rows: {df.duplicated().sum()}")

        return "\n".join(report)