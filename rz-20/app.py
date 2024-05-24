from flask import Flask, jsonify, request, render_template
import brotli
import hashlib
import requests

app = Flask(__name__)

# In-memory storage for blocks
blocks = []

def fetch_bitcoin_data():
    response = requests.get('https://blockstream.info/api/blocks/tip/height')
    block_height = response.text
    response = requests.get(f'https://blockstream.info/api/block-height/{block_height}')
    block_hash = response.text
    response = requests.get(f'https://blockstream.info/api/block/{block_hash}')
    block_data = response.json()
    return block_data

@app.route('/bitcoin', methods=['GET'])
def bitcoin():
    data = fetch_bitcoin_data()
    return jsonify(data)

@app.route('/blocks', methods=['POST'])
def create_block():
    data = request.json['data']
    nonce = request.json['nonce']
    miner_count = request.json['miner_count']
    compressed_data = brotli.compress(data.encode('utf-8'))
    hash_value = hashlib.sha256((data + str(nonce)).encode('utf-8')).hexdigest()
    reward = miner_count  # Flat rate of 1 RIZZ per miner
    block = {
        'id': len(blocks) + 1,
        'data': data,
        'compressed_data': compressed_data,
        'nonce': nonce,
        'hash': hash_value,
        'reward': reward,
        'miner_count': miner_count
    }
    blocks.append(block)
    return jsonify({'message': 'Block created', 'block': block['id']})

@app.route('/blocks', methods=['GET'])
def get_blocks():
    return jsonify([{
        'id': block['id'],
        'data': block['data'],
        'compressed_data': len(block['compressed_data']),
        'nonce': block['nonce'],
        'hash': block['hash'],
        'reward': block['reward'],
        'miner_count': block['miner_count']
    } for block in blocks])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trigger', methods=['POST'])
def trigger_block():
    bitcoin_data = fetch_bitcoin_data()
    block_height = bitcoin_data['height']
    nonce = int(block_height)  # Use block height as a nonce for simplicity
    data = f"Bitcoin Block Height: {block_height}"
    miner_count = 5  # Example: Assume 5 miners participated
    compressed_data = brotli.compress(data.encode('utf-8'))
    hash_value = hashlib.sha256((data + str(nonce)).encode('utf-8')).hexdigest()
    reward = miner_count  # Flat rate of 1 RIZZ per miner
    block = {
        'id': len(blocks) + 1,
        'data': data,
        'compressed_data': compressed_data,
        'nonce': nonce,
        'hash': hash_value,
        'reward': reward,
        'miner_count': miner_count
    }
    blocks.append(block)
    return jsonify({'message': 'RIZZ Block created', 'block': block['id']})

if __name__ == '__main__':
    app.run(debug=True)
