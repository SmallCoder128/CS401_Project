import pandas as pd
import ast
from flask import Flask, request, render_template
from typing import List, Dict
from data_utils import (format_time, get_restaurant_direct, get_reviews_data, get_preferences_data,
                        locator_list, cats_list)

app = Flask(__name__)

app.jinja_env.filters['format_time'] = format_time

# =============================================================================
# TEMPLATE ROUTES
# =============================================================================

## ====== HOME & ABOUT ====== ##
@app.route('/')
def home():
    '''Renders the home page.'''
    return render_template("index.html", active_page="home")

@app.route('/about', methods=["GET"])
def about():
    '''Renders the about page.'''
    return render_template("about.html", active_page="about")

## ====== RESTAURANTS MODEL ====== ##
## Directory
@app.route('/restaurants', methods=["GET"])
def get_restaurants_page() -> str:
    '''Renders the restaurant directory page with optional location and category filtering.'''
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
    '''Renders the detail page for a specific restaurant. Returns 404 if not found.'''
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

## ====== REVIEWS MODEL ====== ##
## General Reviews Page
@app.route('/reviews', methods=["GET"])
def get_reviews_page():
    """Renders the reviews page with optional sorting by rating or alphabetically."""
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

## === PREFERENCES MODEL === ##
@app.route('/preferences', methods=["GET"])
def get_preferences_page():
    '''Renders the preferences page with all categories and preference records.'''
    cats = cats_list()
    preferences = get_preferences_data().to_dict(orient='records')

    return render_template(
        "preferences.html", 
        preferences=preferences,
        cats=cats,
        active_page="preferences")

# =============================================================================
# API ROUTES
# =============================================================================

## ====== RESTAURANTS ====== ##
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
def api_get_restaurant(name: str) -> dict:
    """
    Retrieve a single restaurant by name.

    Args:
        name: The name of the restaurant to look up.

    Returns:
        A dictionary of the restaurant's data, or a 404 error if not found.
    """
    df = get_restaurant_direct()
    result = df[df['name'] == name]

    if result.empty:
        return {"error": "not found"}, 404

    return result.iloc[0].to_dict()

## 1 POST
@app.route('/api/restaurants', methods=['POST'])
def api_add_restaurant() -> tuple[dict, int]:
    """
    Add a new restaurant to the in-memory dataset.

    Expects a JSON body matching the restaurant schema.
    Note: changes are not persisted to the CSV file.

    Returns:
        A confirmation message with a 201 status code.
    """
    data = request.json
    df = get_restaurant_direct()

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    return {"message": "restaurant added (in-memory only)"}, 201

## 1 DELETE
@app.route('/api/restaurants/<name>', methods=['DELETE'])
def api_delete_restaurant(name: str) -> tuple[dict, int]:
    """
    Delete a restaurant by name from the in-memory dataset.

    Args:
        name: The name of the restaurant to delete.

    Note: changes are not persisted to the CSV file.

    Returns:
        A confirmation message with a 200 status code.
    """
    df = get_restaurant_direct()

    df = df[df['name'] != name]

    return {"message": f"{name} deleted (not saved)"}, 200

## ====== REVIEWS ====== ##
## 2 GET
@app.route('/api/reviews', methods=['GET'])
def api_get_reviews() -> list[dict]:
    """
    Retrieve all reviews.

    Returns:
        list[dict]: A list of all review records.
    """
    return get_reviews_data().to_dict('records')

@app.route('/api/reviews/<name>', methods=['GET'])
def api_get_reviews_by_restaurant(name: str) -> list[dict]:
    """
    Retrieve reviews for a specific restaurant.

    Args:
        name (str): The name of the restaurant to filter reviews by.

    Returns:
        list[dict]: A list of review records matching the given restaurant name.
    """
    df = get_reviews_data()
    return df[df['name'] == name].to_dict('records')

## 1 POST
@app.route('/api/reviews', methods=['POST'])
def api_add_review() -> tuple[dict, int]:
    """
    Add a new review (in-memory only, not persisted to CSV).

    Request Body (JSON):
        name (str): The name of the restaurant.
        review1 (str): First review text.
        review2 (str): Second review text.
        review3 (str): Third review text.

    Returns:
        tuple[dict, int]: A confirmation message and HTTP status code 201.
    """
    data: dict = request.json
    df = get_reviews_data()

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    return {"message": "review added (in-memory only)"}, 201

## 1 DELETE
@app.route('/api/reviews/<name>', methods=['DELETE'])
def api_delete_review(name: str) -> tuple[dict, int]:
    """
    Delete reviews for a specific restaurant (in-memory only, not persisted to CSV).

    Args:
        name (str): The name of the restaurant whose reviews should be deleted.

    Returns:
        tuple[dict, int]: A confirmation message and HTTP status code 200.
    """
    df = get_reviews_data()

    df = df[df['name'] != name]

    return {"message": "review deleted"}, 200

## ====== PREFERENCES ====== ##
## 2 GET
@app.route('/api/preferences', methods=['GET'])
def api_get_preferences() -> list[dict]:
    """
    Retrieve all restaurant preferences.

    Returns:
        list[dict]: A list of all preference records.
    """
    return get_preferences_data().to_dict('records')

@app.route('/api/preferences/cats', methods=['GET'])
def api_get_cats() -> list[str]:
    """
    Retrieve all unique food category tags.

    Returns:
        list[str]: A list of all available category tags.
    """
    return cats_list()

## 1 POST
@app.route('/api/preferences', methods=['POST'])
def api_add_preference() -> tuple[dict, int]:
    """
    Add a new restaurant preference record.

    Args:
        data (dict): JSON request body containing preference fields
                     (name, alias, cats).

    Returns:
        tuple[dict, int]: Confirmation message and 201 status code.
    """
    data: dict = request.json
    df = get_preferences_data()

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    return {"message": "preference added"}, 201

## 1 DELETE
@app.route('/api/preferences/<name>', methods=['DELETE'])
def api_delete_preference(name: str) -> tuple[dict, int]:
    """
    Delete a restaurant preference by name.

    Args:
        name (str): The restaurant name to delete from preferences.

    Returns:
        tuple[dict, int]: Confirmation message and 200 status code.
    """
    df = get_preferences_data()

    df = df[df['name'] != name]

    return {"message": "preference deleted"}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')