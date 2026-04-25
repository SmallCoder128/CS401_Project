import pandas as pd
from flask import Flask, request, render_template
from typing import List, Dict
from pandas import DataFrame

app = Flask(__name__)

def get_restaurant_data() -> DataFrame:
    data = pd.read_csv("restaurants.csv")
    return data

def get_reviews_data() -> DataFrame:
    data2 = pd.read_csv("restaurant_reviews.csv")
    return data2

def get_preferences_data() -> DataFrame:
    data3 = pd.read_csv("category_table.csv")
    return data3

def index() -> str:
    return render_template("index.html", active_page="home")

def locator_list():
    data = get_restaurant_data()
    locators = data['Locator'].unique().tolist()
    return locators

# ––––––––––––––– API ENDPOINT ––––––––––––––– #
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants() -> List[Dict]:
    '''
    API endpoint to retrieve all restaurant data.

    Returns:
        List[Dict]: A list of restaurant records in dictionary format.
    '''
    data = get_restaurant_data()
    return data.to_dict('records')

## ––––––––––––––– HOME & ABOUT ROUTES ––––––––––––––– ##
@app.route('/')
def home():
    return render_template("index.html", active_page="home")

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
    data = get_restaurant_data()
    df = pd.DataFrame(data)

    df = df.drop(columns=['id'])

    if place:
        df = df[df['Locator'] == place]

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
    data = get_restaurant_data()
    df = pd.DataFrame(data)

    restaurant = df[df["Name"] == name]

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
    return render_template("reviews.html", active_page="reviews")

## ––––––––––––––– PREFERENCES MODEL ––––––––––––––– ##
@app.route('/preferences', methods=["GET"])
def get_preferences_page():
    return render_template("preferences.html", active_page="preferences")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')