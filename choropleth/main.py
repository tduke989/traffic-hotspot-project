import pandas as pd


def format_str_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Format a string column by:
    - replacing hidden spaces
    - stripping whitespace
    - converting to lowercase
    - removing blank or 'nan' values
    """
    clean = (
        df[col]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df = df[(clean != "") & (clean != "nan")].copy()
    df[col] = clean
    return df

def main():


    incidents = pd.read_csv("Traffic_Incidents_filtered_2020.csv")

    cleaned = format_str_column(incidents, "INCIDENT INFO")
    highways = ["glenmore", "deerfoot", "stoney", "crowchild"]

    for h in highways:
        cleaned = cleaned[~cleaned["INCIDENT INFO"].str.contains(h, na=False)]
    cleaned["START_DT"] = pd.to_datetime(cleaned["START_DT"]) # convert to datetime 
    
    cleaned.to_csv("cleaned.csv", index=False)
    
    #print(cleaned)
    
main()
