import pandas as pd
import numpy as np

#detect functions

def detect_duplicates(df:pd.DataFrame)-> dict :
    return {
        "row_duplicates":int(df.duplicated().sum())
        
    }

def detect_missing_values(df:pd.DataFrame)-> dict:
    missing = df.isnull().sum()
    return {
        col:int(count) for col , count in missing.items() if count > 0
    }


def detect_invalid_values(df: pd.DataFrame)-> dict:
    issues = {}
    
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    for col in numeric_cols:
        col_issues=[]

        if (df[col] < 0).any():
            col_issues.append("Negative values")

        if np.isinf(df[col]).any():
            col_issues.append("Infinite values")

        if col_issues:
            issues[col] = col_issues
    return issues


#suggestion function

def  suggest_cleaning_actions(df : pd.DataFrame , detection_report: dict)-> dict:
    actions = {}

    #missing values
    for col in detection_report.get("missing_values", {}):
        if pd.api.types.is_numeric_dtype(df[col]):
            actions[col] = "median_imputation"
        else:
            actions[col] = "mode_imputation"
    
    #invalid values
    for col in detection_report.get("invalid_values", {}):
        if "Negative values" in detection_report["invalid_values"][col]:
            actions[col] = "set_negative_to_zero"
        if "Infinite values" in detection_report["invalid_values"][col]:
            actions[col] = "replace_infinite_with_median"

        #duplicates
        if detection_report.get("duplicates", {}).get("row_duplicates", 0) > 0:
            actions["duplicates"] = "drop"

    return actions



#apply functions

def apply_missing_value_fix(df : pd.DataFrame , col:str , strategy:str)-> pd.DataFrame:
    if strategy == "mean_imputation":
        df[col] = df[col].fillna(df[col].mean())
    elif strategy == "median_imputation":
        df[col] = df[col].fillna(df[col].median())
    elif strategy == "mode_imputation":
        mode_value = df[col].mode()[0]
        df[col] = df[col].fillna(mode_value)
    return df

def apply_invalid_value_fix(df: pd.DataFrame, col: str, strategy: str) -> pd.DataFrame:
    df = df.copy()

    if strategy == "set_negative_to_zero":
        df[col] = df[col].apply(lambda x: max(x, 0))
    elif strategy == "replace_infinite_with_median":
        median_value = df[col].replace([np.inf, -np.inf], np.nan).median()
        df[col] = df[col].replace([np.inf, -np.inf], median_value)

    return df

def apply_duplicate_fix(df: pd.DataFrame, strategy: str) -> pd.DataFrame:
    df = df.copy()
    if strategy == "drop":
        df = df.drop_duplicates()
    return df   

# pipeline 

def run_cleaning_pipeline(df: pd.DataFrame , actions:dict) -> pd.DataFrame:
    cleaned_df = df.copy()

    for col , action in actions.items():
        if col == "duplicates":
            cleaned_df = apply_duplicate_fix(cleaned_df, action)

        elif action in ["mean_imputation", "median_imputation", "mode_imputation"]:
            cleaned_df = apply_missing_value_fix(cleaned_df, col, action)

        elif action in ["set_negative_to_zero", "replace_infinite_with_median"]:
            cleaned_df = apply_invalid_value_fix(cleaned_df, col, action)

    return cleaned_df        

