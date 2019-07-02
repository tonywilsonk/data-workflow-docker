# encoding: utf-8

from __future__ import absolute_import

import os
import shutil

import requests
import hashlib
from PIL import Image
import numpy as np
import re
from mongoengine.errors import NotUniqueError
from models.documents import Image as Post, Task

from mongoengine import connect

MONGO_DATABASE = os.getenv('MONGO_DATABASE', 'workflowdb')
MONGO_USERNAME = os.getenv('MONGO_USERNAME', 'root')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'breacmpa')
MONGO_HOST = os.getenv('MONGO_HOST', 'mongodb')


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


def image_to_gray(ref_number, **context):

    task_ids = 'extract_task_%d' % ref_number
    file_path = context['task_instance'].xcom_pull(task_ids=task_ids)

    im = Image.open(file_path)
    np_im = np.array(im)
    np_im = np_im.sum(2) / 3
    np_im = np_im.astype(np.uint8)
    head, tail = os.path.split(file_path)
    file_path_gray = os.path.join(head, 'gray_' + tail)
    new_im = Image.fromarray(np_im)
    new_im.save(file_path_gray)

    return file_path_gray


def image_to_md5(ref_number, **context):

    task_ids = 'extract_task_%d' % ref_number
    file_path = context['task_instance'].xcom_pull(task_ids=task_ids)

    return hashlib.md5(open(file_path, 'rb').read()).hexdigest()


def save_image_metadata(ref_number, **context):

    db = connect(MONGO_DATABASE, host=MONGO_HOST, port=27017, username=MONGO_USERNAME, password=MONGO_PASSWORD,
                 authentication_source='admin', connect=False)

    task_ids = 'gray_task_%d' % ref_number
    file_path_gray = context['task_instance'].xcom_pull(task_ids=task_ids)

    task_ids = 'md5_task_%d' % ref_number
    md5 = context['task_instance'].xcom_pull(task_ids=task_ids)

    im = Image.open(file_path_gray)
    width, height = im.size

    try:
        post = Post(md5=md5, width=width, height=height)
        content_type = Image.MIME[im.format]
        post.gray.put(file_path_gray, content_type=content_type)

        post.save()

    except NotUniqueError as ex:
        return True

    return True


def on_workflow_error(url, working_dir_path):

    db = connect(MONGO_DATABASE, host=MONGO_HOST, port=27017, username=MONGO_USERNAME, password=MONGO_PASSWORD,
                 authentication_source='admin', connect=False)

    task = Task(url=url, state='error')
    task.save()

    # delete working dir
    shutil.rmtree(working_dir_path)

    return True


def on_workflow_success(url, working_dir_path):

    db = connect(MONGO_DATABASE, host=MONGO_HOST, port=27017, username=MONGO_USERNAME, password=MONGO_PASSWORD,
                 authentication_source='admin', connect=False)

    task = Task(url=url, state='success')
    task.save()

    # delete working dir
    shutil.rmtree(working_dir_path)

    return True
