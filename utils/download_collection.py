import os
import requests
import json
import argparse
from urllib.request import urlretrieve

def get_url(collection_id, next_string):
    limit = 200
    if next_string == None:
        return f'https://api.opensea.io/api/v2/collection/{collection_id}/nfts?limit={limit}'
    return f'https://api.opensea.io/api/v2/collection/milady/nfts?limit={limit}&next={next_string}'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', type=str, required=True)
    parser.add_argument('--api_key', type=str, required=True)
    parser.add_argument('--limit', type=int, default=200)
    args = parser.parse_args()

    collection_path = os.path.join('data', args.collection)
    if not os.path.exists(collection_path):
        os.makedirs(collection_path)

    collection_data = []
    next_string = None
    next_string_key = 'next'
    nfts_key = 'nfts'
    headers = {'accept': 'application/json', 'x-api-key': args.api_key}

    while True:
        url = get_url(args.collection, next_string)
        response = dict(json.loads(requests.get(url, headers=headers).text))
        collection_data.extend(response[nfts_key])
        print(f'{len(collection_data)} NFTs have been parsed.')

        if next_string_key not in response.keys():
            break
        next_string = response['next']

    num_downloaded = 0
    for nft in collection_data:
            identifier = nft['identifier']
            image_path = os.path.join(collection_path, f'{identifier}.png')
            metadata_path = os.path.join(collection_path, f'{identifier}.json')
            urlretrieve(nft['image_url'], image_path)
            urlretrieve(nft['metadata_url'], metadata_path)
            num_downloaded += 1
            print(f'{num_downloaded} NFTs have been downloaded.')

if __name__ == '__main__':
    main()
