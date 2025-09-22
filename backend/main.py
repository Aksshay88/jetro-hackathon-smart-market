
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from data import get_produce_data
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

app = FastAPI()

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load and preprocess data
df = get_produce_data()
df['date'] = pd.to_datetime(df['date'])
df['day_of_year'] = df['date'].dt.dayofyear

# One-hot encode categorical features
df = pd.get_dummies(df, columns=['weather', 'demand'], drop_first=True)

@app.get("/produce")
def get_produce():
    return {"produce": df["produce"].unique().tolist()}

@app.get("/predict/{produce_name}")
def predict_price(produce_name: str):
    produce_df = df[df['produce'] == produce_name]

    if produce_df.empty:
        return {"error": "Produce not found"}

    # Features and target
    features = ['day_of_year'] + [col for col in df.columns if 'weather_' in col or 'demand_' in col]
    X = produce_df[features]
    y = produce_df['price']

    # Train a simple model
    model = LinearRegression()
    model.fit(X, y)

    # "Predict" for the next day (day_of_year + 1)
    last_day = produce_df['day_of_year'].max()
    # Create a future dataframe with the same features as the training data
    future_df = pd.DataFrame([[last_day + 1, True, False, True, False]], columns=features)
    
    prediction = model.predict(future_df)

    # Generate actionable insight
    last_price = produce_df.iloc[-1]['price']
    insight = ""
    if prediction[0] > last_price:
        insight = f"Predicted price is {prediction[0]:.2f}, which is higher than the last recorded price of {last_price}. Consider selling."
    else:
        insight = f"Predicted price is {prediction[0]:.2f}, which is lower than the last recorded price of {last_price}. Consider holding."

    # Get historical data for charting
    historical_data = produce_df[['date', 'price']].to_dict(orient='records')

    return {
        "produce_name": produce_name,
        "prediction": prediction[0],
        "insight": insight,
        "historical_data": historical_data
    }
