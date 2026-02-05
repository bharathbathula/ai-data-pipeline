import pandas as pd

def run_eda(df:pd.DataFrame) -> dict:
    eda_report={}

    #shape
    eda_report["shape"] = {
        "rows":df.shape[0],
        "columns":df.shape[1]
    }

    #column types
    numerical_cols= df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    eda_report["columns"] ={
        "numerical": numerical_cols,
        "categorical": categorical_cols
    }

    #missing values
    missing_by_column = {k: int(v) for k, v in df.isnull().sum().to_dict().items()}
    total_missing = int(df.isnull().sum().sum())

    eda_report["missing_values"] = {
        "total_missing": total_missing,
        "by_column": missing_by_column
    }

    # summary statistics for numerical columns
    summary_stats = {}
    for col in numerical_cols:
        summary_stats[col] = {
            "mean": float(df[col].mean()) if pd.notnull(df[col].mean()) else None,
            "median": float(df[col].median()) if pd.notnull(df[col].median()) else None,
            "min": float(df[col].min()) if pd.notnull(df[col].min()) else None,
            "max": float(df[col].max()) if pd.notnull(df[col].max()) else None,
            "std": float(df[col].std()) if pd.notnull(df[col].std()) else None,
}


    eda_report["summary_statistics"] = summary_stats

    #categorical distribution
    categorical_distribution = {}
    for cols in categorical_cols:
        categorical_distribution[cols] = df[cols].value_counts().to_dict()

    eda_report["categorical_distribution"] = categorical_distribution


    return eda_report  