# Smart Markets for Smart Produce

### Did by : en peru maha naan oru paithiyam 🤣

## Overview

This project is a web application that predicts the price of produce and provides actionable insights to help users decide whether to sell or hold their produce. It features a React frontend that communicates with a Python backend powered by FastAPI. The backend uses a simple machine learning model to predict prices based on historical data.

## Architecture

The application is composed of two main components:

- **Frontend:** A single-page application built with [React](https://reactjs.org/). It uses [Axios](https://axios-http.com/) for making API requests, [Chart.js](https://www.chartjs.org/) for data visualization, and [Bootstrap](https://getbootstrap.com/) for styling.
- **Backend:** A RESTful API built with [FastAPI](https://fastapi.tiangolo.com/). It uses [Pandas](https://pandas.pydata.org/) for data manipulation and [Scikit-learn](https://scikit-learn.org/stable/) for the machine learning model.

### Architecture Diagram

```
+-----------------+      +-----------------+
|                 |      |                 |
|   React         |----->|   FastAPI       |
|   Frontend      |      |   Backend       |
|                 |      |                 |
+-----------------+      +-----------------+
      |                          |
      |                          |
      v                          v
+-----------------+      +-----------------+
|   Chart.js      |      |   Scikit-learn  |
|   (Charts)      |      |   (ML Model)    |
+-----------------+      +-----------------+
```

## Features

- **Price Prediction:** Predicts the future price of various produce items.
- **Actionable Insights:** Provides users with simple "sell" or "hold" recommendations based on the price prediction.
- **Historical Data Visualization:** Displays a chart of historical produce prices.

## Data Flow

1.  The backend loads a hardcoded dataset of produce prices from `data.py` into a Pandas DataFrame.
2.  The data is preprocessed by converting dates to datetime objects and one-hot encoding categorical features like `weather` and `demand`.
3.  The frontend fetches the list of available produce from the backend's `/produce` endpoint.
4.  When the user selects a produce item, the frontend calls the `/predict/{produce_name}` endpoint.
5.  The backend trains a simple Linear Regression model on the historical data for the selected produce.
6.  The model predicts the price for the next day.
7.  The backend returns the prediction, an actionable insight, and the historical data to the frontend.
8.  The frontend displays the information to the user, including a chart of the historical prices.

## API Endpoints

### `GET /produce`

- **Description:** Returns a list of unique produce names available for prediction.
- **Response:**
  ```json
  {
    "produce": ["Apples", "Tomatoes", "Cucumbers"]
  }
  ```

### `GET /predict/{produce_name}`

- **Description:** Predicts the price of a given produce for the next day.
- **URL Parameters:**
  - `produce_name` (string, required): The name of the produce to predict.
- **Response:**
  ```json
  {
      "produce_name": "Apples",
      "prediction": 272.50,
      "insight": "Predicted price is 272.50, which is higher than the last recorded price of 270. Consider selling.",
      "historical_data": [
          {"date": "2023-01-01", "price": 250},
          {"date": "2023-01-02", "price": 255},
          ...
      ]
  }
  ```

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/)
- [Python 3.8+](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/)

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the backend server:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8001
    ```
    The backend will be running at `http://localhost:8001`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install the dependencies:**
    ```bash
    npm install
    ```
3.  **Run the frontend development server:**
    ```bash
    npm start
    ```
    The frontend will be running at `http://localhost:3000` and will connect to the backend at `http://localhost:8001`.

## Technical Deep Dive

### Backend

- **Data Preprocessing:** The `date` column is converted to a datetime object, and a `day_of_year` feature is extracted. The categorical features `weather` and `demand` are one-hot encoded to be used in the machine learning model.
- **Machine Learning Model:** A `LinearRegression` model from Scikit-learn is used. For each prediction request, a new model is trained on the historical data for the specific produce. The features used for training are `day_of_year` and the one-hot encoded `weather` and `demand` columns. The prediction is made for the next day (`day_of_year + 1`).
- **Actionable Insight:** The predicted price is compared to the last recorded price. If the predicted price is higher, the insight suggests selling; otherwise, it suggests holding.

### Frontend

- **State Management:** The `App` component uses the `useState` and `useEffect` hooks to manage the application's state, including the list of produce, the selected produce, the prediction data, and any errors.
- **Data Fetching:** The `axios` library is used to make HTTP requests to the backend API. The `useEffect` hook is used to fetch the produce list on component mount and to fetch the prediction data whenever the `selectedProduce` state changes.
- **Charting:** The `react-chartjs-2` library is used to render a line chart of the historical price data received from the backend.

## Future Improvements

- **Use a real database:** Replace the hardcoded data with a database like PostgreSQL or MongoDB to store and manage the produce data.
- **Deployment:** Deploy the frontend and backend to a cloud platform like Heroku, Vercel, or AWS.
- **Improve the ML model:** Use a more sophisticated time-series model like ARIMA or LSTM for more accurate price predictions.
- **User authentication:** Add user authentication to allow users to save their preferences and track their portfolio of produce.
