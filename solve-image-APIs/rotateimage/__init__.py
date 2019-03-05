import logging
import json

import azure.functions as func

from common import image_helper
from common import constants


def main(req: func.HttpRequest) -> func.HttpResponse:
    # Grab the required params
    image = req.params.get('image')
    direction = req.params.get('direction')
    if not image:
        try:
            req_body = json.loads(req.get_body().decode())
        except ValueError:
            pass
        else:
            image = req_body.get('image')
            direction = req_body.get('direction')

    if image and direction:
        # We decode the image, use the direction to rotate once and encode the image back
        decoded_image = image_helper.decode_image_base64(image)
        rotate_angle = constants.ROTATE_ANGLE_DEFAULT
        if direction != 'counter':
            rotate_angle *= -1
        image_rotated_bytes = image_helper.rotate_image(decoded_image, rotate_angle)
        encoded_image = image_helper.encode_image_base64(image_rotated_bytes)

        # Create a json with the encoded image to send it as the response
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
