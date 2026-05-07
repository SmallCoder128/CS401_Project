# API Documentation

**Oahu Restaurant Finder**  
Base URL: `http://localhost:5000`

> All data is currently sourced from CSV files. POST and DELETE operations are in-memory only and are not persisted after the server stops.

---

## Table of Contents

- [Restaurants](#restaurants)
- [Reviews](#reviews)
- [Preferences](#preferences)

---

## Restaurants

### `GET /api/restaurants`
Returns all restaurants.
 
> **Note:** The API returns all available fields from the dataset. The website currently uses: `name`, `location.display_address`, `display_phone`, `image_url`, `menu_url`, `price`, `rating`, `coordinates`, and `locator`.
 
**Response:** `200 OK`
<details>
<summary><b>Click to expand full response</b></summary>
  
```json
[
  {
    "Unnamed: 0": 0,
    "Unnamed: 0.1": 0,
    "alias": "monkeypod-kitchen-honolulu-3",
    "attributes": {
      "business_temp_closed": null,
      "menu_url": "http://www.monkeypodkitchen.com/dine_ka_waikiki",
      "open24_hours": null,
      "waitlist_reservation": null
    },
    "business_hours": "[{'open': [{'is_overnight': False, 'start': '0700', 'end': '2300', 'day': 0}, ...], 'hours_type': 'REGULAR', 'is_open_now': True}]",
    "categories": "[{'alias': 'tacos', 'title': 'Tacos'}, {'alias': 'pizza', 'title': 'Pizza'}, {'alias': 'cocktailbars', 'title': 'Cocktail Bars'}]",
    "coordinates": {
      "latitude": 21.27851981119552,
      "longitude": -157.83271429964927
    },
    "display_phone": "(808) 900-4226",
    "distance": 3986.6042452641686,
    "hours_day": [[0, "0700", "2300"], [1, "0700", "2300"], [2, "0700", "2300"], [3, "0700", "2300"], [4, "0700", "2300"], [5, "0700", "2300"], [6, "0700", "2300"]],
    "id": "jUdUpuc9jZ0V33m4pyrgJQ",
    "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/M3D7kz-JbfDPrLdSiqjzIg/o.jpg",
    "is_closed": false,
    "location": {
      "address1": "2169 Kālia Rd",
      "address2": "Unit 111",
      "address3": null,
      "city": "Honolulu",
      "country": "US",
      "display_address": ["2169 Kālia Rd", "Unit 111", "Honolulu, HI 96815"],
      "state": "HI",
      "zip_code": "96815"
    },
    "locator": "Honolulu",
    "menu_url": "http://www.monkeypodkitchen.com/dine_ka_waikiki",
    "name": "Monkeypod Kitchen",
    "phone": 18089004226.0,
    "price": "$$",
    "rating": 4.3,
    "review_count": 1761,
    "transactions": "[]",
    "url": "https://www.yelp.com/biz/monkeypod-kitchen-honolulu-3?..."
  },
  ...
]
```
</details>

---

### `GET /api/restaurants/<name>`
Returns a single restaurant by name.

**URL Parameter:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `string` | The name of the restaurant |

**Response:** `200 OK`

<details>
<summary><b>Click to expand full response</b></summary>
  
```json
{
  "Unnamed: 0": 0,
  "Unnamed: 0.1": 0,
  "alias": "monkeypod-kitchen-honolulu-3",
  "attributes": {
    "business_temp_closed": null,
    "menu_url": "http://www.monkeypodkitchen.com/dine_ka_waikiki",
    "open24_hours": null,
    "waitlist_reservation": null
  },
  "business_hours": "[{'open': [{'is_overnight': False, 'start': '0700', 'end': '2300', 'day': 0}, ...], 'hours_type': 'REGULAR', 'is_open_now': True}]",
  "categories": "[{'alias': 'tacos', 'title': 'Tacos'}, {'alias': 'pizza', 'title': 'Pizza'}, {'alias': 'cocktailbars', 'title': 'Cocktail Bars'}]",
  "coordinates": {
    "latitude": 21.27851981119552,
    "longitude": -157.83271429964927
  },
  "display_phone": "(808) 900-4226",
  "distance": 3986.6042452641686,
  "hours_day": [[0, "0700", "2300"], [1, "0700", "2300"], [2, "0700", "2300"], [3, "0700", "2300"], [4, "0700", "2300"], [5, "0700", "2300"], [6, "0700", "2300"]],
  "id": "jUdUpuc9jZ0V33m4pyrgJQ",
  "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/M3D7kz-JbfDPrLdSiqjzIg/o.jpg",
  "is_closed": false,
  "location": {
    "address1": "2169 Kālia Rd",
    "address2": "Unit 111",
    "address3": null,
    "city": "Honolulu",
    "country": "US",
    "display_address": ["2169 Kālia Rd", "Unit 111", "Honolulu, HI 96815"],
    "state": "HI",
    "zip_code": "96815"
  },
  "locator": "Honolulu",
  "menu_url": "http://www.monkeypodkitchen.com/dine_ka_waikiki",
  "name": "Monkeypod Kitchen",
  "phone": 18089004226.0,
  "price": "$$",
  "rating": 4.3,
  "review_count": 1761,
  "transactions": "[]",
  "url": "https://www.yelp.com/biz/monkeypod-kitchen-honolulu-3?..."
}
```

</details>

**Response:** `404 Not Found`
```json
{ "error": "not found" }
```

---

### `POST /api/restaurants`
Adds a new restaurant to the in-memory dataset.

> **Note:** Changes are not persisted to the CSV file. <br>
> Also, since POST operations are in-memory only, a simplified `address` string is acceptable here. The full dataset uses a nested `location` object sourced from the Yelp API (e.g. `{ "display_address": [...], "city": "...", "state": "...", "zip_code": "..." }`).

**Request Body (JSON):**
| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Restaurant name |
| `address` | `string` | Street address |
| `locator` | `string` | City/area name |
| `display_phone` | `string` | Formatted phone number |
| `image_url` | `string` | URL to restaurant image |
| `menu_url` | `string` | URL to restaurant menu |
| `price` | `string` | Price range (e.g. `$`, `$$`) |
| `rating` | `float` | Rating out of 5 |
| `coordinates` | `dict` | `{ "latitude": float, "longitude": float }` |

```json
{
  "name": "New Restaurant",
  "address": "123 Main St, Honolulu, HI 96815",
  "locator": "Honolulu",
  "display_phone": "(808) 000-0000",
  "image_url": "https://...",
  "menu_url": "https://...",
  "price": "$",
  "rating": 4.0,
  "coordinates": { "latitude": 21.30, "longitude": -157.85 }
}
```

**Response:** `201 Created`
```json
{ "message": "restaurant added (in-memory only)" }
```

---

### `DELETE /api/restaurants/<name>`
Deletes a restaurant by name from the in-memory dataset.

> **Note:** Changes are not persisted to the CSV file.

**URL Parameter:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `string` | The name of the restaurant to delete |

**Response:** `200 OK`
```json
{ "message": "Monkeypod Kitchen deleted (not saved)" }
```

---

## Reviews

### `GET /api/reviews`
Returns all reviews.

**Response:** `200 OK`
```json
[
  {
    "name": "Monkeypod Kitchen",
    "review1": "A fantastic dining experience...",
    "review2": "Solid neighborhood spot...",
    "review3": "One of our regular spots..."
  },
  ...
]
```

---

### `GET /api/reviews/<name>`
Returns reviews for a specific restaurant.

**URL Parameter:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `string` | The name of the restaurant |

**Response:** `200 OK`
```json
[
  {
    "name": "Monkeypod Kitchen",
    "review1": "A fantastic dining experience...",
    "review2": "Solid neighborhood spot...",
    "review3": "One of our regular spots..."
  }
]
```

---

### `POST /api/reviews`
Adds a new review record to the in-memory dataset.

> **Note:** Changes are not persisted to the CSV file.

**Request Body (JSON):**
| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | The name of the restaurant |
| `review1` | `string` | First review text |
| `review2` | `string` | Second review text |
| `review3` | `string` | Third review text |

```json
{
  "name": "New Restaurant",
  "review1": "Amazing food and great vibes!",
  "review2": "Would definitely come back.",
  "review3": "One of the best spots on the island."
}
```

**Response:** `201 Created`
```json
{ "message": "review added (in-memory only)" }
```

---

### `DELETE /api/reviews/<name>`
Deletes all reviews for a specific restaurant from the in-memory dataset.

> **Note:** Changes are not persisted to the CSV file.

**URL Parameter:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `string` | The name of the restaurant whose reviews should be deleted |

**Response:** `200 OK`
```json
{ "message": "review deleted" }
```

---

## Preferences

### `GET /api/preferences`
Returns all restaurant preference records.

**Response:** `200 OK`
```json
[
  {
    "name": "Monkeypod Kitchen",
    "alias": "monkeypod-kitchen-honolulu-3",
    "cats": ["Tacos", "Pizza", "Cocktail Bars"]
  },
  ...
]
```

---

### `GET /api/preferences/cats`
Returns a list of all unique food category tags across all restaurants.

**Response:** `200 OK`
```json
["Tacos", "Pizza", "Cocktail Bars", "Hawaiian", "Seafood", ...]
```

---

### `POST /api/preferences`
Adds a new preference record to the in-memory dataset.

> **Note:** Changes are not persisted to the CSV file.

**Request Body (JSON):**
| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | The name of the restaurant |
| `alias` | `string` | Yelp-style URL slug for the restaurant |
| `cats` | `list[string]` | List of food category tags |

```json
{
  "name": "New Restaurant",
  "alias": "new-restaurant-honolulu",
  "cats": ["Hawaiian", "Seafood"]
}
```

**Response:** `201 Created`
```json
{ "message": "preference added" }
```

---

### `DELETE /api/preferences/<name>`
Deletes a preference record by restaurant name from the in-memory dataset.

> **Note:** Changes are not persisted to the CSV file.

**URL Parameter:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `string` | The name of the restaurant to delete from preferences |

**Response:** `200 OK`
```json
{ "message": "preference deleted" }
```