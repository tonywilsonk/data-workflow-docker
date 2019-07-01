# encoding: utf-8

import os
import uuid

from workflow.tasks import download_file, image_to_gray, image_to_md5, save_image_metadata, on_workflow_success,\
    on_workflow_error
from celery import chain, chord, group


DATA_PATH = os.getenv('DATA_PATH', '/tmp')


def run_workflow(url):

    # getting the working dir
    work_dir = os.path.join(DATA_PATH, str(uuid.uuid4()))

    # define workflow
    extract = download_file.s(url, work_dir)
    transform = group(image_to_gray.s(), image_to_md5.s())
    load = save_image_metadata.s()

    workflow = chain(extract, chord(transform, load), on_workflow_success.si(url, work_dir))
    workflow.apply_async(link_error=on_workflow_error.si(url, work_dir))


if __name__ == '__main__':

    # read the file and run the workflow

    with open('urls.txt') as f:
        for line in f:
            run_workflow(line.rstrip('\n'))


