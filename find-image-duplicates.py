#!/usr/bin/env python

from imagededup.methods import PHash
import os
import argparse
from pathlib import Path

def main(args):
    image_folder = args['images']
    duplicatesd_folder = args['duplicates']

    phasher = PHash()
    encodings = phasher.encode_images(image_dir=image_folder, recursive=True)
    # duplicates = phasher.find_duplicates(encoding_map=encodings, scores=True, max_distance_threshold=0)
    duplicates_to_remove = phasher.find_duplicates_to_remove(encoding_map=encodings, max_distance_threshold=0)

    print('')
    for image in duplicates_to_remove:
        source_file = Path(image_folder) / Path(image)
        target_file = Path(duplicatesd_folder) / Path(source_file.name)
        print(f'moving {source_file} to {target_file}')
        source_file.rename(target_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find Image Duplicates')
    parser.add_argument('--images', default='./photos', metavar='PATH', type=Path, help='path to image files')
    parser.add_argument('--duplicates', default='./photos_duplicates', metavar='PATH', type=Path, help='path to duplicates image files')
    # parser.add_argument('--features', default=6, type=int, metavar='N', help='max features')
    # parser.add_argument('--z-score', default=4, type=int, metavar='N', help='z-score')
    main(vars(parser.parse_args()))
