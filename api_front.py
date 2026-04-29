import pandas as pd
from flask import Flask, request, render_template
from typing import List, Dict
from pandas import DataFrame
import ast

app = Flask(__name__)

def get_restaurant_data() -> DataFrame:
    data = pd.read_csv('data/restaurants.csv')
    return data

def get_restaurant_direct() -> DataFrame:
    data1 = pd.read_csv('data/Restaurants_direct.csv')
    data1['location'] = data1['location'].apply(ast.literal_eval)
    data1['hours_day'] = data1['hours_day'].apply(ast.literal_eval)
    return data1

def get_reviews_data() -> DataFrame:
    data2 = pd.read_csv('data/restaurant_reviews.csv')
    return data2

def get_preferences_data() -> DataFrame:
    data3 = pd.read_csv('data/category_table.csv')
    return data3

def index() -> str:
    return render_template('index.html', active_page='home')

def locator_list():
    data = get_restaurant_direct()
    locators = data['locator'].unique().tolist()
    return locators


##----- time alteration------##

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

app.jinja_env.filters['format_time'] = format_time

# ––––––––––––––– API ENDPOINT ––––––––––––––– #
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants() -> List[Dict]:
    '''
    API endpoint to retrieve all restaurant data.

    Returns:
        List[Dict]: A list of restaurant records in dictionary format.
    '''
    data = get_restaurant_direct()
    return data.to_dict('records')

## ––––––––––––––– HOME & ABOUT ROUTES ––––––––––––––– ##
@app.route('/')
def home():
    return render_template('index.html', active_page='home')

@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html", active_page="about")

## ––––––––––––––– RESTAURANT MODEL ––––––––––––––– ##
@app.route('/restaurants', methods=["GET"])
def get_restaurants_page() -> str:
    '''
    Render the restaurant directory page with optional location filtering.

    Query Parameter:
        place (Optional[str]): Filter restaurants by location.
    
    Returns:
        str: Rendered HTML for the restaurants page.
    '''
    locators = locator_list()
    place = request.args.get('place')
    data = get_restaurant_direct()
    df = pd.DataFrame(data)

    df = df.drop(columns=['id'])

    if place:
        df = df[df['locator'] == place]

    restaurants = df.to_dict(orient='records')

    return render_template(
        "restaurants.html",
        active_page="restaurants",
        #tables=[df.to_html(classes='data')],
        restaurants=restaurants,
        titles=df.columns.values,
        locators=locators,
        selected_place=place)

@app.route('/restaurant/<name>')
def restaurant_detail(name: str) -> str:
    '''
    Renders a detailed page for a specific restaurant.

    Args:
        name (str): The name of the restaurant.

    Returns: 
        str: Rendered HTML for the restaurant detail page.
    
    Raises:
        404: If the restaurant is not found. 
    '''
    data = get_restaurant_direct()
    df = pd.DataFrame(data)

    restaurant = df[df["name"] == name]

    if restaurant.empty:
        return "Restaurant not found", 404
    
    restaurant = restaurant.iloc[0].to_dict()

    return render_template(
        "restaurant_detail.html",
        active_page="restaurants",
        restaurant=restaurant)

## ––––––––––––––– REVIEWS MODEL ––––––––––––––– ##
@app.route('/reviews', methods=["GET"])
def get_reviews_page():
    rest = get_restaurant_direct()
    data = get_reviews_data()

    merged = pd.merge(data, rest[['name', 'rating']], on='name', how='left')
    
    reviews = merged.to_dict(orient='records')

    return render_template("reviews.html", active_page="reviews", reviews=reviews)

## ––––––––––––––– PREFERENCES MODEL ––––––––––––––– ##
@app.route('/preferences', methods=["GET"])
def get_preferences_page():
    return render_template("preferences.html", active_page="preferences")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')