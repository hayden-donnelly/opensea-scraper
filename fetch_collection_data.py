import requests
import json
import argparse

def get_url(next_string):
    limit = 200
    if next_string == None:
        return f'https://api.opensea.io/api/v2/collection/milady/nfts?limit={limit}'
    return f'https://api.opensea.io/api/v2/collection/milady/nfts?limit={limit}&next={next_string}'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', type=str, required=True)
    parser.add_argument('--api_key', type=str, required=True)
    parser.add_argument('--limit', type=int, default=200)
    args = parser.parse_args()

    num_parsed = 0
    next_string = None
    headers = {
        'accept': 'application/json',
        'x-api-key': args.api_key
    }

    while True:
        url = get_url(next_string)
        response = dict(json.loads(requests.get(url, headers=headers).text))
        print(response)
        with open(f'{args.collection}/{num_parsed}.json', 'w') as f:
            json.dump(response, f, indent=4)
        next_string = response['next']
        num_parsed += 1

if __name__ == '__main__':
    main()