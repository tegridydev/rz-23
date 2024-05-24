from flask import Flask, jsonify, request, render_template
import brotli
import hashlib
import requests
import subprocess
import json
import os

app = Flask(__name__)

# In-memory storage for blocks and proofs
blocks = []
proofs = []

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
    metadata = request.json['metadata']
    nft_info = request.json['nft_info']
    runes = request.json['runes']
    brc20 = request.json['brc20']
    
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
        'miner_count': miner_count,
        'metadata': metadata,
        'nft_info': nft_info,
        'runes': runes,
        'brc20': brc20,
        'zk_proof': {}
    }
    blocks.append(block)
    
    # Generate SNARK proof for the new block
    proof = generate_snark_proof(data, nonce)
    proofs.append(proof)
    
    # Update the block with the zk proof details
    block['zk_proof'] = {
        'recursive_proof': proof,
        'previous_proof_hash': hashlib.sha256(proofs[-1].encode('utf-8')).hexdigest() if len(proofs) > 1 else None
    }
    
    return jsonify({'message': 'Block created', 'block': block['id'], 'proof': proof})

@app.route('/blocks', methods=['GET'])
def get_blocks():
    return jsonify([{
        'id': block['id'],
        'data': block['data'],
        'compressed_data': len(block['compressed_data']),
        'nonce': block['nonce'],
        'hash': block['hash'],
        'reward': block['reward'],
        'miner_count': block['miner_count'],
        'metadata': block['metadata'],
        'nft_info': block['nft_info'],
        'runes': block['runes'],
        'brc20': block['brc20'],
        'zk_proof': block['zk_proof']
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
    metadata = "Additional metadata from inscriptions"
    nft_info = {
        "ordinal_id": "12345",
        "inscription_data": "Image data or other NFT information",
        "collection_standard": {
            "meta": {
                "description": "An amazing NFT collection",
                "discord_link": "https://discord.gg/example",
                "icon": "https://example.com/icon.png",
                "name": "RIZZ Collection",
                "slug": "rizz-collection",
                "twitter_link": "https://twitter.com/example",
                "website_link": "https://example.com"
            },
            "inscriptions": [
                {
                    "id": "af0b19432a676551223e300e7197348b7c225cb7b31d0d7c6e246e382cbf6f81i0",
                    "meta": {
                        "name": "Planetary Ordinal #11",
                        "attributes": [
                            {
                                "trait_type": "Background",
                                "value": "Sun sun"
                            },
                            {
                                "trait_type": "Holes",
                                "value": "rose blossom"
                            }
                        ]
                    }
                }
            ]
        }
    }
    runes = {
        "function": "DeFi application logic",
        "parameters": "Smart contract parameters"
    }
    brc20 = {
        "token_id": "RZ23Token",
        "amount": 1000
    }
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
        'miner_count': miner_count,
        'metadata': metadata,
        'nft_info': nft_info,
        'runes': runes,
        'brc20': brc20,
        'zk_proof': {}
    }
    blocks.append(block)
    
    # Generate SNARK proof for the new block
    proof = generate_snark_proof(data, nonce)
    proofs.append(proof)
    
    # Update the block with the zk proof details
    block['zk_proof'] = {
        'recursive_proof': proof,
        'previous_proof_hash': hashlib.sha256(proofs[-1].encode('utf-8')).hexdigest() if len(proofs) > 1 else None
    }
    
    return jsonify({'message': 'RIZZ Block created', 'block': block['id'], 'proof': proof})

def generate_snark_proof(data, nonce):
    # Prepare the input for snarkjs
    input_data = {
        "data": data,
        "nonce": nonce
    }
    with open('input.json', 'w') as f:
        json.dump(input_data, f)
    
    # Run snarkjs to generate proof
    try:
        subprocess.run(['snarkjs', 'plonk', 'setup', 'input.json'], check=True)
        subprocess.run(['snarkjs', 'plonk', 'prove', 'input.json', 'proof.json', 'public.json'], check=True)
        with open('proof.json') as f:
            proof = json.load(f)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        proof = "Error generating proof"
    
    return proof

@app.route('/start', methods=['POST'])
def start_chain():
    # Logic to start the chain
    return jsonify({'message': 'RZ-23 chain started'})

@app.route('/stop', methods=['POST'])
def stop_chain():
    # Logic to stop the chain
    return jsonify({'message': 'RZ-23 chain stopped'})

if __name__ == '__main__':
    app.run(debug=True)
