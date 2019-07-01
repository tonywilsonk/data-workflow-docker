# encoding: utf-8

from flask import Flask, make_response
from models.documents import Image, Task
import json
from werkzeug.exceptions import BadRequest, NotFound, InternalServerError

app = Flask(__name__)


@app.route('/image/<md5>', methods=['GET'])
def get_image(md5):
    image = Image.objects(md5=md5).first()

    if image:
        content_type = image.gray.content_type
        response = make_response(image.gray.read())
        response.headers.set('Content-Type', content_type)

        return response

    payload = {"status": 404, "code": 'not found', "message": "image with the provided md5: %s doesn't exist" % md5}
    response = make_response(json.dumps(payload), 404)
    response.headers.set('Content-Type', "application/json")

    return response


@app.route('/monitoring', methods=['GET'])
def monitoring():

    pipeline = [
        {"$match": {"state": "error"}},
        {'$addFields': {"timestamp": {'$dateToString': {'format': '%Y-%m-%d %H:%M:00', "date": '$create_at'}}}},
        {"$group": {"_id": {'timestamp': "$timestamp"}, "errors": {"$sum": 1}}},
        {'$sort': {'_id.timestamp': 1}},
    ]

    task_errors = Task.objects.aggregate(*pipeline)
    hist = []
    for r in task_errors:
        hist.append(r)

    payload = {"count": len(hist), "results": hist}

    response = make_response(json.dumps(payload))
    response.headers.set('Content-Type', "application/json")

    return response


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    payload = {"status": 400, "code": 'bad request', "message": "Bad request error"}
    response = make_response(json.dumps(payload), 400)
    response.headers.set('Content-Type', "application/json")

    return response


@app.errorhandler(NotFound)
def handle_404request(e):
    payload = {"status": 404, "code": 'not found', "message": "page not found."}
    response = make_response(json.dumps(payload), 404)
    response.headers.set('Content-Type', "application/json")

    return response


@app.errorhandler(InternalServerError)
def handle_500_request(e):
    payload = {"status": 500, "code": 'server error', "message": "An internal server error occur, please retry later."}
    response = make_response(json.dumps(payload), 500)
    response.headers.set('Content-Type', "application/json")

    return response
