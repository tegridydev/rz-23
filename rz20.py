import bz2

def bzip2_compress(data):
    compressed_data = bz2.compress(data.encode('utf-8'))
    return compressed_data

def bzip2_decompress(compressed_data):
    decompressed_data = bz2.decompress(compressed_data).decode('utf-8')
    return decompressed_data

metadata = {
    'Block Hash': '0000000000000000000abc',
    'Timestamp': '2024-05-24 12:34:56',
    'Miner Address': '1A2B3C4D5E6F7G8H9I0J',
    'Transaction Count': '1000',
    'Block Size': '1MB'
}

metadata_str = ','.join([f'{key}:{value}' for key, value in metadata.items()])
compressed_data = bzip2_compress(metadata_str)
decompressed_metadata_str = bzip2_decompress(compressed_data)

print("Original Metadata:", metadata_str)
print("Compressed Data Length:", len(compressed_data))
print("Decompressed Metadata:", decompressed_metadata_str)
