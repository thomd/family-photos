#!/usr/bin/env python

from imagededup.methods import PHash
import os
import argparse
import json
from pathlib import Path

import warnings
warnings.filterwarnings('ignore')

def main(args):
    if not args['images'].exists():
        print(f"folder '{args['images']}' does not exist")
        return

    image_folder = args['images']
    duplicates_folder = Path(f'{image_folder.name}_duplicates')

    phasher = PHash()
    duplicates_to_remove = phasher.find_duplicates_to_remove(image_dir=image_folder.name, recursive=True, max_distance_threshold=0, outfile='removed.json')
    for image in duplicates_to_remove:
        source_file = image_folder / Path(image)
        target_file = duplicates_folder / Path(source_file.name)
        print(f'moving {source_file} to {target_file}')
        source_file.rename(target_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage Image Duplicates', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--images', default='./photos', metavar='PATH', type=Path, help='image folder')
    main(vars(parser.parse_args()))
