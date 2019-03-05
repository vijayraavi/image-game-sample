import logging
import json

import azure.functions as func

from . import fetch_image
from common import image_helper


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    random_image, image_name = fetch_image.fetch_random_image()
    image_coded = image_helper.encode_image_base64(random_image)
    image_id = image_helper.get_hash(image_name)

    json_response = {
        'id': image_id,
        'encoded_image': image_coded
    }

    return func.HttpResponse(
        json.dumps(json_response),
        headers={'Access-Control-Allow-Origin': '*'},
        status_code=200,
        mimetype='application/json'
    )
