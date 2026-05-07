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

def test_home_contains_closing_tag(client):
    res = client.get('/')
    assert b'</html>' in res.data

def test_home_post_not_allowed(client):
    res = client.post('/')
    assert res.status_code == 405

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

def test_about_contains_closing_tag(client):
    res = client.get('/about')
    assert b'</html>' in res.data

def test_about_post_not_allowed(client):
    res = client.post('/about')
    assert res.status_code == 405

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

def test_restaurants_page_contains_closing_tag(client):
    res = client.get('/restaurants')
    assert b'</html>' in res.data

def test_restaurants_page_no_params(client):
    res = client.get('/restaurants?place=&cats=')
    assert res.status_code == 200

def test_restaurants_page_contains_monkeypod(client):
    res = client.get('/restaurants')
    assert b'Monkeypod Kitchen' in res.data

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

def test_restaurant_detail_valid_not_empty(client):
    res = client.get('/restaurant/Monkeypod Kitchen')
    assert len(res.data) > 0

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
    assert len(res.data) > 100

def test_review_page_contains_restaurant_name(client):
    res = client.get('/restaurant/review/Monkeypod Kitchen')
    assert b'Monkeypod Kitchen' in res.data

def test_review_page_deck_contains_name(client):
    res = client.get('/restaurant/review/Deck.')
    assert b'Deck.' in res.data

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

def test_preferences_page_post_not_allowed(client):
    res = client.post('/preferences')
    assert res.status_code == 405

# ====== FILTER: LOCATION ====== #
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

# ====== FILTER: CATEGORY ====== #
def test_filter_cat_hawaiian(client):
    res = client.get('/restaurants?cats=Hawaiian')
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

# ====== FILTER: MULTIPLE CATEGORIES ====== #
def test_filter_multi_cat_hawaiian_seafood(client):
    res = client.get('/restaurants?cats=Hawaiian&cats=Seafood')
    assert res.status_code == 200

def test_filter_multi_cat_pizza_tacos(client):
    res = client.get('/restaurants?cats=Pizza&cats=Tacos')
    assert res.status_code == 200

def test_filter_multi_cat_returns_html(client):
    res = client.get('/restaurants?cats=Hawaiian&cats=Seafood')
    assert b'<html' in res.data

# ====== FILTER: LOCATION + CATEGORY ====== #
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

# ====== GET /api/restaurants ====== #
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

# ====== GET /api/restaurants/<name> ====== #
def test_api_get_restaurant_valid(client):
    res = client.get('/api/restaurants/Monkeypod Kitchen')
    assert res.status_code == 200

def test_api_get_restaurant_valid_deck(client):
    res = client.get('/api/restaurants/Deck.')
    assert res.status_code == 200

def test_api_get_restaurant_returns_dict(client):
    res = client.get('/api/restaurants/Monkeypod Kitchen')
    assert isinstance(res.json, dict)

def test_api_get_restaurant_correct_name(client):
    res = client.get('/api/restaurants/Monkeypod Kitchen')
    assert res.json['name'] == 'Monkeypod Kitchen'

def test_api_get_restaurant_has_rating(client):
    res = client.get('/api/restaurants/Monkeypod Kitchen')
    assert 'rating' in res.json

def test_api_get_restaurant_has_address(client):
    res = client.get('/api/restaurants/Monkeypod Kitchen')
    assert 'location' in res.json

def test_api_get_restaurant_has_price(client):
    res = client.get('/api/restaurants/Monkeypod Kitchen')
    assert 'price' in res.json

def test_api_get_restaurant_has_image_url(client):
    res = client.get('/api/restaurants/Monkeypod Kitchen')
    assert 'image_url' in res.json

def test_api_get_restaurant_has_display_phone(client):
    res = client.get('/api/restaurants/Monkeypod Kitchen')
    assert 'display_phone' in res.json

def test_api_get_restaurant_has_menu_url(client):
    res = client.get('/api/restaurants/Monkeypod Kitchen')
    assert 'menu_url' in res.json

def test_api_get_restaurant_has_locator(client):
    res = client.get('/api/restaurants/Monkeypod Kitchen')
    assert 'locator' in res.json

def test_api_get_restaurant_has_coordinates(client):
    res = client.get('/api/restaurants/Monkeypod Kitchen')
    assert 'coordinates' in res.json

def test_api_get_restaurant_deck_correct_name(client):
    res = client.get('/api/restaurants/Deck.')
    assert res.json['name'] == 'Deck.'

def test_api_get_restaurant_invalid_404(client):
    res = client.get('/api/restaurants/FakeRestaurant999')
    assert res.status_code == 404

def test_api_get_restaurant_invalid_error_key(client):
    res = client.get('/api/restaurants/FakeRestaurant999')
    assert 'error' in res.json

def test_api_get_restaurant_invalid_returns_dict(client):
    res = client.get('/api/restaurants/FakeRestaurant999')
    assert isinstance(res.json, dict)

# ====== POST /api/restaurants ====== #
def test_api_post_restaurant_status(client):
    res = client.post('/api/restaurants', json={"name": "Test Place", "rating": 4.0})
    assert res.status_code == 201

def test_api_post_restaurant_returns_message(client):
    res = client.post('/api/restaurants', json={"name": "Test Place"})
    assert 'message' in res.json

def test_api_post_restaurant_message_is_string(client):
    res = client.post('/api/restaurants', json={"name": "Test Place"})
    assert isinstance(res.json['message'], str)

def test_api_post_restaurant_full_payload(client):
    res = client.post('/api/restaurants', json={
        "name": "Test Place",
        "location": "123 Test St",
        "locator": "Honolulu",
        "display_phone": "(808) 000-0000",
        "image_url": "https://example.com/img.jpg",
        "menu_url": "https://example.com/menu",
        "price": "$",
        "rating": 4.2,
        "coordinates": {"latitude": 21.30, "longitude": -157.85}
    })
    assert res.status_code == 201

def test_api_post_restaurant_empty_payload(client):
    res = client.post('/api/restaurants', json={})
    assert res.status_code == 201

def test_api_post_restaurant_response_is_json(client):
    res = client.post('/api/restaurants', json={"name": "Test Place"})
    assert res.is_json

# ====== DELETE /api/restaurants/<name> ====== #
def test_api_delete_restaurant_status(client):
    res = client.delete('/api/restaurants/Monkeypod Kitchen')
    assert res.status_code == 200

def test_api_delete_restaurant_returns_message(client):
    res = client.delete('/api/restaurants/Monkeypod Kitchen')
    assert 'message' in res.json

def test_api_delete_restaurant_message_is_string(client):
    res = client.delete('/api/restaurants/Monkeypod Kitchen')
    assert isinstance(res.json['message'], str)

def test_api_delete_restaurant_invalid_name(client):
    res = client.delete('/api/restaurants/FakeRestaurant999')
    assert res.status_code == 200

def test_api_delete_restaurant_invalid_returns_message(client):
    res = client.delete('/api/restaurants/FakeRestaurant999')
    assert 'message' in res.json

def test_api_delete_restaurant_response_is_json(client):
    res = client.delete('/api/restaurants/Monkeypod Kitchen')
    assert res.is_json

def test_api_delete_wrong_method_restaurants(client):
    res = client.delete('/api/restaurants')
    assert res.status_code == 405

# =============================================================================
# API ROUTES — REVIEWS
# =============================================================================

# ====== GET /api/reviews ====== #
def test_api_reviews_status(client):
    res = client.get('/api/reviews')
    assert res.status_code == 200

def test_api_reviews_returns_list(client):
    res = client.get('/api/reviews')
    assert isinstance(res.json, list)

def test_api_reviews_not_empty(client):
    res = client.get('/api/reviews')
    assert len(res.json) > 0

def test_api_reviews_first_item_is_dict(client):
    res = client.get('/api/reviews')
    assert isinstance(res.json[0], dict)

def test_api_reviews_has_name(client):
    res = client.get('/api/reviews')
    assert 'name' in res.json[0]

def test_api_reviews_has_review1(client):
    res = client.get('/api/reviews')
    assert 'review1' in res.json[0]

def test_api_reviews_has_review2(client):
    res = client.get('/api/reviews')
    assert 'review2' in res.json[0]

def test_api_reviews_has_review3(client):
    res = client.get('/api/reviews')
    assert 'review3' in res.json[0]

def test_api_reviews_name_is_string(client):
    res = client.get('/api/reviews')
    assert isinstance(res.json[0]['name'], str)

def test_api_reviews_review1_is_string(client):
    res = client.get('/api/reviews')
    assert isinstance(res.json[0]['review1'], str)

def test_api_reviews_review2_is_string(client):
    res = client.get('/api/reviews')
    assert isinstance(res.json[0]['review2'], str)

def test_api_reviews_review3_is_string(client):
    res = client.get('/api/reviews')
    assert isinstance(res.json[0]['review3'], str)

def test_api_reviews_count(client):
    res = client.get('/api/reviews')
    assert len(res.json) > 100

def test_api_reviews_content_type(client):
    res = client.get('/api/reviews')
    assert 'application/json' in res.content_type

def test_api_reviews_response_is_json(client):
    res = client.get('/api/reviews')
    assert res.is_json

def test_api_reviews_all_have_name(client):
    res = client.get('/api/reviews')
    for r in res.json:
        assert 'name' in r

def test_api_reviews_all_have_review1(client):
    res = client.get('/api/reviews')
    for r in res.json:
        assert 'review1' in r

def test_api_reviews_all_have_review2(client):
    res = client.get('/api/reviews')
    for r in res.json:
        assert 'review2' in r

def test_api_reviews_all_have_review3(client):
    res = client.get('/api/reviews')
    for r in res.json:
        assert 'review3' in r

# ====== GET /api/reviews/<name> ====== #
def test_api_get_reviews_by_name_valid(client):
    res = client.get('/api/reviews/Monkeypod Kitchen')
    assert res.status_code == 200

def test_api_get_reviews_by_name_valid_deck(client):
    res = client.get('/api/reviews/Deck.')
    assert res.status_code == 200

def test_api_get_reviews_by_name_returns_list(client):
    res = client.get('/api/reviews/Monkeypod Kitchen')
    assert isinstance(res.json, list)

def test_api_get_reviews_by_name_not_empty(client):
    res = client.get('/api/reviews/Monkeypod Kitchen')
    assert len(res.json) > 0

def test_api_get_reviews_by_name_correct_name(client):
    res = client.get('/api/reviews/Monkeypod Kitchen')
    assert res.json[0]['name'] == 'Monkeypod Kitchen'

def test_api_get_reviews_by_name_has_review1(client):
    res = client.get('/api/reviews/Monkeypod Kitchen')
    assert 'review1' in res.json[0]

def test_api_get_reviews_by_name_has_review2(client):
    res = client.get('/api/reviews/Monkeypod Kitchen')
    assert 'review2' in res.json[0]

def test_api_get_reviews_by_name_has_review3(client):
    res = client.get('/api/reviews/Monkeypod Kitchen')
    assert 'review3' in res.json[0]

def test_api_get_reviews_by_name_invalid_status(client):
    res = client.get('/api/reviews/FakeRestaurant999')
    assert res.status_code == 200

def test_api_get_reviews_by_name_invalid_returns_list(client):
    res = client.get('/api/reviews/FakeRestaurant999')
    assert isinstance(res.json, list)

def test_api_get_reviews_by_name_invalid_empty_list(client):
    res = client.get('/api/reviews/FakeRestaurant999')
    assert len(res.json) == 0

# ====== POST /api/reviews ====== #
def test_api_post_review_status(client):
    res = client.post('/api/reviews', json={
        "name": "Test Place",
        "review1": "Great!",
        "review2": "Loved it.",
        "review3": "Will return."
    })
    assert res.status_code == 201

def test_api_post_review_returns_message(client):
    res = client.post('/api/reviews', json={"name": "Test Place"})
    assert 'message' in res.json

def test_api_post_review_message_is_string(client):
    res = client.post('/api/reviews', json={"name": "Test Place"})
    assert isinstance(res.json['message'], str)

def test_api_post_review_empty_payload(client):
    res = client.post('/api/reviews', json={})
    assert res.status_code == 201

def test_api_post_review_full_payload(client):
    res = client.post('/api/reviews', json={
        "name": "Test Place",
        "review1": "Amazing food.",
        "review2": "Great service.",
        "review3": "Would come back."
    })
    assert res.status_code == 201

def test_api_post_review_response_is_json(client):
    res = client.post('/api/reviews', json={"name": "Test Place"})
    assert res.is_json

# ====== DELETE /api/reviews/<name> ====== #
def test_api_delete_review_status(client):
    res = client.delete('/api/reviews/Monkeypod Kitchen')
    assert res.status_code == 200

def test_api_delete_review_returns_message(client):
    res = client.delete('/api/reviews/Monkeypod Kitchen')
    assert 'message' in res.json

def test_api_delete_review_message_is_string(client):
    res = client.delete('/api/reviews/Monkeypod Kitchen')
    assert isinstance(res.json['message'], str)

def test_api_delete_review_invalid_name(client):
    res = client.delete('/api/reviews/FakeRestaurant999')
    assert res.status_code == 200

def test_api_delete_review_invalid_returns_message(client):
    res = client.delete('/api/reviews/FakeRestaurant999')
    assert 'message' in res.json

# =============================================================================
# API ROUTES — PREFERENCES
# =============================================================================

# ====== GET /api/preferences ====== #
def test_api_preferences_status(client):
    res = client.get('/api/preferences')
    assert res.status_code == 200

def test_api_preferences_returns_list(client):
    res = client.get('/api/preferences')
    assert isinstance(res.json, list)

def test_api_preferences_not_empty(client):
    res = client.get('/api/preferences')
    assert len(res.json) > 0

def test_api_preferences_first_item_is_dict(client):
    res = client.get('/api/preferences')
    assert isinstance(res.json[0], dict)

def test_api_preferences_has_name(client):
    res = client.get('/api/preferences')
    assert 'name' in res.json[0]

def test_api_preferences_has_alias(client):
    res = client.get('/api/preferences')
    assert 'alias' in res.json[0]

def test_api_preferences_has_cats(client):
    res = client.get('/api/preferences')
    assert 'cats' in res.json[0]

def test_api_preferences_name_is_string(client):
    res = client.get('/api/preferences')
    assert isinstance(res.json[0]['name'], str)

def test_api_preferences_alias_is_string(client):
    res = client.get('/api/preferences')
    assert isinstance(res.json[0]['alias'], str)

def test_api_preferences_count(client):
    res = client.get('/api/preferences')
    assert len(res.json) > 100

def test_api_preferences_content_type(client):
    res = client.get('/api/preferences')
    assert 'application/json' in res.content_type

def test_api_preferences_response_is_json(client):
    res = client.get('/api/preferences')
    assert res.is_json

def test_api_preferences_all_have_name(client):
    res = client.get('/api/preferences')
    for r in res.json:
        assert 'name' in r

def test_api_preferences_all_have_alias(client):
    res = client.get('/api/preferences')
    for r in res.json:
        assert 'alias' in r

def test_api_preferences_all_have_cats(client):
    res = client.get('/api/preferences')
    for r in res.json:
        assert 'cats' in r

# ====== GET /api/preferences/cats ====== #
def test_api_cats_status(client):
    res = client.get('/api/preferences/cats')
    assert res.status_code == 200

def test_api_cats_returns_list(client):
    res = client.get('/api/preferences/cats')
    assert isinstance(res.json, list)

def test_api_cats_not_empty(client):
    res = client.get('/api/preferences/cats')
    assert len(res.json) > 0

def test_api_cats_first_item_is_string(client):
    res = client.get('/api/preferences/cats')
    assert isinstance(res.json[0], str)

def test_api_cats_contains_hawaiian(client):
    res = client.get('/api/preferences/cats')
    assert 'Hawaiian' in res.json

def test_api_cats_contains_cocktail_bars(client):
    res = client.get('/api/preferences/cats')
    assert 'Cocktail Bars' in res.json

def test_api_cats_no_duplicates(client):
    res = client.get('/api/preferences/cats')
    assert len(res.json) == len(set(res.json))

def test_api_cats_content_type(client):
    res = client.get('/api/preferences/cats')
    assert 'application/json' in res.content_type

def test_api_cats_response_is_json(client):
    res = client.get('/api/preferences/cats')
    assert res.is_json

# ====== POST /api/preferences ====== #
def test_api_post_preference_status(client):
    res = client.post('/api/preferences', json={
        "name": "Test Place",
        "alias": "test-place-honolulu",
        "cats": ["Hawaiian", "Seafood"]
    })
    assert res.status_code == 201

def test_api_post_preference_returns_message(client):
    res = client.post('/api/preferences', json={"name": "Test Place"})
    assert 'message' in res.json

def test_api_post_preference_message_is_string(client):
    res = client.post('/api/preferences', json={"name": "Test Place"})
    assert isinstance(res.json['message'], str)

def test_api_post_preference_empty_payload(client):
    res = client.post('/api/preferences', json={})
    assert res.status_code == 201

def test_api_post_preference_full_payload(client):
    res = client.post('/api/preferences', json={
        "name": "Test Place",
        "alias": "test-place-honolulu",
        "cats": ["Hawaiian", "Seafood", "Cocktail Bars"]
    })
    assert res.status_code == 201

def test_api_post_preference_response_is_json(client):
    res = client.post('/api/preferences', json={"name": "Test Place"})
    assert res.is_json

# ====== DELETE /api/preferences/<name> ====== #
def test_api_delete_preference_status(client):
    res = client.delete('/api/preferences/Monkeypod Kitchen')
    assert res.status_code == 200

def test_api_delete_preference_returns_message(client):
    res = client.delete('/api/preferences/Monkeypod Kitchen')
    assert 'message' in res.json

def test_api_delete_preference_message_is_string(client):
    res = client.delete('/api/preferences/Monkeypod Kitchen')
    assert isinstance(res.json['message'], str)

def test_api_delete_preference_invalid_name(client):
    res = client.delete('/api/preferences/FakeRestaurant999')
    assert res.status_code == 200

def test_api_delete_preference_invalid_returns_message(client):
    res = client.delete('/api/preferences/FakeRestaurant999')
    assert 'message' in res.json

def test_api_delete_preference_response_is_json(client):
    res = client.delete('/api/preferences/Monkeypod Kitchen')
    assert res.is_json

# =============================================================================
# EDGE CASES & MISC
# =============================================================================
 
# ====== NONEXISTENT ROUTES ====== #
def test_nonexistent_route(client):
    res = client.get('/nonexistent')
    assert res.status_code == 404
 
def test_nonexistent_api_route(client):
    res = client.get('/api/nonexistent')
    assert res.status_code == 404
 
def test_nonexistent_restaurant_api_sub_route(client):
    res = client.get('/api/restaurants/fake/extra')
    assert res.status_code == 404
 
def test_nonexistent_reviews_sub_route(client):
    res = client.get('/api/reviews/fake/extra')
    assert res.status_code == 404
 
# ====== WRONG HTTP METHODS ====== #
def test_api_delete_wrong_method_restaurants(client):
    res = client.delete('/api/restaurants')
    assert res.status_code == 405
 
def test_api_delete_wrong_method_reviews(client):
    res = client.delete('/api/reviews')
    assert res.status_code == 405
 
def test_api_delete_wrong_method_preferences(client):
    res = client.delete('/api/preferences')
    assert res.status_code == 405