import os
import logging

from flask import Flask
from imghdr import what


logging.basicConfig(level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)


@app.route('/refresh')
def refresh():
    def index_dir_imgs(path, previous_id):
        paths = []
        current_id = previous_id
        with os.scandir(path) as ls:
            for entry in ls:
                if entry.is_dir():
                    (sub_paths, current_id) = index_dir_imgs(
                        entry.path, current_id)
                    for sub_path in sub_paths:
                        paths.append(sub_path)
                if entry.is_file() and what(entry.path) is not None:
                    paths.append({
                        'id': current_id,
                        'name': entry.name,
                        'path': entry.path,
                        'tags': ['untagged']
                    })
                    current_id += 1
        return (paths, current_id)

    def index_all_subdir_imgs(root_path):
        return index_dir_imgs(root_path, 0)

    return "Not fully implemented yet!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5002')
