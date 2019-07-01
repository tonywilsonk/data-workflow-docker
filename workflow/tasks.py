# encoding: utf-8

from __future__ import absolute_import

import os
import shutil
from celery.utils.log import get_task_logger
from workflow.celery import app

import requests
import hashlib
from PIL import Image
import numpy as np
import re
from mongoengine.errors import NotUniqueError
from models.documents import Image as Post, Task


import socket
timeout = 300
socket.setdefaulttimeout(timeout)


logger = get_task_logger(__name__)


DATA_PATH = os.getenv('DATA_PATH', '/tmp')


def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0].replace('"', '')


@app.task
def download_file(url, work_dir_path):

    # make work dir if no exists
    if not os.path.exists(work_dir_path):
        os.makedirs(work_dir_path)

    # download image
    r = requests.get(url, allow_redirects=True)
    # raise exception if error
    r.raise_for_status()

    # save file and return path
    filename = get_filename_from_cd(r.headers.get('content-disposition'))
    file_path = os.path.join(work_dir_path, filename)
    open(file_path, 'wb').write(r.content)

    return file_path


@app.task
def image_to_gray(file_path):

    im = Image.open(file_path)
    np_im = np.array(im)
    np_im = np_im.sum(2) / 3
    np_im = np_im.astype(np.uint8)
    head, tail = os.path.split(file_path)
    file_path_gray = os.path.join(head, 'gray_' + tail)
    new_im = Image.fromarray(np_im)
    new_im.save(file_path_gray)

    return file_path_gray


@app.task
def image_to_md5(file_path):
    return hashlib.md5(open(file_path, 'rb').read()).hexdigest()


@app.task
def save_image_metadata(results):
    file_path_gray, md5 = results
    im = Image.open(file_path_gray)
    width, height = im.size

    try:
        post = Post(md5=md5, width=width, height=height)
        content_type = Image.MIME[im.format]
        post.gray.put(file_path_gray, content_type=content_type)

        post.save()

    except NotUniqueError as ex:
        logger.info('image already processed....')
        return True

    return True


@app.task
def on_workflow_error(url, working_dir_path):

    task = Task(url=url, state='error')
    task.save()

    # delete working dir
    shutil.rmtree(working_dir_path)

    return True


@app.task
def on_workflow_success(url, working_dir_path):

    task = Task(url=url, state='success')
    task.save()

    # delete working dir
    shutil.rmtree(working_dir_path)

    return True
