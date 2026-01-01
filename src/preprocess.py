import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(input_path, output_path):
    df = pd.read_csv(input_path)

    # Drop index column
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    # Feature engineering
    df['waste_ratio'] = df['quantity_wasted'] / df['quantity_prepared']
    df['waste_per_guest'] = df['quantity_wasted'] / df['num_guests']

    # One-hot encode
    categorical_cols = df.select_dtypes(include='object').columns
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Scale numeric columns
    scaler = StandardScaler()
    numeric_cols = ['num_guests', 'quantity_prepared', 'waste_ratio', 'waste_per_guest']
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    df.to_csv(output_path, index=False)
