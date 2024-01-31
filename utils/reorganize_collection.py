import os
import argparse
import json
import shutil
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--collection', type=str, required=True)
    args = parser.parse_args()

    collection_dir = os.path.join('data', args.collection)
    assert os.path.exists(collection_dir), (
        f'The collection {args.collection} could not be found. '
        'Make sure you have downloaded it.'
    )

    reorganized_collection_dir = f'data/{args.collection}_reorganized'
    assert not os.path.exists(reorganized_collection_dir), (
        'The destination for the reorganized collection is occupied '
        f'({reorganized_collection_dir}). '
        'Try deleting it and running this script again.'
    )

    metadata = []
    collection_list = os.listdir(collection_dir)
    images_subdir = 'images'
    os.makedirs(os.path.join(reorganized_collection_dir, images_subdir))
    for file in collection_list:
        if not file.endswith('.json'):
            continue
        identifier = file.split('.')[0]
        full_path = os.path.join(collection_dir, file)
        
        try:
            with open(full_path, 'r') as f:
                current_metadata = json.load(f)
                new_image_path = f'{images_subdir}/{identifier}.png'
                metadata.append({
                    'file_name': new_image_path,
                    'attributes': current_metadata['attributes'],
                    'remote_url': current_metadata['image']
                })
                shutil.copy(
                    os.path.join(collection_dir, f'{identifier}.png'),
                    os.path.join(reorganized_collection_dir, new_image_path)
                )
        except:
            print(f'Could not load {full_path}, skipping...')
    df = pd.DataFrame(metadata)
    print(df.head())
    df.to_json(
        os.path.join(reorganized_collection_dir, 'metadata.json'), 
        orient='records', 
        lines=True
    )

if __name__ == '__main__':
    main()
