## RZ-20

### Overview

The RZ-20 Block Visualizer is a web application that provides real-time visualization of Bitcoin block data and simulates the creation of RIZZ blocks on top of the Bitcoin blockchain. Each new Bitcoin block triggers the creation of a corresponding RIZZ block, and miners participating in the RIZZ blocks are rewarded with a flat rate of 1 RIZZ.

### Features

- **Real-time Bitcoin Block Data**: Fetches and displays the latest Bitcoin block height, hashrate, and block number.
- **RIZZ Block Simulation**: Simulates RIZZ block creation triggered by new Bitcoin blocks.
- **In-Memory Data Storage**: Stores all block data in memory for easy testing and development.


### File Descriptions

- **app.py**: The main Flask application. Handles routes for fetching Bitcoin data, creating and retrieving RIZZ blocks, and serving the frontend.
- **static/app.js**: JavaScript file for fetching data and updating the frontend dynamically.
- **static/styles.css**: CSS file for styling the web application with a dark theme.
- **templates/index.html**: The main HTML template for the web application.

### API Endpoints

- **GET /bitcoin**: Fetches the latest Bitcoin block data from the Blockstream API.
- **POST /blocks**: Creates a new RIZZ block with the provided data.
- **GET /blocks**: Retrieves all RIZZ blocks stored in memory.
- **POST /trigger**: Triggers the creation of a new RIZZ block based on the latest Bitcoin block.

### Data Structure

RIZZ blocks are stored in memory as a list of dictionaries. Each block contains the following fields:
- `id`: Unique identifier for the block.
- `data`: Original data of the block.
- `compressed_data`: Brotli-compressed data.
- `nonce`: Nonce value used in the block.
- `hash`: SHA-256 hash of the block data and nonce.
- `reward`: Total RIZZ reward for the block.
- `miner_count`: Number of miners who participated in creating the block.

### Example

Example of a RIZZ block:
```json
{
  "id": 1,
  "data": "Bitcoin Block Height: 680000",
  "compressed_data": "<binary data>",
  "nonce": 680000,
  "hash": "0000000000000000000abc...",
  "reward": 5,
  "miner_count": 5
}
```

### Contributing

Contributions are welcome! Please fork the repository and build some cool stuff

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.

### Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Chart.js](https://www.chartjs.org/)
- [Bootstrap](https://getbootstrap.com/)
- [Blockstream API](https://blockstream.info/api/)

---