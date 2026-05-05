import pandas as pd
import ast
from flask import Flask, request, render_template
from typing import List, Dict
from pandas import DataFrame
from data_utils import (format_time, get_restaurant_direct, 
                        get_reviews_data, get_preferences_data,
                        locator_list, cats_list
                        )

app = Flask(__name__)

#----------------- FILTERS -----------------#
app.jinja_env.filters['format_time'] = format_time

## ––––––––––––––– HOME & ABOUT ROUTES ––––––––––––––– ##
@app.route('/')
def home():
    return render_template("index.html", active_page="home")

@app.route('/about', methods=["GET"])
def about():
    return render_template("about.html", active_page="about")

# ––––––––––––––– RESTAURANTS: API ENDPOINT ––––––––––––––– #
## 2 GET
@app.route('/api/restaurants', methods=['GET'])
def get_restaurants() -> List[Dict]:
    '''
    API endpoint to retrieve all restaurant data.

    Returns:
        List[Dict]: A list of restaurant records in dictionary format.
    '''
    data = get_restaurant_direct()
    return data.to_dict('records')

@app.route('/api/restaurants/<name>', methods=['GET'])
def api_get_restaurant(name):
    df = get_restaurant_direct()
    result = df[df['name'] == name]

    if result.empty:
        return {"error": "not found"}, 404

    return result.iloc[0].to_dict()

## 1 POST
@app.route('/api/restaurants', methods=['POST'])
def api_add_restaurant():
    data = request.json
    df = get_restaurant_direct()

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    return {"message": "restaurant added (in-memory only)"}, 201

## 1 DELETE
@app.route('/api/restaurants/<name>', methods=['DELETE'])
def api_delete_restaurant(name):
    df = get_restaurant_direct()

    df = df[df['name'] != name]

    return {"message": f"{name} deleted (not saved)"}, 200

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
@app.route('/restaurant/<name>', methods=['GET'])
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

## ––––––––––––––– REVIEWS: API ENDPOINT ––––––––––––––– ##
## 2 GET
@app.route('/api/reviews', methods=['GET'])
def api_get_reviews():
    return get_reviews_data().to_dict('records')

@app.route('/api/reviews/<name>', methods=['GET'])
def api_get_reviews_by_restaurant(name):
    df = get_reviews_data()
    return df[df['name'] == name].to_dict('records')

## 1 POST
@app.route('/api/reviews', methods=['POST'])
def api_add_review():
    data = request.json
    df = get_reviews_data()

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    return {"message": "review added (in-memory only)"}, 201

## 1 DELETE
@app.route('/api/reviews/<name>', methods=['DELETE'])
def api_delete_review(name):
    df = get_reviews_data()

    df = df[df['name'] != name]

    return {"message": "review deleted"}, 200

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

    merged = merged.drop_duplicates(subset=['name'])

    reviews = merged.to_dict(orient='records')

    return render_template(
        "reviews.html", 
        reviews=reviews,
        active_page="reviews")

## Individual Reviews Page
@app.route('/restaurant/review/<name>', methods=['GET'])
def review_page(name: str ) -> str:
    """Render a page showing all reviews for a specific restaurant."""
    
    reviews = get_reviews_data()
    reviews_df = reviews[reviews['name'] == name]
    reviews = reviews_df.to_dict(orient='records')

    restaurant_df = get_restaurant_direct()
    restaurant = restaurant_df[restaurant_df['name'] == name]
    
    if restaurant.empty:
        return "Restaurant not found", 404
    
    restaurant = restaurant.iloc[0].to_dict()

    return render_template(
        "restaurant_reviews.html",
        restaurant=restaurant,
        reviews=reviews,
        active_page="reviews"
    )

## ––––––––––––––– PREFERENCES: API ENDPOINT ––––––––––––––– ##
## 2 GET
@app.route('/api/preferences', methods=['GET'])
def api_get_preferences():
    return get_preferences_data().to_dict('records')

@app.route('/api/preferences/cats', methods=['GET'])
def api_get_cats():
    return cats_list()

## 1 POST
@app.route('/api/preferences', methods=['POST'])
def api_add_preference():
    data = request.json
    df = get_preferences_data()

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    return {"message": "preference added"}, 201

## 1 DELETE
@app.route('/api/preferences/<name>', methods=['DELETE'])
def api_delete_preference(name):
    df = get_preferences_data()

    df = df[df['name'] != name]

    return {"message": "preference deleted"}, 200

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