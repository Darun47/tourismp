import pandas as pd

DATA_PATH = "data/master_tourism_dataset_v2_enhanced.csv"

def load_dataset():
    
    df = pd.read_csv(DATA_PATH)
    
    return df


def preprocess_dataset(df):

    df = df.drop_duplicates()

    df["combined_features"] = (
        df["Site Name"].astype(str) + " " +
        df["Type"].astype(str) + " " +
        df["city"].astype(str) + " " +
        df["country"].astype(str) + " " +
        df["Interests"].astype(str)
    )

    return df


if __name__ == "__main__":

    df = load_dataset()

    df = preprocess_dataset(df)

    print(df.head())
