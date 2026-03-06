import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error

# Load dataset
data_url = "https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv"
data = pd.read_csv(data_url)

# Features and target
features = [
    "GDP per capita",
    "headcount_ratio_upper_mid_income_povline",
    "year"
]

target = "Life Expectancy (IHME)"

# Prepare dataset
data_model = data[features + [target]].dropna()

X = data_model[features]
y = data_model[target]

# Train/validation split
X_train, X_val, y_train, y_val = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=9,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
train_preds = model.predict(X_train)
val_preds = model.predict(X_val)

# Metrics
train_r2 = r2_score(y_train, train_preds)
val_r2 = r2_score(y_val, val_preds)

train_mae = mean_absolute_error(y_train, train_preds)
val_mae = mean_absolute_error(y_val, val_preds)

train_rmse = root_mean_squared_error(y_train, train_preds)
val_rmse = root_mean_squared_error(y_val, val_preds)

# Print results
print("\nModel Performance")
print("------------------------")

print("Training metrics:")
print(f"R²:   {train_r2:.3f}")
print(f"MAE:  {train_mae:.3f}")
print(f"RMSE: {train_rmse:.3f}")

print("\nValidation metrics:")
print(f"R²:   {val_r2:.3f}")
print(f"MAE:  {val_mae:.3f}")
print(f"RMSE: {val_rmse:.3f}")

# Save model
with open("life_expectancy_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nModel saved as life_expectancy_model.pkl")