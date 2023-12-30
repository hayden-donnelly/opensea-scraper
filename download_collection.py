from urllib import request
import json
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', type=str, required=True)
    args = parser.parse_args()

    for i in range(49):
        with open(f'{args.collection}/{i}.json', 'r') as f:
            nft_data = dict(json.load(f))['nfts']
        for nft in nft_data:
            request.urlretrieve(nft['image_url'], f'milady-collection/{nft["identifier"]}.png')
            request.urlretrieve(nft['metadata_url'], f'milady-collection/{nft["identifier"]}.json')

if __name__ == '__main__':
    main()