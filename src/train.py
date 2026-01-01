import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

def train_model(data_path, model_path):
    df = pd.read_csv(data_path)

    y = df['quantity_wasted']
    X = df.drop(columns=['quantity_wasted', 'waste_ratio', 'waste_per_guest'])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("R2:", r2_score(y_test, y_pred))

    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
