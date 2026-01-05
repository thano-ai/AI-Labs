from flask import Flask, render_template, jsonify, request
from tsp_ga import genetic_algorithm
from cities import CITIES

app = Flask(__name__)

city_names = [city[0] for city in CITIES]
city_coords = [city[1] for city in CITIES]


@app.route('/')
def index():
    return render_template('index.html', cities=city_names)


@app.route('/api/cities')
def get_cities():
    return jsonify([{
        'name': name,
        'lat': coords[0],
        'lng': coords[1]
    } for name, coords in CITIES])


@app.route('/api/solve', methods=['POST'])
def solve_tsp():
    data = request.json

    params = {
        'population_size': 100,
        'generations': 200,
        'mutation_rate': 0.2,
        'elitism': 5,
        'use_roulette': data.get('selection_method', 'tournament') == 'roulette'
    }

    start_city = data.get('start_city')
    end_city = data.get('end_city')

    if start_city:
        params['start_city'] = city_names.index(start_city)
    if end_city:
        params['end_city'] = city_names.index(end_city)

    best_path, best_distance, gen_found = genetic_algorithm(
        city_coords,
        **params
    )

    path_with_names = [city_names[i] for i in best_path]

    return jsonify({
        'path': path_with_names,
        'distance': best_distance,
        'generation_found': gen_found,
        'path_indices': best_path
    })


if __name__ == '__main__':
    app.run(debug=True)