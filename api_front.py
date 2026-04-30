import pandas as pd
import ast
from flask import Flask, request, render_template
from typing import List, Dict
from pandas import DataFrame

app = Flask(__name__)

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
#-----------------filters-----------------#
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
    return render_template("index.html", active_page="home")

@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html", active_page="about")

## ––––––––––––––– RESTAURANT MODEL ––––––––––––––– ##
## Directory Page
@app.route('/restaurants', methods=["GET"])
def get_restaurants_page() -> str:
    '''
    Render the restaurant directory page with optional location filtering.

    Query Parameter:
        place (Optional[str]): Filter restaurants by location.
        cats (Optional[str]): Filter restaurants by preference.
    
    Returns:
        str: Rendered HTML for the restaurants page.
    '''
    locators = locator_list()

    place = request.args.get('place')
    selected_cats = request.args.getlist('cats')

    restaurants_df = get_restaurant_direct()
    categories_df = get_preferences_data()

    categories_df['cats'] = categories_df['cats'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )

    merged = restaurants_df.merge(categories_df, on="name", how="left")

    # Filtering (Location & Category)
    if place:
        merged = merged[merged['locator'] == place]
    if selected_cats:
        merged = merged[
            merged['cats'].apply(lambda cat_list: all(c in cat_list for c in selected_cats))
        ]

    merged = merged.drop_duplicates(subset=['name'])

    restaurants = merged.to_dict(orient='records')

    return render_template(
        "restaurants.html",
        active_page="restaurants",
        restaurants=restaurants,
        locators=locators,
        selected_place=place,
        selected_cats=selected_cats)

## Individual Restaurant Page
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
    restaurants_df = get_restaurant_direct()
    categories_df = get_preferences_data()

    categories_df['cats'] = categories_df['cats'].apply(ast.literal_eval)

    restaurant = restaurants_df[restaurants_df['name'] == name]

    if restaurant.empty:
        return "Restaurant not found", 404
    
    restaurant = restaurant.iloc[0].to_dict()

    cats = categories_df[categories_df['name'] == name]['cats'].explode().tolist()

    return render_template(
        "restaurant_detail.html",
        active_page="restaurants",
        restaurant=restaurant,
        categories=cats)

## ––––––––––––––– REVIEWS MODEL ––––––––––––––– ##
## General Reviews Page
@app.route('/reviews', methods=["GET"])
def get_reviews_page():
    """
    Render reviews page with optional sorting.

    Query Params:
        sort (str): 'rating' or 'alpha'
    """
    reviews_df = get_reviews_data()
    restaurants_df = get_restaurant_direct()
    sort_option = request.args.get("sort")

    merged = reviews_df.merge(
        restaurants_df[['rating', 'name']], on='name', how='left'
    )

    # Sorting Logic
    if sort_option == "rating":
        merged = merged.sort_values(by="rating", ascending=False)
    elif sort_option == "alpha":
        merged = merged.sort_values(by="name", ascending=True)

    reviews = merged.to_dict(orient='records')

    return render_template(
        "reviews.html", 
        reviews=reviews,
        active_page="reviews")

## Individual Reviews Page
@app.route('/restaurant/reviews/<name>', methods=['GET'])
def restaurant_reviews(name: str) -> str:
    """
    Render all reviews for a specific restaurant.
    """
    reviews_df = get_reviews_data()
    restaurant_df = get_restaurant_direct()

    restaurant = restaurant_df[restaurant_df['name'] == name]
    
    if restaurant.empty:
        return "Restaurant not found", 404
    
    restaurant = restaurant.iloc[0].to_dict()

    reviews = reviews_df[reviews_df['name'] == name]
    reviews = reviews_df.to_dict(orient='records')

    return render_template(
        "restaurant_reviews.html",
        restaurant=restaurant,
        reviews=reviews,
        active_page="reviews"
    )
## ---------------SINGLE RESTRAURANT REVIEW PAGE---------------- ##
@app.route('/restaurant/review/<name>', methods=['GET'])
def review_page(name: str ) -> str:
    """Render a page showing all reviews for a specific restaurant."""
    
    reviews = get_reviews_data()
    reviews_df = reviews[reviews['name'] == name]
    reviews = reviews_df.to_dict(orient='records')

    return render_template(
        "restaurant_reviews.html",
        reviews=reviews,
        active_page="reviews"
    )
## ––––––––––––––– PREFERENCES MODEL ––––––––––––––– ##
@app.route('/preferences', methods=["GET"])
def get_preferences_page():
    cats = cats_list()
    preferences = get_preferences_data().to_dict(orient='records')

    return render_template(
        "preferences.html", 
        preferences=preferences,
        cats=cats,
        active_page="preferences")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')