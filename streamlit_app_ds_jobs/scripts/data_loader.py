import pandas as pd
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def load_job_data(file_path="data/DataScience_job_sample.csv"):
    """
    Load and preprocess the data science job data.
    Returns a cleaned DataFrame ready for analysis.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Load data
    df = pd.read_csv(file_path, index_col=0)

    # Drop missing values
    df = df.dropna()

    # Drop duplicates based on key identifying columns
    df = df.drop_duplicates(subset=['roles', 'companies', 'locations', 'experience', 'skills'])

    # Normalize case to lowercase
    df = df.apply(lambda x: x.astype(str).str.lower())

    # Split locations into lists
    df['locations'] = df['locations'].apply(lambda x: x.split(',') if isinstance(x, str) else [])

    # Clean location text
    df['locations_clean'] = df['locations'].apply(lambda x: ', '.join([loc.strip() for loc in x]))

    # Exploded location for plotting (optional helper)
    df_exploded = df.explode('locations')
    df_exploded['locations'] = df_exploded['locations'].str.strip()

    return df, df_exploded
