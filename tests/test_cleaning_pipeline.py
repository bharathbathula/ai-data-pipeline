from app.core.data_loader import load_data

from app.core.cleaning_engine import (
    detect_duplicates,
    detect_missing_values,
    detect_invalid_values,
    suggest_cleaning_actions,
    run_cleaning_pipeline

)

def test_cleaning_pipeline():
    df = load_data("data/raw/cleaning_test_data.csv")

    detection_report = {
        "duplicates": detect_duplicates(df),
        "missing_values": detect_missing_values(df),
        "invalid_values": detect_invalid_values(df)
    }

    print("Detection Report:")
    print(detection_report)

    actions = suggest_cleaning_actions(df, detection_report)
    print("\nSuggested Actions:")
    print(actions)

    cleaned_df = run_cleaning_pipeline(df, actions)
    print("\nCleaned DataFrame:")
    print(cleaned_df)

if __name__ == "__main__":
    test_cleaning_pipeline()    