from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Load the JSON data
def load_games_data():
    try:
        with open('scraped_date_printstudios.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Get all games
@app.route('/games', methods=['GET'])
def get_all_games():
    games = load_games_data()
    return jsonify({
        'success': True,
        'count': len(games),
        'data': games
    })

# Get game by ID
@app.route('/games/<int:game_id>', methods=['GET'])
def get_game_by_id(game_id):
    games = load_games_data()
    
    # Find game by ID
    game = next((game for game in games if game.get('gameId') == game_id), None)
    
    if game:
        return jsonify({
            'success': True,
            'data': game
        })
    else:
        return jsonify({
            'success': False,
            'error': f'Game with ID {game_id} not found'
        }), 404

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API is running successfully'
    })

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Welcome to Print Studios Games API',
        'endpoints': {
            'all_games': '/games',
            'game_by_id': '/games/<id>',
            'health': '/health'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
