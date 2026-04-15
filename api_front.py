import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

def get_data():
    '''
    Load restaurant data from a CSV file.
    '''
    data = pd.read_csv('/users/gener/Code/CS401_Project/restaurants.csv')
    return data

def index():
    return render_template("index.html")

def locator_list():
    data = get_data()
    locators = data['Locator'].unique().tolist()
    return locators

@app.route('/', methods=("POST", "GET"))
def home():
    data = get_data()
    df = pd.DataFrame(data)
    df = df.drop(columns=['id'])
    return render_template("index.html",
                            tables=[df.to_html(classes='data')], 
                            titles=df.columns.values, 
                            locators=locator_list(),
                            selected_place=None)
    

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    '''
    API endpoint to retrieve restaurant data.
    '''
    data = get_data()
    return data

@app.route('/restaurants', methods=["GET"])
def get_restaurants_page():
    locators = locator_list()
    place = request.args.get('place')
    data = get_data()
    df = pd.DataFrame(data)
    df = df[df['Locator'] == place]
    df = df.drop(columns=['id'])
    
    return render_template("index.html",
                             tables=[df.to_html(classes='data')],
                             titles=df.columns.values,
                             locators=locators,
                             selected_place=place)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')