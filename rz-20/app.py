from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import brotli
import hashlib
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rz20.db'
db = SQLAlchemy(app)

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=False)
    compressed_data = db.Column(db.LargeBinary, nullable=False)
    nonce = db.Column(db.Integer, nullable=False)
    hash = db.Column(db.String(64), nullable=False)
    reward = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

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
    compressed_data = brotli.compress(data.encode('utf-8'))
    hash_value = hashlib.sha256((data + str(nonce)).encode('utf-8')).hexdigest()
    reward = len(compressed_data) / 1024 * 10
    block = Block(data=data, compressed_data=compressed_data, nonce=nonce, hash=hash_value, reward=reward)
    db.session.add(block)
    db.session.commit()
    return jsonify({'message': 'Block created', 'block': block.id})

@app.route('/blocks', methods=['GET'])
def get_blocks():
    blocks = Block.query.all()
    return jsonify([{'id': block.id, 'data': block.data, 'compressed_data': len(block.compressed_data), 'nonce': block.nonce, 'hash': block.hash, 'reward': block.reward} for block in blocks])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trigger', methods=['POST'])
def trigger_block():
    bitcoin_data = fetch_bitcoin_data()
    block_height = bitcoin_data['height']
    nonce = int(block_height)  # Use block height as a nonce for simplicity
    data = f"Bitcoin Block Height: {block_height}"
    compressed_data = brotli.compress(data.encode('utf-8'))
    hash_value = hashlib.sha256((data + str(nonce)).encode('utf-8')).hexdigest()
    reward = len(compressed_data) / 1024 * 10
    block = Block(data=data, compressed_data=compressed_data, nonce=nonce, hash=hash_value, reward=reward)
    db.session.add(block)
    db.session.commit()
    return jsonify({'message': 'RIZZ Block created', 'block': block.id})

if __name__ == '__main__':
    app.run(debug=True)
