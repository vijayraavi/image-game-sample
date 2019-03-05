import logging
import json

import azure.functions as func

from random import randint

from common import image_helper
from common import constants


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Grab the required params
    image = req.params.get('image')
    if not image:
        try:
            req_body = json.loads(req.get_body().decode())
        except ValueError:
            raise
        else:
            image = req_body.get('image')

    if image:
        # We decode the image, get a random angle, rotate the image and encode it back
        decoded_image = image_helper.decode_image_base64(image)
        random_rotate_angle = randint(0, 10) * constants.ROTATE_ANGLE_DEFAULT
        image_rotated_bytes = image_helper.rotate_image(decoded_image, random_rotate_angle)
        encoded_image = image_helper.encode_image_base64(image_rotated_bytes)

        # This is our response
        json_response = {
            'encoded_image': encoded_image
        }

        return func.HttpResponse(
            json.dumps(json_response),
            headers={'Access-Control-Allow-Origin': '*'},
            status_code=200,
            mimetype='application/json'
        )

    else:
        return func.HttpResponse(
            'Please pass an image in the query string or the body',
            headers={'Access-Control-Allow-Origin': '*'},
            status_code=400
        )
