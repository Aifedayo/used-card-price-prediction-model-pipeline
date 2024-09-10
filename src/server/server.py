from flask import Flask, jsonify, request
from flask_cors import CORS

import utils

app = Flask(__name__)
CORS(app)

@app.route('/object/<obj>/')
def get_objects_list(obj):
    objects_keys = utils.get_object_keys(obj)
    response = jsonify({
        'objects': objects_keys
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/column_name/<col_name>/dict_name/<dict_name>/key/<key>/')
def get_specific_objects_value(col_name, dict_name, key):
    object_value = utils.get_exact_value(col_name, dict_name, key)
    response = jsonify({
        key: object_value
    })
    response.headers.add('Access-Content-Allow-Origin', '*')
    return response

@app.route('/manufacturer/<manufacturer_name>/')
def fetch_manufacturer_models(manufacturer_name):
    manufacturer_list = utils.get_manufacturer_models(manufacturer_name)
    response = jsonify({
        manufacturer_name: manufacturer_list
    })
    response.headers.add('Access-Content-Allow-Origin', '*')
    return response

@app.route('/estimate-price', methods=['POST'])
def predict():
    if request.is_json:
        data = request.get_json()

        prediction = utils.predict_used_car_price(**data)
        
        response = jsonify({
            f'predicted_price': prediction
        })

        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Content-Type', 'application/json')
        return response
    else:
        # Handle the case where the Content-Type is not JSON
        return jsonify({'error': 'Invalid content type, please send application/json'}), 400
    
if __name__ == '__main__':
    print('Starting flask server for used car price prediction...')
    utils.load_artifacts()
    app.run(debug=True)
