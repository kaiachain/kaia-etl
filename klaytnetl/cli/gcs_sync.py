# MIT License
#
# Modifications Copyright (c) klaytn authors
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import glob
import logging
import shutil

from google.cloud import storage
from google.oauth2 import service_account


def get_path(tmpdir, path):
    if path is None:
        return None
    elif tmpdir is None:
        return os.path.normpath(path)
    else:
        return os.path.normpath(os.path.join(tmpdir, path))


def sync_to_gcs(bucket, tmpdir, outputs, is_single_file):
    client = storage.Client()
    bucket_name = client.get_bucket(bucket)

    for output_path in filter(lambda o: o is not None, outputs):
        temp_path = get_path(tmpdir, output_path)
        for file in _get_files(temp_path, is_single_file):
            out = os.path.join(os.path.normpath(output_path), os.path.basename(file))
            logging.info(f"Transfer {file} --> gcs://{bucket}/{out}")
            blob = bucket_name.blob(f'{bucket}/{out}')
            blob.upload_from_filename(f'{file}')
        shutil.rmtree(temp_path)


def _get_files(path, is_single_file):
    import os, glob

    if is_single_file:
        path = os.path.normpath(path)
    else:
        path = os.path.join(os.path.normpath(path), "*")

    return glob.glob(path)
