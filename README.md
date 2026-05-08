<!-- Improved compatibility of back to top link -->
<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
<!--[![project_license][license-shield]][license-url]-->

<br />
<div align="center">

<h1 align="center">Oahu Restaurant Finder</h1>

  <p align="center">
    A platform designed to help Oahu residents discover local restaurants, filter food options, and explore reviews.
    <br />
    <a href="https://github.com/SmallCoder128/CS401_Project"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/SmallCoder128/CS401_Project">View Demo</a>
    &middot;
    <a href="https://github.com/SmallCoder128/CS401_Project/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/SmallCoder128/CS401_Project/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

---

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <ul>
      <li><a href="#built-with">Built With</a></li>
      <li><a href="#repository-structure">Repository Structure</a></li>
    </ul>
    <li><a href="#group-members">Group Members</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#how-to-run">How to Run</a>
      <ul>
        <li><a href="#website">Website</a></li>
        <li><a href="#tests">Tests</a></li>
      </ul>
    </li>
    <li><a href="#api-documentation">API Documentation</a></li>
    <li><a href="#database">Database</a></li>
  </ol>
</details>

---

## About The Project

On Oahu, there are so many restaurant options that it can be difficult to decide where to go and what to eat.  
This website helps users navigate local dining by providing updated information on nearby establishments, food categories, and customer reviews.  
The system uses three connected models — **Restaurant Directory**, **Reviews**, and **Food Preferences** — to support browsing, filtering, and informed decision‑making.

This repository contains all development work for the project, including backend logic, database design, and frontend structure.

### Built With

[![Python][python-shield]][python-url]
[![Flask][flask-shield]][flask-url]
[![HTML][html-shield]][html-url]
[![CSS][css-shield]][css-url]
[![Bootstrap][bootstrap-shield]][bootstrap-url]
[![JavaScript][js-shield]][js-url]
[![Jinja2][jinja-shield]][jinja-url]

### Repository Structure

| Path | Description |
|------|-------------|
| `data/` | CSV files for restaurants, reviews, and preferences |
| `docs/` | UML diagram, report, presentation, and API documentation |
| `templates/` | Jinja2 HTML templates |
| `static/` | CSS stylesheets and images |
| `api_front.py` | Main Flask app — template routes and API endpoints |
| `data_utils.py` | Data loading and helper functions |
| `Dockerfile` | Docker image configuration |
| `Docker-compose.yml` | Docker Compose configuration |
| `requirements.txt` | Python dependencies |
| `test_app.py` | pytest test file |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Group Members

| Name | GitHub |
|------|--------|
| Calvin Small | [@SmallCoder128](https://github.com/SmallCoder128) |
| Vlad Tomutiu | [@vladtomutiu](https://github.com/vladtomutiu) |
| Ashley Sofia Alfaro | [@AshleySofiaAlfaro](https://github.com/AshleySofiaAlfaro) |
| Jayce Pascua | [@BraddahJayce](https://github.com/BraddahJayce) |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

### Prerequisites

Make sure you have the following installed:
 
- Python 3.9+
- pip
- Docker (for running via Docker)

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/SmallCoder128/CS401_Project.git
   cd CS401_Project
   ```
 
2. Create a virtual environment:
   **Windows:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
 
   **Mac/Linux:**
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```
 
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## How to Run

### Website

**Docker Compose**
```sh
docker compose up
```

**Example Output**
```sh
oahu-food-finder  |  * Serving Flask app 'api_front'
oahu-food-finder  |  * Debug mode: off
oahu-food-finder  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
oahu-food-finder  |  * Running on all addresses (0.0.0.0)
oahu-food-finder  |  * Running on http://127.0.0.1:5000
oahu-food-finder  |  * Running on http://172.21.0.2:5000
```

### Tests
Make sure you're still in `CS401_Project` directory before you run the tests:
```sh
pytest
```
`pytest` will automatically discover `test_app.py` and execute all 200 test cases.
 
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## API Documentation

Public API documentation is available here: **[API Docs](https://github.com/SmallCoder128/CS401_Project/blob/main/docs/api.md)**

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Database
 
This project uses CSV files as its data source (no live database). The data is loaded at runtime via pandas and served through the Flask API.
 
**Restaurant** — The main model, sourced from the Yelp API. Stores each restaurant's name, address, phone number, image, menu URL, price range, rating, and coordinates (~170 restaurants).
 
**Reviews** — One row per restaurant containing three pre-generated customer review snippets (`review1`, `review2`, `review3`). Linked to Restaurant by `name`.
 
**Preferences** — Stores each restaurant's Yelp category tags (e.g. `['Hawaiian', 'Seafood', 'Cocktail Bars']`) along with its alias. Used to support filtering by food category. Linked to Restaurant by `name`.
 
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- SHIELDS -->
[contributors-shield]: https://img.shields.io/github/contributors/SmallCoder128/CS401_Project.svg?style=for-the-badge
[contributors-url]: https://github.com/SmallCoder128/CS401_Project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/SmallCoder128/CS401_Project.svg?style=for-the-badge
[forks-url]: https://github.com/SmallCoder128/CS401_Project/network/members
[stars-shield]: https://img.shields.io/github/stars/SmallCoder128/CS401_Project.svg?style=for-the-badge
[stars-url]: https://github.com/SmallCoder128/CS401_Project/stargazers
[issues-shield]: https://img.shields.io/github/issues/SmallCoder128/CS401_Project.svg?style=for-the-badge
[issues-url]: https://github.com/SmallCoder128/CS401_Project/issues
[license-shield]: https://img.shields.io/github/license/SmallCoder128/CS401_Project.svg?style=for-the-badge
[license-url]: https://github.com/SmallCoder128/CS401_Project/blob/master/LICENSE.txt
 
<!-- TECH BADGES -->
[python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
[flask-shield]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[flask-url]: https://flask.palletsprojects.com/
[bootstrap-shield]: https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white
[bootstrap-url]: https://getbootstrap.com/
[js-shield]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[js-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript
[jinja-shield]: https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white
[jinja-url]: https://jinja.palletsprojects.com/
[html-shield]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
[html-url]: https://developer.mozilla.org/en-US/docs/Web/HTML
[css-shield]: https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white
[css-url]: https://developer.mozilla.org/en-US/docs/Web/CSS