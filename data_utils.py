import pandas as pd
from pandas import DataFrame
import ast

def format_time(value):
    """Convert 0700 to 7:00 AM"""
    if not value:
        return "Closed"
    value = str(value).zfill(4)
    hour = int(value[:2])
    minute = value[2:]
    period = "AM" if hour < 12 else "PM"
    if hour == 0:
        hour = 12
    elif hour > 12:
        hour -= 12
    return f"{hour}:{minute} {period}"

def get_restaurant_data() -> DataFrame:
    data = pd.read_csv("data/restaurants.csv")
    return data

def get_restaurant_direct() -> DataFrame:
    data1 = pd.read_csv('data/Restaurants_direct.csv')
    data1['location'] = data1['location'].apply(ast.literal_eval)
    data1['hours_day'] = data1['hours_day'].apply(ast.literal_eval)
    data1['coordinates'] = data1['coordinates'].apply(ast.literal_eval)
    data1['attributes'] = data1['attributes'].apply(ast.literal_eval)
    data1['menu_url'] = data1['attributes'].apply(lambda x: x.get('menu_url'))
    return data1

def get_reviews_data() -> DataFrame:
    data2 = pd.read_csv("data/restaurant_reviews.csv")
    return data2

def get_preferences_data() -> DataFrame:
    data3 = pd.read_csv("data/category_table.csv")
    return data3

def locator_list():
    data = get_restaurant_direct()
    locators = data['locator'].str.strip().unique().tolist()
    return locators

def cats_list():
    data = get_preferences_data()
    df = pd.DataFrame(data)

    df['cats'] = df['cats'].apply(ast.literal_eval)
    all_cats = df['cats'].explode().unique().tolist()
    return sorted(all_cats)