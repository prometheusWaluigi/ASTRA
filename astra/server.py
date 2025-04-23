import csv
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

CITY_CSV = os.path.join(os.path.dirname(__file__), 'data', 'worldcities.csv')

# Load cities into memory for fast lookup
def load_cities():
    cities = []
    with open(CITY_CSV, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cities.append(row)
    return cities

CITIES = load_cities()

@app.route('/city_search')
def city_search():
    country = request.args.get('country', '').lower()
    query = request.args.get('query', '').lower()
    results = []
    for city in CITIES:
        if country and city['country'].lower() != country:
            continue
        if query and not city['city'].lower().startswith(query):
            continue
        results.append({
            'city': city['city'],
            'country': city['country'],
            'lat': city['lat'],
            'lng': city['lng']
        })
        if len(results) >= 10:
            break
    return jsonify(results)

@app.route('/city_lookup')
def city_lookup():
    city_name = request.args.get('city', '').lower()
    country = request.args.get('country', '').lower()
    for city in CITIES:
        if city['city'].lower() == city_name and city['country'].lower() == country:
            return jsonify({
                'city': city['city'],
                'country': city['country'],
                'lat': city['lat'],
                'lng': city['lng']
            })
    return jsonify({'error': 'City not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
