#!/usr/bin/env python

from imagededup.methods import PHash
import os
import argparse
from pathlib import Path
from flask import Flask, render_template, request
import webbrowser
from threading import Timer

def open_browser():
      webbrowser.open_new("http://localhost:5001")

def group_images(image_pairs, path):
    grouped = {}
    result = []
    for _img, connections in list(image_pairs.items()):
        if len(connections) > 0:
            img = f'{path}/{_img}'
            if img in grouped:
                continue
            new_group = [img]
            grouped[img] = True
            for _conn_img, weight in connections:
                conn_img = f'{path}/{_conn_img}'
                if conn_img not in grouped:
                    new_group.append(conn_img)
                    grouped[conn_img] = True
            new_group.sort()
            result.append((new_group, weight))
    return result

def main(args):
    # TODO check folders for existence
    image_folder = args['images'].name
    duplicates_folder = args['duplicates'].name

    phasher = PHash()
    encodings = phasher.encode_images(image_dir=image_folder, recursive=True)
    # duplicates_to_remove = phasher.find_duplicates_to_remove(encoding_map=encodings, max_distance_threshold=0)
    duplicates = {
        'a_img_0127.jpg': [],
        'a/img_0799.jpg': [('a/img_0798.jpg', 10)],
        'a/img_0772.jpg': [('a/img_0773.jpg', 4)],
        'a/img_0766.jpg': [('a/img_0765.jpg', 8)],
        'a/img_0216.jpg': [],
        'a/img_0570.jpg': [('a/img_0571.jpg', 8), ('a/img_0569.jpg', 8)],
        'a/img_0564.jpg': [('a/img_0566.jpg', 8)],
        'a/img_0202.jpg': [('a/img_0201.jpg', 8)],
        'a/img_0558.jpg': [],
        'a/img_0389.jpg': [('a/img_0398.jpg', 10)]
    }
    duplicates = phasher.find_duplicates(encoding_map=encodings, scores=True, max_distance_threshold=args['threshold'])

    # move duplicates_to_remove into duplicates_folder
    # for image in duplicates_to_remove:
        # source_file = Path(image_folder) / Path(image)
        # target_file = Path(duplicates_folder) / Path(source_file.name)
        # print(f'moving {source_file} to {target_file}')
        # source_file.rename(target_file)

    # open duplicates webapp in browser
    if args['www'] == True:
        app = Flask(__name__, template_folder='.', static_url_path='', static_folder='.')

        @app.route('/')
        def index_page():
            return render_template('./find-image-duplicates.html', duplicates=group_images(duplicates, image_folder))

        @app.route('/move', methods=['POST'])
        def move_image():
            request_data = request.get_json()
            p = Path(request_data['path'])
            target_folder = duplicates_folder if list(p.parents)[-2].name == image_folder else image_folder
            target = Path(target_folder).joinpath(*p.parts[1:])
            Path(target).parents[0].mkdir(parents=True, exist_ok=True)
            p.rename(target)
            return {'path': str(target)}

        # Timer(1, open_browser).start()
        app.run("localhost", "5001")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage Image Duplicates')
    parser.add_argument('--images', default='./photos', metavar='PATH', type=Path, help='image folder')
    parser.add_argument('--duplicates', default='./photos_duplicates', metavar='PATH', type=Path, help='folder for image duplicates')
    parser.add_argument('--threshold', default=10, type=int, metavar='N', help='max distance threshold')
    parser.add_argument('--www', action='store_true', default=False, help='start image de-selection tool in browser')
    main(vars(parser.parse_args()))
