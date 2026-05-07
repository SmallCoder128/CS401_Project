import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from api_front import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# =============================================================================
# TEMPLATE ROUTES
# =============================================================================

# ====== HOME ====== #
def test_home_status(client):
    res = client.get('/')
    assert res.status_code == 200

def test_home_returns_html(client):
    res = client.get('/')
    assert b'<html' in res.data

def test_home_not_empty(client):
    res = client.get('/')
    assert len(res.data) > 0

def test_home_content_type(client):
    res = client.get('/')
    assert 'text/html' in res.content_type

# ====== ABOUT ====== #
def test_about_status(client):
    res = client.get('/about')
    assert res.status_code == 200

def test_about_returns_html(client):
    res = client.get('/about')
    assert b'<html' in res.data

def test_about_not_empty(client):
    res = client.get('/about')
    assert len(res.data) > 0

def test_about_content_type(client):
    res = client.get('/about')
    assert 'text/html' in res.content_type

# ====== RESTAURANTS PAGE ====== #
def test_restaurants_page_status(client):
    res = client.get('/restaurants')
    assert res.status_code == 200

def test_restaurants_page_returns_html(client):
    res = client.get('/restaurants')
    assert b'<html' in res.data

def test_restaurants_page_not_empty(client):
    res = client.get('/restaurants')
    assert len(res.data) > 0

def test_restaurants_page_content_type(client):
    res = client.get('/restaurants')
    assert 'text/html' in res.content_type

# ====== RESTAURANT DETAIL PAGE ====== #
def test_restaurant_detail_valid(client):
    res = client.get('/restaurant/Monkeypod Kitchen')
    assert res.status_code == 200

def test_restaurant_detail_valid_deck(client):
    res = client.get('/restaurant/Deck.')
    assert res.status_code == 200

def test_restaurant_detail_invalid_returns_404(client):
    res = client.get('/restaurant/FakeRestaurant999')
    assert res.status_code == 404

def test_restaurant_detail_valid_returns_html(client):
    res = client.get('/restaurant/Monkeypod Kitchen')
    assert b'<html' in res.data

def test_restaurant_detail_invalid_name_symbols(client):
    res = client.get('/restaurant/!!!!')
    assert res.status_code in [200, 404]

def test_restaurant_detail_empty_string(client):
    res = client.get('/restaurant/ ')
    assert res.status_code in [200, 404]

# ====== REVIEWS PAGE ====== #
def test_reviews_page_status(client):
    res = client.get('/reviews')
    assert res.status_code == 200

def test_reviews_page_returns_html(client):
    res = client.get('/reviews')
    assert b'<html' in res.data

def test_reviews_page_not_empty(client):
    res = client.get('/reviews')
    assert len(res.data) > 0

def test_reviews_page_content_type(client):
    res = client.get('/reviews')
    assert 'text/html' in res.content_type

def test_reviews_page_sort_rating(client):
    res = client.get('/reviews?sort=rating')
    assert res.status_code == 200

def test_reviews_page_sort_alpha(client):
    res = client.get('/reviews?sort=alpha')
    assert res.status_code == 200

def test_reviews_page_sort_invalid(client):
    res = client.get('/reviews?sort=invalid')
    assert res.status_code == 200

def test_reviews_page_sort_rating_returns_html(client):
    res = client.get('/reviews?sort=rating')
    assert b'<html' in res.data

def test_reviews_page_sort_alpha_returns_html(client):
    res = client.get('/reviews?sort=alpha')
    assert b'<html' in res.data

def test_reviews_page_sort_rating_not_empty(client):
    res = client.get('/reviews?sort=rating')
    assert len(res.data) > 0

def test_reviews_page_sort_alpha_not_empty(client):
    res = client.get('/reviews?sort=alpha')
    assert len(res.data) > 0

# ====== INDIVIDUAL REVIEW PAGE ====== #
def test_review_page_valid(client):
    res = client.get('/restaurant/review/Monkeypod Kitchen')
    assert res.status_code == 200

def test_review_page_valid_deck(client):
    res = client.get('/restaurant/review/Deck.')
    assert res.status_code == 200

def test_review_page_invalid_returns_404(client):
    res = client.get('/restaurant/review/FakeRestaurant999')
    assert res.status_code == 404

def test_review_page_valid_returns_html(client):
    res = client.get('/restaurant/review/Monkeypod Kitchen')
    assert b'<html' in res.data

def test_review_page_valid_not_empty(client):
    res = client.get('/restaurant/review/Monkeypod Kitchen')
    assert len(res.data) > 0

# ====== PREFERENCES PAGE ====== #
def test_preferences_page_status(client):
    res = client.get('/preferences')
    assert res.status_code == 200

def test_preferences_page_returns_html(client):
    res = client.get('/preferences')
    assert b'<html' in res.data

def test_preferences_page_not_empty(client):
    res = client.get('/preferences')
    assert len(res.data) > 0

def test_preferences_page_content_type(client):
    res = client.get('/preferences')
    assert 'text/html' in res.content_type

# ====== FILTER: Location ====== #
def test_filter_location_honolulu(client):
    res = client.get('/restaurants?place=Honolulu')
    assert res.status_code == 200

def test_filter_location_kapolei(client):
    res = client.get('/restaurants?place=Kapolei')
    assert res.status_code == 200

def test_filter_location_waikiki(client):
    res = client.get('/restaurants?place=Waikiki')
    assert res.status_code == 200

def test_filter_location_kailua(client):
    res = client.get('/restaurants?place=Kailua')
    assert res.status_code == 200

def test_filter_location_pearl_city(client):
    res = client.get('/restaurants?place=Pearl City')
    assert res.status_code == 200

def test_filter_location_mililani(client):
    res = client.get('/restaurants?place=Mililani')
    assert res.status_code == 200

def test_filter_location_invalid(client):
    res = client.get('/restaurants?place=FakeCity')
    assert res.status_code == 200

def test_filter_location_returns_html(client):
    res = client.get('/restaurants?place=Honolulu')
    assert b'<html' in res.data

def test_filter_location_not_empty(client):
    res = client.get('/restaurants?place=Honolulu')
    assert len(res.data) > 0

# ====== FILTER: Category ====== #
def test_filter_cat_hawaiian(client):
    res = client.get('/restaurants?cats=Hawaiian')
    assert res.status_code == 200

def test_filter_cat_seafood(client):
    res = client.get('/restaurants?cats=Seafood')
    assert res.status_code == 200

def test_filter_cat_pizza(client):
    res = client.get('/restaurants?cats=Pizza')
    assert res.status_code == 200

def test_filter_cat_tacos(client):
    res = client.get('/restaurants?cats=Tacos')
    assert res.status_code == 200

def test_filter_cat_japanese(client):
    res = client.get('/restaurants?cats=Japanese')
    assert res.status_code == 200

def test_filter_cat_american(client):
    res = client.get('/restaurants?cats=American')
    assert res.status_code == 200

def test_filter_cat_cocktail_bars(client):
    res = client.get('/restaurants?cats=Cocktail Bars')
    assert res.status_code == 200

def test_filter_cat_invalid(client):
    res = client.get('/restaurants?cats=FakeCategory')
    assert res.status_code == 200

def test_filter_cat_returns_html(client):
    res = client.get('/restaurants?cats=Hawaiian')
    assert b'<html' in res.data

def test_filter_cat_not_empty(client):
    res = client.get('/restaurants?cats=Hawaiian')
    assert len(res.data) > 0

# ====== FILTER: Multiple Categories ====== #
def test_filter_multi_cat_hawaiian_seafood(client):
    res = client.get('/restaurants?cats=Hawaiian&cats=Seafood')
    assert res.status_code == 200

def test_filter_multi_cat_pizza_tacos(client):
    res = client.get('/restaurants?cats=Pizza&cats=Tacos')
    assert res.status_code == 200

def test_filter_multi_cat_returns_html(client):
    res = client.get('/restaurants?cats=Hawaiian&cats=Seafood')
    assert b'<html' in res.data

def test_filter_multi_cat_not_empty(client):
    res = client.get('/restaurants?cats=Hawaiian&cats=Seafood')
    assert len(res.data) > 0

# ====== FILTER: Location + Category Combined ====== #
def test_filter_location_and_cat(client):
    res = client.get('/restaurants?place=Honolulu&cats=Hawaiian')
    assert res.status_code == 200

def test_filter_location_and_cat_returns_html(client):
    res = client.get('/restaurants?place=Honolulu&cats=Hawaiian')
    assert b'<html' in res.data

def test_filter_location_and_multi_cat(client):
    res = client.get('/restaurants?place=Honolulu&cats=Hawaiian&cats=Seafood')
    assert res.status_code == 200

# =============================================================================
# API ROUTES — RESTAURANTS
# =============================================================================

# --- GET /api/restaurants ---
def test_api_restaurants_status(client):
    res = client.get('/api/restaurants')
    assert res.status_code == 200

def test_api_restaurants_returns_list(client):
    res = client.get('/api/restaurants')
    assert isinstance(res.json, list)

def test_api_restaurants_not_empty(client):
    res = client.get('/api/restaurants')
    assert len(res.json) > 0

def test_api_restaurants_first_item_is_dict(client):
    res = client.get('/api/restaurants')
    assert isinstance(res.json[0], dict)

def test_api_restaurants_has_name(client):
    res = client.get('/api/restaurants')
    assert 'name' in res.json[0]

def test_api_restaurants_has_rating(client):
    res = client.get('/api/restaurants')
    assert 'rating' in res.json[0]

def test_api_restaurants_has_price(client):
    res = client.get('/api/restaurants')
    assert 'price' in res.json[0]

def test_api_restaurants_has_address(client):
    res = client.get('/api/restaurants')
    assert 'location' in res.json[0]

def test_api_restaurants_has_image_url(client):
    res = client.get('/api/restaurants')
    assert 'image_url' in res.json[0]

def test_api_restaurants_has_display_phone(client):
    res = client.get('/api/restaurants')
    assert 'display_phone' in res.json[0]

def test_api_restaurants_has_menu_url(client):
    res = client.get('/api/restaurants')
    assert 'menu_url' in res.json[0]

def test_api_restaurants_has_locator(client):
    res = client.get('/api/restaurants')
    assert 'locator' in res.json[0]

def test_api_restaurants_has_coordinates(client):
    res = client.get('/api/restaurants')
    assert 'coordinates' in res.json[0]

def test_api_restaurants_name_is_string(client):
    res = client.get('/api/restaurants')
    assert isinstance(res.json[0]['name'], str)

def test_api_restaurants_rating_is_number(client):
    res = client.get('/api/restaurants')
    assert isinstance(res.json[0]['rating'], (int, float))

def test_api_restaurants_count(client):
    res = client.get('/api/restaurants')
    assert len(res.json) > 100