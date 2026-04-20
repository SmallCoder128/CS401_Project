import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

def get_data():
    '''
    Load restaurant data from a CSV file.
    '''
    data = pd.read_csv('restaurants.csv')
    return data

def index():
    return render_template("index.html")

def locator_list():
    data = get_data()
    locators = data['Locator'].unique().tolist()
    return locators

@app.route('/')
def home():
    return render_template("index.html")
    

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    '''
    API endpoint to retrieve restaurant data.
    '''
    data = get_data()
    return data.to_dict('records')

@app.route('/restaurants', methods=["GET"])
def get_restaurants_page():
    '''
    Directory of restaurants.
    '''
    locators = locator_list()
    place = request.args.get('place')
    data = get_data()
    df = pd.DataFrame(data)

    df = df.drop(columns=['id'])

    if place:
        df = df[df['Locator'] == place]

    restaurants = df.to_dict(orient='records')

    return render_template(
        "restaurants.html",
        #tables=[df.to_html(classes='data')],
        restaurants=restaurants,
        titles=df.columns.values,
        locators=locators,
        selected_place=place)

@app.route('/restaurant/<name>')
def restaurant_detail(name):
    '''
    Returns individual restaurant page upon selection.
    '''
    return f"<h1>{name}</h1><p>Details coming soon...</p>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')