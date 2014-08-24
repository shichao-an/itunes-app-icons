#!/usr/bin/env python

import itunes
import os
from PIL import Image
import requests
import sys
import uuid


class Search(object):
    def __init__(self, keyword):
        self.keyword = keyword

    @property
    def app(self):
        """Best matched app in the result"""
        results = itunes.search_app(self.keyword)
        return results[0]


class Icon(object):
    def __init__(self, artwork):
        self.artwork = artwork

    def download(self, path, size):
        url = self.artwork['60']
        temp_path = os.path.join('/tmp', str(uuid.uuid4()))
        download(temp_path, url)
        _size = size, size
        i = Image.open(temp_path)
        im = i.resize(_size, Image.ANTIALIAS)
        im.save(path, quality=100)
        os.remove(temp_path)


def download(path, url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)


def main():
    keyword = sys.argv[1]
    size = 42
    path = None
    if len(sys.argv) >= 3:
        size = int(sys.argv[2])
    if len(sys.argv) == 4:
        path = sys.argv[3]
    app = Search(keyword).app
    if path is None:
        path = app.name.lower() + '_icon.png'
    icon = Icon(app.artwork)
    icon.download(path, size)


if __name__ == '__main__':
    main()
