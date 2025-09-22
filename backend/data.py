import pandas as pd
from io import StringIO

def get_produce_data():
    produce_data = """date,produce,price,weather,demand
2023-01-01,Apples,250,Sunny,High
2023-01-02,Apples,255,Sunny,High
2023-01-03,Apples,260,Cloudy,Medium
2023-01-04,Apples,258,Rainy,Low
2023-01-05,Apples,262,Sunny,Medium
2023-01-06,Apples,265,Sunny,High
2023-01-07,Apples,270,Cloudy,High
2023-01-01,Tomatoes,300,Sunny,High
2023-01-02,Tomatoes,305,Sunny,High
2023-01-03,Tomatoes,310,Cloudy,Medium
2023-01-04,Tomatoes,308,Rainy,Low
2023-01-05,Tomatoes,312,Sunny,Medium
2023-01-06,Tomatoes,315,Sunny,High
2023-01-07,Tomatoes,320,Cloudy,High
2023-01-01,Cucumbers,150,Sunny,High
2023-01-02,Cucumbers,155,Sunny,High
2023-01-03,Cucumbers,160,Cloudy,Medium
2023-01-04,Cucumbers,158,Rainy,Low
2023-01-05,Cucumbers,162,Sunny,Medium
2023-01-06,Cucumbers,165,Sunny,High
2023-01-07,Cucumbers,170,Cloudy,High
"""
    return pd.read_csv(StringIO(produce_data))